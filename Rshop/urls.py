from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('mainapp.urls')),
    path('products/', include('products.urls')),

    path('accounts/', include('authentication.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    path('cart/', include('cart.urls')),        # ✅ ADD THIS
    path('orders/', include('orders.urls')),    # ✅ if you need orders
    path('', include('payments.urls')),         # ✅ if you need payments
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
