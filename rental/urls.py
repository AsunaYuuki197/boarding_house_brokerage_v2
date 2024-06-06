from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('house/<int:pk>/', views.house_detail, name='house_detail'),
    path('create_rental_post/', views.create_rental_post, name='create_rental_post'),
    path('verify_post/<int:pk>/', views.verify_post, name='verify_post'),
    path('delete_post/<int:pk>/', views.delete_post, name='delete_post'),
    path('delete_review/<int:pk>/', views.delete_review, name='delete_review'),
    path('reply_review/<int:pk>/', views.reply_review, name='reply_review'),
    path('manage_posts/', views.manage_posts, name='manage_posts'),
    path('manage_reviews/', views.manage_reviews, name='manage_reviews'),
    path('manage_user_posts/', views.manage_user_posts, name='manage_user_posts'),
    path('manage_user_reviews/', views.manage_user_reviews, name='manage_user_reviews'),
    path('customer_care/', views.customer_care, name='customer_care'),
    path('reserve_house/<int:pk>/', views.reserve_house, name='reserve_house'),
    path('payment/<int:pk>/', views.payment, name='payment'),
    path('manage_reservations/', views.manage_reservations, name='manage_reservations'),
    path('manage_user_reservations/', views.manage_user_reservations, name='manage_user_reservations'),
    path('manage_user_rental_reservations/', views.manage_user_rental_reservations, name='manage_user_rental_reservations'),
    path('refund_request/<int:pk>/', views.refund_request, name='refund_request'),
    path('process_refund/<int:pk>/', views.process_refund, name='process_refund'),
    path('delete_reservation/<int:pk>/', views.delete_reservation, name='delete_reservation'),
    path('user_delete_reservation/<int:pk>/', views.user_delete_reservation, name='user_delete_reservation'),

]
