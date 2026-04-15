from allauth.account.forms import SignupForm
from django import forms
from .models import CustomUser

class CustomSignupForm(SignupForm):
    birthday = forms.DateField()
    
    def save(self, request):
        user =super().save(request)
        user.birthday = self.cleaned_data.get('birthday')
        user.username = user.username.lower()
        user.email = user.email.lower()
        user.save()
        return user
    
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['image', 'username', 'name', 'bio', 'website']
        widgets = {
            'username' : forms.TextInput(attrs={'class': 'input-field','placeholder': 'Username'}),
            'name' : forms.TextInput(attrs={'class': 'input-field','placeholder': 'Name'}),
            'bio' : forms.Textarea(attrs={'class': 'input-field resize-none','rows':2, 'placeholder': 'Bio', 'maxlength': '250'}),
        }