from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('projets.urls')),  # Inclut les routes de ton app
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    #path('logout/', views.logout_user, name='logout'),  # ✅ logout ajouté
    #path('suivi/<int:projet_id>/', views.suivi_detail, name='suivi_detail'),

]

