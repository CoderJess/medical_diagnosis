from django import forms
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    USER_TYPE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('lab_tech', 'Lab Technician'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'user_type']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        if commit:
            user.save()
        return user