# safety/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('equipment/', views.equipment_list, name='equipment_list'),
    # 아래 줄을 새로 추가합니다.
    path('equipment/<int:pk>/', views.equipment_detail, name='equipment_detail'),
]

urlpatterns = [
    path('equipment/', views.equipment_list, name='equipment_list'),
    path('equipment/<int:pk>/', views.equipment_detail, name='equipment_detail'),
    path('equipment/<int:pk>/submit/', views.submit_checklist, name='submit_checklist'),
    path('signup/', views.signup, name='signup'),
    path('log/<int:pk>/delete/', views.delete_log, name='delete_log'),
    path('qr_codes/', views.qr_code_list, name='qr_code_list'),
]