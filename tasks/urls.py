from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),

    path('', views.homePage, name="home"),
    path('ulist/', views.userList, name="ulist"),
    path('create_task', views.createTask, name="create_task"),
    path('update_task/<str:pk>', views.updateTask, name="update_task"),
    path('delete/<str:pk>', views.deleteTask, name="delete"),
    path('view_task/<str:pk>', views.viewTask, name="view_task"),
]
