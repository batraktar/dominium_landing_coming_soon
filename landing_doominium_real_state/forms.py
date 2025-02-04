from django import forms
from phonenumber_field.formfields import PhoneNumberField


class ConsultationForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    phone = PhoneNumberField(
        region="UA",  # Вказуємо Україну (або іншу країну за замовчуванням)
        required=True,
        error_messages={'invalid': "Введіть коректний номер телефону."},
    )
    subject = forms.CharField(max_length=255, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
