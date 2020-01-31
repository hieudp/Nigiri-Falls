from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def login_view(request):
    """
    Log out if logged in.
    Else take the username and password and attempt to login.
    Return to home if successfull or stay if not.
    """
    if request.user.is_authenticated:
        logout(request)
        return redirect('home')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        return render(request, 'login/login.html', {'session': request.session, 'error': True, 'username': username})
    return render(request, 'login/login.html', {'session': request.session})

def registration_view(request):
    """
    If the requst method is GET, return a page with a blank form.
    If POST, create a form with the input and validate it.
    If successful create a User object, save it in the database and redirect to login.
    """
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        errors = [False, False]
        # Checks that...
        # username is available
        if User.objects.filter(username=phone_number).exists():
            errors[0] = True
        # username correct length and numeric
        elif not len(phone_number) == 8 or not phone_number.isdigit():
            errors[1] = True
        if any(errors):
            data = [phone_number, first_name, last_name, email]
            return render(request, 'login/registration.html', {'session': request.session, 'errors': errors, 'data': data})

        user = User.objects.create_user(username=phone_number)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.set_password(password)
        user.save()
        return redirect('login')
    return render(request, 'login/registration.html', {'session': request.session})

def promote_view(request):
    """
    Renders a page with a number input and a button.
    If the button was pressed, retrieve and promote the User. If successful or not, render the same page with a message
    """
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        phone_number = request.POST.get('phonenumber')
        try:
            user = User.objects.get(username=phone_number)
            if user.is_staff:
                return render(request, 'login/promote.html', {'session': request.session, 'message': 'User is already staff'})
            user.is_staff = True
            user.save()
            return render(request, 'login/promote.html', {'session': request.session, 'message': 'User promoted to staff'})
        except:
           return render(request, 'login/promote.html', {'session': request.session, 'message': 'Phone number "' + str(phone_number) + '" not found'})
    return render(request, 'login/promote.html', {'session': request.session})
