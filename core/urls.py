from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    # Override login to use our template; include rest of auth urls (logout, password reset, etc.)
    path('accounts/login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('news/', include('news.urls')),
    path('', RedirectView.as_view(url='/accounts/login/', permanent=False)),
]
