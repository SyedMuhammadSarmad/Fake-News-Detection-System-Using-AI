from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/',    views.dashboard,    name='dashboard'),
    path('analyze/',      views.analyze,      name='analyze'),
    path('history/',      views.history,      name='history'),
    path('export/',       views.export_csv,   name='export_csv'),
    path('export/pdf/',   views.export_pdf,   name='export_pdf'),
    path('export/excel/', views.export_excel, name='export_excel'),
]
