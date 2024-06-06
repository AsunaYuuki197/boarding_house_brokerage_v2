from django import forms
from django.forms.widgets import DateInput
from django.contrib.auth.forms import UserCreationForm
from .models import *

class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

class SignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Password'
        self.fields['password2'].label = 'Password Confirmation'

        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2' )
        help_texts = {
            'username': None,
        }

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    name.widget.attrs.update({'class': 'form-control'})
    email.widget.attrs.update({'class': 'form-control'})
    message.widget.attrs.update({'class': 'form-control'})


class HouseForm(FormSettings):
    class Meta:
        model = House
        fields = ['name', 'address', 'description', 'price']

# class HouseImageForm(forms.ModelForm):
#     class Meta:
#         model = HouseImage
#         fields = ['image']
#         widgets = {
#             'image': forms.ClearableFileInput(attrs={'multiple': True}),
#         }

class RentalPostForm(FormSettings):
    class Meta:
        model = RentalPost
        fields = ['title', 'total_vacancies', 'available_vacancies']


class VerificationForm(FormSettings):
    class Meta:
        model = Verification
        fields = ['status', 'comments']

class ReviewForm(FormSettings):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

class ReviewReplyForm(FormSettings):
    class Meta:
        model = ReviewReply
        fields = ['comment']

class ReservationForm(FormSettings):
    class Meta:
        model = Reservation
        fields = ['start_date', 'end_date']
        widgets = {'start_date': DateInput(attrs={'type': 'date'}),
                   'end_date': DateInput(attrs={'type': 'date'})
                 }


class PaymentForm(FormSettings):
    class Meta:
        model = Payment
        fields = ['payment_method']

class RefundRequestForm(FormSettings):
    class Meta:
        model = Reservation
        fields = ['refund_status']
        widgets = {
            'refund_status': forms.HiddenInput()
        }