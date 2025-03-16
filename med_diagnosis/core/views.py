from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import login
from .models import UserProfile
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import DiagnosisHistory, DoctorObservation, LabResult
import requests

def register(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user and get the User instance
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')

            # Create a UserProfile for the new user
            UserProfile.objects.create(user=user)

            return redirect('login')  # Redirect to login page after successful registration

    return render(request, 'registration.html', {'form': form})

@login_required(login_url='login')
def profile_view(request):
    return render(request, 'profile.html')

def home(request):
    return render(request, 'home.html')

@login_required(login_url='login')
def record_symptoms(request):
    if request.method == 'POST':
        symptoms = request.POST.get('symptoms')
        diagnosis_history = DiagnosisHistory.objects.create(user=request.user, symptoms=symptoms)
        return redirect('doctor_observations', diagnosis_history.id)
    return render(request, 'record_symptoms.html')

@login_required(login_url='login')
def doctor_observations(request, diagnosis_id):
    if request.method == 'POST':
        observation = request.POST.get('observation')
        diagnosis_history = DiagnosisHistory.objects.get(id=diagnosis_id)
        DoctorObservation.objects.create(diagnosis_history=diagnosis_history, observation=observation)
        return redirect('lab_results', diagnosis_id)
    return render(request, 'doctor_observations.html')

@login_required(login_url='login')
def lab_results(request, diagnosis_id):
    if request.method == 'POST':
        result = request.POST.get('result')
        diagnosis_history = DiagnosisHistory.objects.get(id=diagnosis_id)
        LabResult.objects.create(diagnosis_history=diagnosis_history, result=result)
        
        response = requests.post('##########', json={
            'symptoms': diagnosis_history.symptoms,
            'observations': diagnosis_history.doctorobservation_set.last().observation,
            'lab_results': diagnosis_history.labresult_set.last().result
        })
        
        final_diagnosis = response.json().get('diagnosis')
        return render(request, 'diagnosis_result.html', {'diagnosis': final_diagnosis})
    
    return render(request, 'lab_results.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('profile')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')
    else:
        return render(request, 'login.html')

@login_required(login_url='login')    
def logout(request):
    auth.logout(request)
    return redirect('login.html')

