from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as ad
urlpatterns = [
  path('',views.home,name="home"),
  path('login/',ad.LoginView.as_view(template_name="html/login.html"),name="login"),
  path('lgot/',ad.LogoutView.as_view(template_name="html/logout.html"),name="lgt"),
  path('signup/',views.register,name="signup"),
  path('helpdesk/',views.help,name="hl"),
  path('services/',views.book,name="services"),
  path('servicedet/',views.details,name="det"),
  path('usrlst/',views.userlist,name="usrl"),
  path('usrdel/<int:d>/',views.userdelete,name="usd"),
  path('updateprofile/',views.update_profile,name="update_profile"),
  path('pfle/',views.profile,name="pf"),
  path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
  path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
  path('view_cart/', views.view_cart, name='view_cart'),
  path('checkout/',views.checkout,name="checkout"),
  path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
  path('order_history/<int:user_id>/', views.order_history, name='order_history'),
  path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
  path('service_requests/',service_requests,name='service_requests'),
  path('add_services/', views.add_services, name='add_services'),
  path('acservices/',views.ac_services,name="acservices"),
  path('eleservices/',views.eletrical_service,name="ele"),
  path('CarpenterServices/',views.carpenter_service,name="carp"),
  path('approval/',views.service_form,name='approval'),
  path('pending_submissions/', views.pending_submissions, name='pending_submissions'),
  path('approve_service/<int:service_id>/', views.approve_service, name='approve_service'),
  path('approved_service_providers/<int:order_id>/',views.approved_service_providers,name="approvedproviders"),
  path('allocate_order/<int:order_id>/', views.allocate_order, name="allocate_order"),
  path('bookings/<int:user_id>/',views.bookings,name="bookings"),
  path('rar/',views.review_rating,name ='rar'),
  path('unallocate_order/<int:order_id>/', views.unallocate_order, name='unallocate_order'),
  
    
]
