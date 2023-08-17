from django import forms
from .models import StudentContact

class StudentContactForm(forms.ModelForm):
    class Meta:
        model = StudentContact
        fields = "__all__"
#
# from django import forms
#
# class NameForm(forms.Form):
#     your_name = forms.CharField(label='Your name', max_length=100)