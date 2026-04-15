from django.urls import path
from .views import profile_view, profile_edit

urlpatterns = [
    path('', profile_view),
    path('edit/', profile_edit, name='profile_edit'),
]