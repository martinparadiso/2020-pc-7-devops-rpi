from django.urls import path

from . import views

app_name = 'dashboard'
urlpatterns = [
    # ex: /dashboard/
    path('', views.index, name='index'),
    # ex: /dashboard/23/edit
    path('add', views.add, name='add'),
    # ex: /dashboard/23/
    path('<int:pk>', views.detail, name='detail'),
    # ex: /dashboard/23/edit
    path('<int:pk>/edit', views.edit, name='edit'),
    # ex: /dashboard/23/remove
    path('<int:pk>/remove', views.remove, name='remove'),
    # ex: /dashboard/23/change_version/
    path('<int:pk>/change_version', views.change_version, name='change_version'),
    # ex: /dashboard/23/force_update/
    path('<int:pk>/force_update', views.force_update, name='force_update'),
    # ex: /dashboard/new_version
    path('new_version/<str:version>', views.new_version, name='new_version'),
    # ex: /dashboard/login
    path('login/', views.login_view, name='login'),
    # ex: /dashboard/logout
    path('logout/', views.log_out, name='logout'),
    # ex: /dashboard/register
    path('register/', views.register_view, name='register'),
]
