from datetime import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from cart.models import Order
from message.models import Message

def all_orders(orders):
    """
    Takes a list of orders as a parameter.
    Sort the order by datetime, and split them into to list; one list for upcoming orders and one list for past_orders.
    Returns a tuple of both lists.
    """
    orders = sorted(orders, key=lambda order: datetime.strptime(str(order.datetime)[:16], '%Y-%m-%d %H:%M'))
    upcoming_orders = []
    past_orders = []
    for order in orders:
        if datetime.strptime(str(order.datetime)[:16], '%Y-%m-%d %H:%M') <= datetime.now():
            past_orders.append(order)
        else:
            upcoming_orders.append(order)
    upcoming_orders = (upcoming_orders, 'Upcoming orders')
    past_orders = (reversed(past_orders), 'Past orders')
    return (upcoming_orders, past_orders)

def orders_view(request):
    """
    Get every order associated with the logged in user account.
    Sort the orders with a lambda by converting to python datetime.
    Return a render.
    """
    orders = Order.objects.filter(user=User.objects.get(id=request.user.id))
    if not orders:
        return render(request, 'orders/index.html', {'session': request.session})
    return render(request, 'orders/index.html', {'session': request.session, 'all_orders': all_orders(orders)})

def order_delete(request, pk):
    """
    Get every order associated with the current user and the order to be deleted.
    If the order is in the user orders, delete it and redirect to the list of orders.
    If the user is staff, send a message to the user that ordered the order.
    """
    print("Delete")
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        orders = Order.objects.filter(user=User.objects.get(id=request.user.id))
        if order in orders or request.user.is_staff:
            order.delete()
            if request.user.is_staff:
                sender = User.objects.get(username=request.user.username)
                receiver = order.user
                subject = 'Order deleted'
                content = 'Your order was deleted'
                message = Message.objects.create(sender=sender, receiver=receiver, msg_subject=subject, msg_content=content)
                message.save()
        if request.user.is_staff:
            return redirect('order_manage')
        return redirect('orders')
    return render(request, 'orders/order_confirm_delete.html', {'session': request.session, 'order': order})

def order_update(request, pk):
    """
    Get every order associated with the current user and the order to be updated.
    If the order is in the user orders, update, save and redirect to the list of orders.
    If the user is staff, send a message to the user that ordered the order.
    """
    print("Update")
    if request.method == 'POST':
        orders = Order.objects.filter(user=User.objects.get(id=request.user.id))
        order = Order.objects.get(id=pk)
        before_update = ''
        after_update = ''
        if order in orders or request.user.is_staff:
            if request.POST['send'] == 'Update restaurant':
                before_update = order.restaurant
                after_update = request.POST['restaurant']
                order.restaurant = request.POST['restaurant']
            elif request.POST['send'] == 'Update date and time':
                before_update = order.datetime
                after_update = request.POST['datetime']
                order.datetime = request.POST['datetime']
            order.save()
            if request.user.is_staff:
                sender = User.objects.get(username=request.user.username)
                receiver = order.user
                subject = 'Order updated'
                content = 'Before change: ' + str(before_update) + ', after change: ' + str(after_update)
                message = Message.objects.create(sender=sender, receiver=receiver, msg_subject=subject, msg_content=content)
                message.save()
        if request.user.is_staff:
            return redirect('order_manage')
        return redirect('orders')
    return render(request, 'orders/order_update.html', {'session': request.session})

def manage_orders(request):
    """
    If the user is not staff, redirect to home.
    If the request method is GET, render the template with every order.
    If POST render only with the selected restaurant.
    """
    print("Manage")
    if not request.user.is_staff:
        return redirect('home')
    if request.method == 'POST':
        restaurant_name = request.POST.get('restaurant')
        if restaurant_name == 'All':
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(restaurant=restaurant_name)
        return render(request, 'orders/manage_orders.html', {'session': request.session, 'all_orders': all_orders(orders), 'restaurant': restaurant_name})
    return render(request, 'orders/manage_orders.html', {'session': request.session, 'all_orders': all_orders(Order.objects.all()), 'restaurant': 'All'})
