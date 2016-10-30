from django import forms


class MessageForm(forms.Form):
    to = forms.CharField()
    msisdn = forms.CharField()
    messageId = forms.CharField()
    timestamp = forms.CharField()
    text = forms.CharField()
    type = forms.CharField()
