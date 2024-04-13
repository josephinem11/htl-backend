from django.urls import path
from .views import start_timer_view, end_timer_view, calculate_score_view

urlpatterns = [
    path('start/', start_timer_view, name='start_timer_view'),
    path('end/', end_timer_view, name='end_timer_view'),
    path('score/', calculate_score_view, name='calculate_score_view')
]

