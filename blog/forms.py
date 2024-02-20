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
        fields = ['username', 'email', 'first_name', 'last_name', 'city', 'country', 'dob','mobile_number','avatar']


class LoginForm(AuthenticationForm):
    print('U=I am here')
    class Meta:
        model = User


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['email','mobile_number','dob','city','country', 'avatar']
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author' ,'text' ]


class EmailOrUsernameAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=254)
