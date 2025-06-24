from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message, Product
from django.contrib.auth.models import User
from users.models import CustomUser
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.db.models import Q
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Personalization, To
from home import settings


@login_required(login_url='/users/log_in/')
def conversation_list(request):
    conversations = request.user.conversations.filter(display=True)
    return render(request, 'conversation_list.html', {'conversations': conversations})

@login_required(login_url='/users/log_in/')
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    conversation.display = True
    conversation.save()

    # Get the other participant (not the current user)
    other_user = conversation.participants.exclude(id=request.user.id).first()

    if request.user not in conversation.participants.all():
        return HttpResponseForbidden("You are not authorized to view this conversation.")

    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Message.objects.create(conversation=conversation, sender=request.user, text=text)

            # Send notification email using SendGrid dynamic template
            try:
                conversation_url = request.build_absolute_uri(
                    reverse('conversation_detail', kwargs={'conversation_id': conversation.id})
                )

                # Get the recipient's name from CustomUser model
                recipient_name = other_user.full_name if other_user.full_name else "Student"
                sender_name = request.user.full_name if request.user.full_name else "Anonymous"

                template_data = {
                    'recipient_name': recipient_name,
                    'sender_name': sender_name,
                    'message_preview': text[:150] + '...' if len(text) > 150 else text,
                    'conversation_url': conversation_url
                }
                
                # Create the email message with dynamic template
                message = Mail(
                    from_email='cmill026@students.bju.edu',
                    to_emails=To(other_user.email),
                    subject=f'New message from {sender_name} - Campus Exchange'
                )
                
                # Set the template ID (replace with your actual SendGrid template ID)
                message.template_id = 'd-3748a6d436d143b29ff38b686d6044a3'  # Get this from SendGrid dashboard

                # Add dynamic template data
                message.dynamic_template_data = template_data

                sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                response = sg.send(message)
                print(f"SendGrid status: {response.status_code}")
                
                if response.status_code == 202:
                    print("Email sent successfully!")
                else:
                    print(f"Email sending failed with status: {response.status_code}")

            except Exception as e:
                print(f"SendGrid error: {str(e)}")
                import traceback
                print(f"Full error: {traceback.format_exc()}")

        return redirect('conversation_detail', conversation_id=conversation.id)

    return render(request, 'conversation_details.html', {'conversation': conversation})

@login_required(login_url='/users/log_in/')
def start_conversation(request):
    user = request.user
    other_user_email = request.GET.get('user_id')
    product_id = request.GET.get('product_id')

    # Get the other user and product
    other_user = get_object_or_404(CustomUser, email=other_user_email)
    product = get_object_or_404(Product, id=product_id)

    # Check if a conversation for this product between these users already exists
    
    conversation = Conversation.objects.filter(
        product=product,
        participants__in=[user, other_user]
    ).distinct().filter(participants=user).filter(participants=other_user).first()


    # Create a new conversation if none exists
    if not conversation:
        conversation = Conversation.objects.create(product=product)
        conversation.participants.add(user, other_user)

    return redirect(reverse('conversation_detail', kwargs={'conversation_id': conversation.id}))


@login_required(login_url='/users/log_in/')
def delete_conversation(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    conversation.display = False
    conversation.save()
    return redirect('/messaging')