from django import forms
from .models import RiskAssessment

class GeneralInfoForm(forms.ModelForm):
    class Meta:
        model = RiskAssessment
        fields = ['field1', 'field2']

class RiskDetailsForm(forms.ModelForm):
    class Meta:
        model = RiskAssessment
        fields = ['field3', 'field4']

class ImpactForm(forms.ModelForm):
    class Meta:
        model = RiskAssessment
        fields = ['field5', 'field6']

class RecommendationsForm(forms.ModelForm):
    class Meta:
        model = RiskAssessment
        fields = ['field7', 'field8']
