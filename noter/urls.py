from django.urls import path

from . import views

app_name = 'noter'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('notebook/<int:notebook_id>/', views.notebook_view, name = 'notebook'),
    path('note/<int:note_id>/', views.note_view, name = 'note'),
    path('login/', views.login_view, name = 'login'),
    path('logout/', views.logout_view, name = 'logout'),
    path('register/', views.register_view, name = 'register'),
    path('create_notebook/', views.notebook_creation, name = 'notebook_create'),
    path('create_note/<int:notebook_id>/', views.note_creation, name = 'note_create'),
    path('note_delete/<int:note_id>/', views.note_delete, name = 'note_delete'),
    path('notebook_delete/<int:notebook_id>', views.notebook_delete, name = 'notebook_delete'),
    path('notebook_edit/<int:notebook_id>', views.notebook_edit, name = 'notebook_edit'),
    path('user_settings/', views.user_settings, name = 'user_settings'),
    path('access_denied/', views.access_denied, name = 'access_denied')
]
