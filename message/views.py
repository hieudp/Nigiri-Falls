from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from .models import Message

def message_view(request):

    """
    Creates a new message if the input is correct.
    This means that the receiver is a user in the database.
    """

    try:
        user = User.objects.get(id = request.user.id)
        if not request.user.is_staff:
            return redirect('home')

        error = False
        if request.method == 'POST':
            sender = User.objects.get(id = request.user.id)
            receiver_number = request.POST['receiver']
            receiver = User.objects.get(username = receiver_number)
            subject = request.POST['subject']
            content = request.POST['content']

            message = Message.objects.create(sender=sender, receiver=receiver, msg_subject=subject, msg_content=content)

            message.save()

        return render(request, 'message/message.html', {'session': request.session, 'error' : error })
    except:
        error = True
        return render(request, 'message/message.html', {'session': request.session, 'error' : error })


def messagelist_view(request):

    """
    Creates a list of the messages in which a user is the receiver.
    A staff user can see all the messages sent.
    """

    user = User.objects.get(id = request.user.id)

    messages = []
    allMessages = Message.objects.all()

    if not user.is_staff:
        for message in allMessages:
            if message.receiver == user:
                messages.append(message)

    else:
        for message in allMessages:
            messages.append(message)

    return render(request, 'message/messagelist.html', {'session': request.session, 'messages' : messages, 'user' : user})
