from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField
from PIL import Image

Departments = [
    ("Aero", "Aerospace"),
    ("Civil", "Civil"),
    ("CSE", "Computer Science"),
    ("ECE", "Electronics & Communication"),
    ("Electrical", "Electrical"),
    ("Mechanical", "Mechanical"),
    ("Metallurgy", "Materials & Metallurgical"),
    ("Production", "Production & Industrial"),
]

complaints = [
    ('Mess', 'Mess'),
    ('Hostel Room', 'Hostel Room'),
    ('Hostel Washroom', 'Hostel Washroom'),
    ('Electricity', 'Electricity'),
    ('Water', 'Water'),
    ('Ragging', 'Ragging'),
    ('Sexual harassment', 'Sexual harassment'),
    ('Other', 'Other'),
]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    StudentID = models.IntegerField(primary_key=True, verbose_name='SID')
    Branch = models.CharField(max_length=255, choices=Departments, default="CSE")
    YearOfStudy = models.IntegerField(default=1)
    ContactNumber = PhoneField(help_text='Contact phone number')
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics', blank=True)
    parentsContactNumber = PhoneField(help_text="Parent's phone number", blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class complaint(models.Model):
    complaintUser = models.ForeignKey(Profile, on_delete=models.CASCADE)
    category = models.CharField(max_length=255, choices=complaints, default='Mess')
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='complaint_pics/', blank=True)

    def __str__(self):
        return self.title
