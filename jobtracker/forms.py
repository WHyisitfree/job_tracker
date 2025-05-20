from django import forms

from .models import JobApplication, Company, Status


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = [
            'company',
            'position',
            'job_type',
            'status',
            'job_link',
            'date_applied',
            'expected_date',
            'wage',
            'notes',
        ]
        widgets = {
            'position': forms.TextInput(attrs={'position': 'position'}  ),
            'job_type': forms.TextInput(attrs={'job_type': 'job_type'}),
            'job_link': forms.URLInput(attrs={'job_link': 'job_link'}),
            'wage': forms.NumberInput(attrs={'wage': 'wage'}),
            'notes': forms.Textarea(attrs={ 'notes': 'notes'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            # filter company choices to current user companies
            self.fields['company'].queryset = Company.objects.filter(user=user)


class CompanyForm(forms.ModelForm):
        class Meta:
            model = Company
            fields = [
                'name',
                'email',
                'phone_number',
                'website',
                'location',
                'description',
            ]
            widgets = {
                'name': forms.TextInput(attrs={'name': 'name'}),
                'email': forms.EmailInput(attrs={'email': 'email'}),
                'phone_number': forms.TextInput(attrs={'phone_number': 'phone_number'}),
                'website': forms.TextInput(attrs={'website': 'website'}),
                'location': forms.TextInput(attrs={'location': 'location'}),
                'description': forms.Textarea(attrs={'description': 'description'}),
            }