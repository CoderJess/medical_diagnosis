from django.contrib import admin
from .models import UserProfile, Disease, DiagnosisHistory, DoctorObservation, LabResult

admin.site.register(UserProfile)
admin.site.register(Disease)
admin.site.register(DiagnosisHistory)
admin.site.register(DoctorObservation)
admin.site.register(LabResult)