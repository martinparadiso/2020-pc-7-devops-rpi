from django.urls import path

from . import views

app_name = 'dashboard'
urlpatterns = [
    # ex: /dashboard/
    path('', views.index, name='index'),
    # ex: /dashboard/23/
    path('<int:pk>', views.detail, name='detail'),
    # ex: /dashboard/23/edit
    path('<int:pk>/edit', views.edit, name='edit'),
    # ex: /dashboard/23/change_version/
    path('<int:pk>/change_version', views.change_version, name='change_version'),
]
