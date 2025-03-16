from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    USER_TYPE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('lab_tech', 'Lab Technician'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

class Disease(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    symptoms = models.TextField()
    treatment = models.TextField()
    doctor_observations = models.TextField()
    lab_results = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class DiagnosisHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    symptoms = models.TextField()  # Patient input history
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, null=True, blank=True)
    date_diagnosed = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.disease.name if self.disease else 'Pending'} on {self.date_diagnosed}"

class DoctorObservation(models.Model):
    diagnosis_history = models.ForeignKey(DiagnosisHistory, on_delete=models.CASCADE)
    observation = models.TextField()

    def __str__(self):
        return f"Observation for {self.diagnosis_history.user.username}"

class LabResult(models.Model):
    diagnosis_history = models.ForeignKey(DiagnosisHistory, on_delete=models.CASCADE)
    result = models.TextField()

    def __str__(self):
        return f"Lab Result for {self.diagnosis_history.user.username}"