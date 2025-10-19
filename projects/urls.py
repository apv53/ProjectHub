from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('projects/', views.project_list, name='project_list'),
    path('create/', views.project_create, name='project_create'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
    path('<int:pk>/delete/', views.project_delete, name='project_delete'),
    path('<int:pk>/vote/', views.project_vote, name='project_vote'),

    # Comments
    path('<int:pk>/comment/add/', views.add_comment, name='add_comment'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),

    # Auth
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
]

