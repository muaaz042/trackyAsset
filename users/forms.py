from django import forms
from .models import User

class CustomUserCreationForm(forms.ModelForm):
    # We explicitly define the fields here so there is no "magic" involved
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role', 'tenant', 'assigned_building')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data

    def save(self, commit=True):
        # Save the user but don't commit to DB yet
        user = super().save(commit=False)
        # Manually hash and set the password
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'