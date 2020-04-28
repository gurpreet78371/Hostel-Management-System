from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from user.models import Profile
import datetime


hostels = (
	('shivalik', 'Shivalik Hostel'),
	('aravali', 'Aravali Hostel'),
	('himalaya', 'Himalaya Hostel'),
	('kurukshetra', "Kurukshetra Hostel"),
	('vindhya', 'Vindhya Hostel'),
	('kalpana', 'Kalpana Hostel'),
)

isChandigarhQuota = (
	('yes', 'Yes'),
	('no', 'No')
)

months = (
	('january', 'january'),
	('february', 'february'),
	('march', 'march'),
	('april', 'april'),
	('may', 'may'),
	('june', 'june'),
	('july', 'july'),
	('august', 'august'),
	('semptember', 'semptember'),
	('october', 'october'),
	('november', 'november'),
	('december', 'december'),
)


class notification(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	document = models.FileField(upload_to='documents/', null=True)
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, default=User, on_delete=models.CASCADE, null=True)

	def __str__(self):
		return self.title


def validate_digit_length(sid):
	if not ((str(sid)).isdigit() and len(str(sid)) == 8):
		raise ValidationError('sid must be 8 digit long ', params={'sid': sid}, )


class hostelApplication(models.Model):
	hostelName = models.CharField(verbose_name='Select Hostel', max_length=20, choices=hostels, default='shivalik')
	sid = models.IntegerField(verbose_name='Student ID', validators=[validate_digit_length])
	studentName = models.CharField(max_length=20, default='gurpreet singh')
	city = models.CharField(max_length=50, default='chandigarh')
	dateApplied = models.DateTimeField(default=timezone.now)
	isChandigarhQuota = models.CharField(verbose_name='Do you have chandigarh quota?', max_length=3, choices=isChandigarhQuota, default='y')
	antiRaggingAffidavit = models.FileField(verbose_name='Anti Ragging Affidavit', upload_to='documents/')
	noVehicleAffidavit = models.FileField(verbose_name='No Vehicle Affidavit', upload_to='documents/')

	def __str__(self):
		return self.hostelName


class messFee(models.Model):
	User = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile')
	hostelName = models.CharField(verbose_name='Select Hostel', max_length=20, choices=hostels, default='shivalik')
	month = models.CharField(max_length=10,verbose_name='Month', choices=months, blank=True)
	regularFee = models.IntegerField(verbose_name='Regular Fee', default=1500)
	extraFee = models.IntegerField(verbose_name='Extra', default=0)
	discount = models.IntegerField(verbose_name='Discount', default=0)
	Total = models.IntegerField(default=1500)
	status = models.BooleanField(default=False)

	def __str__(self):
		return self.User.user.username


class FeeQuery(models.Model):
	SID = models.IntegerField(verbose_name='Enter Student ID', blank=True)
	month = models.CharField(max_length=10,verbose_name='Enter month you want to check for', choices=months, blank=True)
	hostelName = models.CharField(verbose_name='Select Hostel', max_length=20, choices=hostels, default='shivalik',blank=True)

	def __str__(self):
		return self.SID
