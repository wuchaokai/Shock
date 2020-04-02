from django.urls import path
from . import views
urlpatterns=[
    path('',views.IndexView.as_view(),name='index'),
    path('info/',views.acceptInfo,name='info'),
    path('detail/<int:code>',views.detailInfo,name='detail'),
    path('login/',views.loginInfo,name='login'),
    path('loginout/',views.loginexit,name='loginexit'),
    path('trade/<str:code>',views.sell_or_buy,name='trade'),
    path('individualInfo/',views.individual,name='individual'),
    path('register/',views.RegisterView.as_view(),name='register'),
    path('state/',views.createAccount,name='createAccount')
]