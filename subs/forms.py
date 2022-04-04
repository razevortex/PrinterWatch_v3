from django import forms

class addIP_text(forms.Form):
    enter_IP = forms.CharField()

class addIP_file(forms.Form):
    text_IP = forms.FileField()
