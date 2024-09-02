from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('add/', views.add_product, name='add_product'),
    path('products/', views.product_list, name='product_list'), 
    path('product_details/<int:id>/', views.product_details, name='product_details'), 
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    