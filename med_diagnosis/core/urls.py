from django.urls import path
from .views import record_symptoms, doctor_observations, lab_results, home, register, logout, login, profile_view
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import RedirectView


urlpatterns = [
    path('', RedirectView.as_view(url='/login/', permanent=False)),
    path('record_symptoms/', record_symptoms, name='record_symptoms'),
    path('doctor_observations/<int:diagnosis_id>/', doctor_observations, name='doctor_observations'),
    path('lab_results/<int:diagnosis_id>/', lab_results, name='lab_results'),
    path('register/', register, name='registration'),
    path('login/', login, name='login'),
    path('profile/', profile_view, name='profile'),
    #path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', logout, name='logout'),
    #path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]