from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('<int:product_id>/payment_form/', views.payment_form, name='payment_form'),
    path('<int:product_id>/process_payment/', views.process_payment, name='process_payment'),
    path('<int:product_id>/payment_success/', views.payment_success, name='payment_success'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    