from django import forms
from .models import Election, Candidate, Vote
from django.core.exceptions import ValidationError
from django.utils import timezone

class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = ['title', 'description', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if start_date >= end_date:
                raise ValidationError("End date must be after start date.")
            
            if start_date < timezone.now():
                raise ValidationError("Start date cannot be in the past.")

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['name', 'bio', 'photo']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ['candidate']
        widgets = {
            'candidate': forms.RadioSelect()
        }

    def __init__(self, *args, **kwargs):
        self.election = kwargs.pop('election', None)
        self.voter = kwargs.pop('voter', None)
        super().__init__(*args, **kwargs)
        if self.election:
            self.fields['candidate'].queryset = Candidate.objects.filter(election=self.election)
            self.fields['candidate'].empty_label = None
            self.fields['candidate'].label = 'Select a candidate'
        else:
            self.fields['candidate'].queryset = Candidate.objects.none()

    def clean_candidate(self):
        candidate = self.cleaned_data.get('candidate')
        if candidate and self.election:
            if candidate.election != self.election:
                raise forms.ValidationError("Invalid candidate for this election.")
        return candidate

    def clean(self):
        cleaned_data = super().clean()
        if self.election:
            self.instance.election = self.election
        if self.voter:
            self.instance.voter = self.voter
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.election:
            instance.election = self.election
        if self.voter:
            instance.voter = self.voter
        if commit:
            instance.save()
        return instance 