from django import forms
from .models import User



class SignupForm(forms.ModelForm):
    
    # def __init__(self, *args, **kwargs):     #필수필드 커스텀 할때 사용
    #     super().__init__(*args,**kwargs)
    #     self.fields['email'].required = True
    #     self.fields['email'].required = True
    #     self.fields['email'].required = True
    class Meta:
        model = User
        fields = ['username','password']







