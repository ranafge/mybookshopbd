from django import forms
from . import models

PAYMENT_CHOICES = (
    ('C', 'Cash on delivery'),
    ('BKH', 'Bkash'),
    ('RCT', 'Rocket')
)


class CheckoutForm(forms.Form):
    full_name = forms.CharField(label='Your name', max_length=50,
                                widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control', }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    phone = forms.CharField(label='Your phone', max_length=11,
                            widget=forms.TextInput(attrs={'placeholder': 'Phone', 'class': 'form-control', }))
    another_phone = forms.CharField(label='Your phone', max_length=11,
                                    widget=forms.TextInput(attrs={'placeholder': 'Phone', 'class': 'form-control', }))
    division = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Division', 'class': 'form-control', }))
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Address', 'class': 'form-control', }))
    payment_option = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.Select)
    # total_amount = forms.CharField(max_length=20)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code',
        'arial-label': 'Recipient\'s username',
        'arial-describedby': 'basic-addon2'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4,
    }))
    email = forms.EmailField()


class ContactForm(forms.ModelForm):
    contact_choice_text = forms.ModelChoiceField(queryset=models.SubjectChoice.objects.all(),widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = models.Contact
        fields = ['name','contact_choice_text', 'phone_number', 'email', 'text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder':'Your message here.'}),
            'phone_number': forms.TextInput(attrs={'placeholder':'Your Phone number', 'class': 'form-control'}),
            'email': forms.TextInput(attrs={'placeholder':'Your email here.', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'placeholder':'Your name', 'class': 'form-control'}),
        }


class SearchChoicesForm(forms.ModelForm):
    search_text = forms.ModelChoiceField(queryset=models.SearchChoices.objects.all(),
                                         widget=forms.Select(attrs={'class': 'form-control'}))
