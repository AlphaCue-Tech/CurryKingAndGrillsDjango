from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3

class OrderForm(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV3)