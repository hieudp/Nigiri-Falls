from functools import reduce

from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from home.models import Dish
from .models import Order, OrderItem
from rating.models import Rating
from django.db.models import Avg, Sum

def cart(request):
    """
    If the request method is GET, simply render the page.
    If is POST it means Set Order was pressed.
    Check if the user is logged in, if set an error message.
    Check if the amount of dishes is greater than 0. If not set another error message.
    If there are errors render the page with those.
    If not get the User from the database and the restaurant and datetime from the form.
    Create a new Order with the data. Get the dishes from request.session and add them as an OrderItem to the Order.
    If the OrderItem already exists, then retrieve it from the database. If not, create a new entry.
    Save to the database and redirect to confirmation.
    """
    dishes = Dish.objects.all()
    price = 0
    for dishe in request.session['dishes']:
        for dish in dishes:
            if dish.name == dishe and dish.enabled == False:
                request.session['cartAmount'] -= request.session['dishes'][dishe][0]
                request.session['dishes'][dishe] = list(request.session['dishes'][dishe])
                request.session['dishes'][dishe][0] = 0
                request.session['dishes'][dishe] = tuple(request.session['dishes'][dishe])
    for dish in request.session['dishes'].values():
        price += dish[0] * dish[1]
    if request.method == 'POST':
        errors = [False, False]
        if not request.user.is_authenticated:
            errors[0] = True
        #maps the session variable to the amount of each dish, and reduces them to their sum
        amount = reduce((lambda x, y: x + y), list(map(lambda x: x[0], request.session['dishes'].values())))
        if amount == 0:
            errors[1] = True
        if errors[0] or errors[1]:
            return render(request, 'cart/cart.html', {'session': request.session, 'error': errors, 'price': price})
        order_user = User.objects.get(id=request.user.id)
        order_restaurant = request.POST.get('restaurant')
        order_datetime = request.POST.get('datetime')
        order = Order.objects.create(user=order_user, restaurant=order_restaurant, datetime=order_datetime)
        for dish_name, values in request.session['dishes'].items():
            if values[0] == 0:
                continue
            try:
                order_item = OrderItem.objects.get(dish=Dish.objects.get(name=dish_name), amount=values[0])
            except OrderItem.DoesNotExist:
                order_item = OrderItem.objects.create(dish=Dish.objects.get(name=dish_name), amount=values[0])
            order.items.add(order_item)
        order.price = price
        order.save()
        return redirect('confirmation')
    return render(request, 'cart/cart.html', {'session': request.session, 'price': price, 'dishes': dishes})


def confirmation(request):
    """
    Resets the session variable.
    Render the confirmation page.
    """
    if request.method == 'POST':
        rate = int(request.POST['rating'])
    
        user = User.objects.get(id=request.user.id)
        ratings = Rating.objects.filter(customer=user)

        if ratings:
            """sletter rating-objektet dersom det blir gjort av den samme brukeren"""
            for rating in ratings:
                rating.delete()

        rating = Rating.objects.create(customer=user, rate=rate)
        rating.save()

        """finner gjennomsnittlig rating ved å ta antall brukere/antall ratinger"""
        total_users = Rating.objects.count()
        all_ratings = Rating.objects.all()
        map1 = map(lambda x: x.rate, all_ratings)
        liste = list(map1)
        total_rating = reduce((lambda x, y: x + y), liste)
        avg = total_rating / total_users
        avg = round(avg, 2)

        return render(request, 'cart/confirmation.html', {'session': request.session, 'avg': avg, 'total_users': total_users, 'rate': rate, 'show_rating': False})
    
    request.session['dishes'] = {}
    dishes = Dish.objects.all()
    for dish in dishes:
        request.session['dishes'][dish.name] = (0, dish.price, dish.image)
    request.session['cartAmount'] = 0
    request.session['categories'] = 'All'

    return render(request, 'cart/confirmation.html', {'session': request.session, 'show_rating': True})
    
def increase(request, name):
    """
    Increases the number for the dish
    """
    request.session['dishes'][name][0] += 1
    request.session['cartAmount'] += 1
    return redirect('cart')

def decrease(request, name):
    """
    Decreases the number for the dish
    """
    if request.session['dishes'][name][0] > 0:
        request.session['dishes'][name][0] -= 1
        request.session['cartAmount'] -= 1
    return redirect('cart')