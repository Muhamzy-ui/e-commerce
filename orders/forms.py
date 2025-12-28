from django import forms

class CheckoutForm(forms.Form):
    full_name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=50, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    state = forms.CharField(max_length=100, required=True)
    payment_method = forms.ChoiceField(choices=[
        ("paystack", "Paystack (Card / Bank)"),
        ("pod", "Pay on Delivery"),
        ("bank", "Bank Transfer"),
    ], widget=forms.RadioSelect)
