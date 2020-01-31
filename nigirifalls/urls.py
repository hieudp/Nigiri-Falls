from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('cart/', include('cart.urls')),
    path('login/', include('login.urls')),
    path('orders/', include('orders.urls')),
    path('addDish/', include('addDish.urls')),
    path('account/', include('account.urls')),
    path('message/', include('message.urls')),
]# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
