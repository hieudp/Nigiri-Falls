from django.shortcuts import render, redirect
from django.http.response import JsonResponse
from .models import Dish, Categori

def index(request):
    """
    Renders the main page so you get dishes, categories and if you are authenticated
    """

    if 'cartAmount' not in request.session:
        request.session['cartAmount'] = 0

    categories = Categori.objects.all()
    if 'categories' not in request.session:
        request.session['categories'] = "All"

    dishes = Dish.objects.all()
    if 'dishes' not in request.session:
        request.session['dishes'] = {}
        for dish in dishes:
            request.session['dishes'][dish.name] = (0, dish.price, dish.image, dish.enabled)

    if request.method == "POST":
        name = request.POST['dish']
        dish = Dish.objects.get(name=name)
        dish.enabled = not dish.enabled
        dish.save()
    
    #Forløkke for å fjerne retter fra handlekurven som er utilgjengelige
    for dishe in request.session['dishes']:
        for dish in dishes:
            if dish.name == dishe and dish.enabled == False:
                request.session['cartAmount'] -= request.session['dishes'][dishe][0]
                request.session['dishes'][dishe] = list(request.session['dishes'][dishe])
                request.session['dishes'][dishe][0] = 0
                request.session['dishes'][dishe] = tuple(request.session['dishes'][dishe])
    return render(request, 'home/index.html', {'dishes': dishes, 'categories': list(categories), 'session': request.session})

def about(request):
    """
    Renders the about page
    """
    return render(request, 'home/about.html', {'session': request.session})

def increase(request):
    """
    Get the dish name from the AJAX call and increase the amount for the dish.
    Send a JsonResponse with the total price, to update it on cart.
    """
    name = request.GET.get('dish')
    request.session['dishes'][name][0] += 1
    request.session['cartAmount'] += 1
    
    #Regner ut pris
    total_price = 0
    for value in request.session['dishes'].values():
        total_price += value[1] * value[0]
    return JsonResponse({'total_price': total_price})

def decrease(request):
    """
    Get the dish name from the AJAX call and decrease the amount for the dish.
    Send a JsonResponse with the total price, to update it on cart.
    """
    name = request.GET.get('dish')
    if request.session['dishes'][name][0] > 0:
        request.session['dishes'][name][0] -= 1
        request.session['cartAmount'] -= 1
        
    #Regner ut pris    
    total_price = 0
    for value in request.session['dishes'].values():
        total_price += value[1] * value[0]
    return JsonResponse({'total_price': total_price})

def set_categori(request):
    """
    Get the categori_name from the AJAX call and update the session variable.
    Retrieve all dishes, the dishes related to the categori and all categories, and convert them into lists of names.
    Send these back to the template as a JsonResponse and update the page.
    """
    categori_name = request.GET.get('categori')
    request.session['categories'] = categori_name
    show_dishes = Categori.objects.get(name=categori_name).dishes.all()
    show_dishes = list(map(lambda dish: dish.name, show_dishes))
    all_dishes = Dish.objects.all()
    all_dishes = list(map(lambda dish: dish.name, all_dishes))
    all_categories = Categori.objects.all()
    all_categories = list(map(lambda categori: categori.name, all_categories))
    return JsonResponse({'show_dishes': show_dishes, 'all_dishes': all_dishes, 'all_categories': all_categories})