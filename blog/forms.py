from django import forms
from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm ,UserChangeForm
from .models import Post ,User,Comment
from django.core.validators import RegexValidator

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text','category','tags','thumbnail','feature_image')

class UserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = '__all__'


class SignUpForm(UserCreationForm):
    dob = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    mobile_number = forms.IntegerField(
        validators=[
            RegexValidator(
                regex='^\d+$',
                message='Mobile number must contain only numeric digits.',
                code='invalid_mobile_number'
            )
        ],
        required=False
    )    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'city', 'country', 'dob','mobile_number']


class LoginForm(AuthenticationForm):
    class Meta:
        model = User


class EditProfileForm(UserChangeForm):

    email = forms.EmailField(required=True)
    mobile_number = forms.CharField(max_length=15, required=False)
    dob = forms.DateField()
    city =forms.CharField(max_length=15, required=True)
    country=forms.CharField(max_length=15, required=True)
    class Meta:
        model = User
        fields = ['email','mobile_number','dob','city','country', 'avatar']
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text' ]


