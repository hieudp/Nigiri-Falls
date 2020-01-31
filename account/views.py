from django.shortcuts import render

from django.contrib.auth.models import User

# Create your views here.


def account_view(request):
    """
    Changes user information if the submit-button is pressed and the input is valid
    """

    account = User.objects.get(id=request.user.id)

    actions_names = ['Phone number', 'First name', 'Last name', 'Email', 'Password']
    action = ""

    if request.method == "POST":
        if request.POST['send'] == 'Change phone number':
            phone_number = request.POST['username']
            if len(phone_number) == 8 and phone_number.isdigit(): # Check if input is 8 digits
                account.username = phone_number
                action = actions_names[0]
        if request.POST['send'] == 'Change first name':
            first_name = request.POST['first_name']
            if first_name.strip():  # Check for empty string and whitespace
                account.first_name = first_name
                action = actions_names[1]
        if request.POST['send'] == 'Change last name':
            last_name = request.POST['last_name']
            if last_name.strip():  # Check for empty string and whitespace
                account.last_name = last_name
                action = actions_names[2]
        if request.POST['send'] == 'Change email':
            email = request.POST['email']
            if email.strip():  # Check for empty string and whitespace
                account.email = email
                action = actions_names[3]
        if request.POST['send'] == 'Change password':
            password = (request.POST['password'])
            if password.strip():  # Check for empty string and whitespace
                account.set_password(password)
                action = actions_names[4]
        account.save()

    return render(request, 'account/account.html', {'session': request.session, 'account': account, 'action' : action})
