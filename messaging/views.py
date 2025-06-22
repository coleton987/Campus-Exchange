from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message, Product
from django.contrib.auth.models import User
from users.models import CustomUser
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.db.models import Q
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from home import settings


@login_required(login_url='/users/log_in/')
def conversation_list(request):
    conversations = request.user.conversations.filter(display=True)
    return render(request, 'conversation_list.html', {'conversations': conversations})

@login_required(login_url='/users/log_in/')
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    conversation.display = True
    other_user = conversation.participants.exclude(id=request.user.id).first().email
    conversation.save()
    if request.user not in conversation.participants.all():
        return HttpResponseForbidden("You are not authorized to view this conversation.")
    
    if request.method == 'POST':
        text = request.POST.get('text')
        Message.objects.create(conversation=conversation, sender=request.user, text=text)

        print(other_user)
        messages = Mail(
            from_email='cmill026@students.bju.edu',
            to_emails= other_user,
            subject='Campus Exchange Message',
            html_content=f'<strong>You have unread messages on Campus Exchange</strong>')
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(messages)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)

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