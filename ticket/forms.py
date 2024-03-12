from django import forms
#from .views import value
class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(max_length = 100, label = "Enter Current Password", widget=forms.PasswordInput)
    new_password = forms.CharField(max_length = 100, label = "Enter New Password", widget=forms.PasswordInput)
    re_password = forms.CharField(max_length = 100, label = "Re-Enter New Password", widget=forms.PasswordInput)

class EditForm(forms.Form):
    Value = forms.CharField(max_length = 1000)

