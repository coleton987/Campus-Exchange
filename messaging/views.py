from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message, Product
from django.contrib.auth.models import User
from users.models import CustomUser
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.db.models import Q
from django.conf import settings
import requests
import json


def send_message_notification_email(recipient_email, recipient_name, sender_name, message_preview, conversation_url):
    """Send message notification email using Brevo Transactional Email API"""
    try:
        # Brevo API endpoint
        url = "https://api.brevo.com/v3/smtp/email"
        
        # Headers for Brevo API
        headers = {
            'api-key': settings.EMAIL_API_KEY,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # Email payload with template
        payload = {
            "sender": {
                "name": "Campus Exchange",
                "email": settings.DEFAULT_FROM_EMAIL
            },
            "to": [
                {
                    "email": recipient_email,
                    "name": recipient_name
                }
            ],
            "templateId": 2,  # Your message notification template ID
            "params": {
                "recipient_name": recipient_name,
                "sender_name": sender_name,
                "message_preview": message_preview,
                "conversation_url": conversation_url
            }
        }
        
        # Send the email
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        print(f"Brevo Response Status: {response.status_code}")
        print(f"Brevo Response Body: {response.text}")
        
        # Check if request was successful
        if response.status_code == 201:
            return True
        else:
            print(f"Brevo API Error: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"Brevo Email Error: {e}")
        return False


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

            # Send notification email using Brevo
            try:
                conversation_url = request.build_absolute_uri(
                    reverse('conversation_detail', kwargs={'conversation_id': conversation.id})
                )

                # Get the recipient's name from CustomUser model
                recipient_name = other_user.full_name if other_user.full_name else "Student"
                sender_name = request.user.full_name if request.user.full_name else "Anonymous"

                # Prepare message preview (limit to 150 characters)
                message_preview = text[:150] + '...' if len(text) > 150 else text
                
                # Send notification email
                success = send_message_notification_email(
                    recipient_email=other_user.email,
                    recipient_name=recipient_name,
                    sender_name=sender_name,
                    message_preview=message_preview,
                    conversation_url=conversation_url
                )
                
                if success:
                    print("Message notification email sent successfully!")
                else:
                    print("Failed to send message notification email")

            except Exception as e:
                print(f"Email notification error: {str(e)}")
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