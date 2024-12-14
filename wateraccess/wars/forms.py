from django import forms
from .models import Province, District, Sector, Cell, Village,ContactMessage, warsUser,userProfile

# Form for User Registration
class RegistrationForm(forms.Form):
    names = forms.CharField(max_length=255, required=True, label='Names')
    email = forms.EmailField(max_length=255, required=True, label='Email')
    phone = forms.CharField(max_length=15, required=True, label='Phone Number')
    nationalId = forms.CharField(max_length=16, required=True, label='National ID/Passport No')
    dob = forms.DateField(required=True, label='Date of Birth')
    gender= forms.ChoiceField(choices=userProfile.GENDER_CHOICES, required=True, label='Gender')
    nationality= forms.ChoiceField(choices=userProfile.NATIONALITY_CHOICES, required=True, label='Nationality')
    emergencyContact= forms.CharField(max_length=15, required=True, label='Emergency Contact')
    country = forms.CharField(max_length=100, required=True, label='Country')
    province = forms.CharField(max_length=100, required=True, label='Province')
    district = forms.CharField(max_length=100, required=True, label='District')
    sector = forms.CharField(max_length=100, required=True, label='Sector')
    cell = forms.CharField(max_length=100, required=False, label='Cell')
    village = forms.CharField(max_length=100, required=False, label='Village')
    profile_pic = forms.ImageField(required=True, label='Profile_picture')
    role = forms.ChoiceField(choices=userProfile.ROLE_CHOICES, required=True, label='Role')

    def clean_email(self):
        email = self.cleaned_data['email']
        if warsUser.objects.filter(email=email).exists():
            raise ValidationError('Email already exists. Please use a different email.')
        return email

    # Location Information
    country = forms.ChoiceField(choices=[('Rwanda', 'Rwanda')], widget=forms.Select(attrs={'placeholder': 'Select your country'}))
    province = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'placeholder': 'Select Province'}))
    district = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'placeholder': 'Select District'}))
    sector = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'placeholder': 'Select Sector'}))
    cell = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'placeholder': 'Select Cell'}))
    village = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'placeholder': 'Select Village'}))

    # Profile Picture
    profile_pic = forms.ImageField(required=True, widget=forms.ClearableFileInput(attrs={'accept': 'image/*'}))

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

    # Example of custom validation if required
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Add custom phone validation if needed
        return phone

    def clean_emergencyContact(self):
        emergency_contact = self.cleaned_data.get('emergencyContact')
        # Add custom validation for emergency contact
        return emergency_contact

#ContactMessageForm

class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['names', 'phone', 'email', 'message', 'file']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your names'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Write your message here...'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }


# Forms for user registration data

class ProvinceForm(forms.ModelForm):
    class Meta:
        model = Province
        fields = '__all__'

class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = '__all__'

class SectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = '__all__'

class CellForm(forms.ModelForm):
    class Meta:
        model = Cell
        fields = '__all__'

class VillageForm(forms.ModelForm):
    class Meta:
        model = Village
        fields = '__all__'
