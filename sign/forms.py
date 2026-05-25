from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            "email",
            "password1",
            "password2",
        )

class CodeForm(forms.Form):
    code = forms.CharField(required=True,max_length=6, label='', widget=forms.TextInput(attrs={'placeholder': 'Введите код'}))

    def clean_code(self):
        code = self.cleaned_data['code']
        if not code.isdigit() or len(code) != 6:
            raise forms.ValidationError("Код должен состоять из 6 цифр.")
        return code