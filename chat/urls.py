from django.urls import path
from .views import UserView,UserDetails,ChatView

urlpatterns = [
    path('users/',UserView.as_view()),
    path('userdetails/<str:name>',UserDetails.as_view()),
    path('chat/',ChatView.as_view())
]