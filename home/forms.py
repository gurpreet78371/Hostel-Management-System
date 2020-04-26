from django import forms
from .models import notification, hostelApplication, messFee, FeeQuery


class notification(forms.ModelForm):
	class Meta:
		model = notification
		fields = ('title', 'content', 'document',)


class hostelapplication(forms.ModelForm):
	class Meta:
		model = hostelApplication
		fields = ('hostelName', 'sid','isChandigarhQuota', 'city', 'antiRaggingAffidavit', 'noVehicleAffidavit',)


class messFeeForm(forms.ModelForm):
	class Meta:
		model = messFee
		fields = ('User', 'month', 'regularFee', 'extraFee', 'discount', 'Total',)


class FeeQueryForm(forms.ModelForm):
	class Meta:
		model = FeeQuery
		fields = ('SID', 'month', 'hostelName', )