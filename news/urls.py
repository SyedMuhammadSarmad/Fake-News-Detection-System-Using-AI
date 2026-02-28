from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('analyze/',   views.analyze,   name='analyze'),
    path('history/',   views.history,   name='history'),
    path('export/',    views.export_csv, name='export_csv'),
]
