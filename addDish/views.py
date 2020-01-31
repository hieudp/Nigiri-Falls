from django.shortcuts import render, redirect
from home.models import Dish, Categori
from .forms import CategoriForm, DishForm
# Create your views here.


# Legge til retter i databasen og riktig kategori til retten som blir lagt til
def add_dish(request):
        form = DishForm()
        dishes = Dish.objects.all()
        if request.user.is_staff or request.user.is_superuser:
                if request.method == 'POST':
                        form = DishForm(request.POST)
                        if form.is_valid():
                                error = False
                                #if Dish.objects.filter(name= form['name'].value()).exists():
                                        #error = True
                                #elif not len(form['name'].value()) < 100 or not form['name'].value().isalpha():
                                        #error = True
                                #elif not form['name'].value() or not form['image'].value() or not form['categori'].value() or not form['enabled'].value():
                                        #error = True

                                if error:
                                        return render(request, 'addDish/addDish.html', {'form': form, 'error': error, 'session': request.session})

                                form.save()
                                categoriname = form['categori'].value()
                                dishname = form['name'].value()
                                categori = Categori.objects.get(name=categoriname)
                                categoriAll = Categori.objects.get(name='All')
                                dish = Dish.objects.get(name=dishname)
                                categori.dishes.add(dish)
                                categoriAll.dishes.add(dish)
                                request.session['dishes'] = {}
                                for dish in dishes:
                                        request.session['dishes'][dish.name] = (0, dish.price, dish.image, dish.enabled)
                                return redirect('addDish')
        return render(request, 'addDish/addDish.html', {'form': form, 'session': request.session})

# Legge til kategori i databasen
def add_categori(request):
        catform = CategoriForm()
        if request.method == 'POST':
                catform = CategoriForm(request.POST)
                if catform.is_valid():
                        error = False
                        if catform['name'].value().isdigit():
                                error = True
                        if error:
                                return render(request, 'addDish/addCategori.html', {'catform': catform, 'error': error, 'session': request.session})
                        catform.save()
                        return redirect('addDish')
        return render(request, 'addDish/addCategori.html', {'catform': catform, 'session': request.session})
