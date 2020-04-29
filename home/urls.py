from django.urls import path
from . import views
from user import views as user_views

urlpatterns = [
    path('', views.home, name="web-home"),
    path('about/', views.about, name="web-about"),
    path('users/notification/<int:id>/', views.noti, name="notification"),
    path('users/noti_form/<content>/', views.noti_upload, name="noti_upload"),
    path('users/application-for-hostel/', views.CreateMyModelView.as_view(), name='application-for-hostel'),
    path('users/postComplaint/', user_views.CreateComplaintView.as_view(), name='postComplaint'),
    path('users/post_announcement/', views.upload, name="upload"),
    path('users/application-for-hostel/success/', views.success, name='success'),
    path('users/postComplaint/complaintSuccess/', views.success, name='complaintSuccess'),
    path('users/fee/', views.CreateFeeQueryView, name='fee'),
    path('users/fee/updateFee/', views.updateFeeView, name='updateFee'),
    path('users/', views.users, name="users"),
    path('messFee', views.payment, name="payment"),

]
