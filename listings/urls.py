from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('add/', views.add_product, name='add_product'),
    path('products/', views.product_list, name='product_list'),
    path('my-listings/', views.product_list, name='my_listings'), 
    path('product_details/<int:id>/', views.product_details, name='product_details'),
    path('upload/', views.file_upload, name='file_upload'),
    path('edit/<int:id>/', views.edit_listing, name='edit_listing'),
    path('delete/<int:id>/', views.delete_listing, name='delete_listing'),
    path('remove-image/', views.remove_image, name='remove_image'),  
    path('update-photo-order/', views.update_photo_order, name='update_photo_order'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)