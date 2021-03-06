from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager
from .managers import CustomManager
from django.utils import timezone
from phone_field import PhoneField
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True)
    DOB = models.DateField(blank=True,null=True)
    email = models.EmailField(null=True, blank=True)
    first_name = models.CharField(max_length=100,null=True, blank=True)
    last_name = models.CharField(max_length=100,null=True, blank=True)
    is_Doctor = models.BooleanField(default=False)
    is_Patient = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_hospital_staff=models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    # profile_pic = models.ImageField(
    #     upload_to="uploads/%Y/%m/%d/", null=True, blank=True
    # )
    profile_pic=models.TextField(null=True,blank=True)
    contact_no = PhoneField(blank=True, help_text = 'Contact phone number',null=True)


    objects = CustomManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []
    


class Doctor(models.Model):
    username = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=False)
    Degrees = (
        ("MBBS", "MBBS"),
        ("BDS", "BDS"),
        ("BHMS", "BHMS"),
        ("DHMS", "DHMS"),
        ("BAMS", "BAMS"),
        ("BUMS", "BUMS"),
        ("BVSc & AH", "BVSc & AH"),
        ("B.Pharm.", "B.Pharm."),
        ("D.Pharm.", "D.Pharm."),
        ("BOT", "BOT"),
        ("BMLT", "BMLT"),
        ("BPT", "BPT"),
        ("B.Sc. Nursing", "B.Sc. Nursing"),
        ("BNYS", "BNYS"),
    )
    Postgrad = (
        ("None", "None"),
        ("MD", "MD"),
        ("MS", "MS"),
        ("Diploma", "Diploma"),
    )

    Specialization = (
        ("None", "None"),
        ("DM", "DM"),
        ("MCh", "MCh"),
    )
    doctor_id = models.AutoField(primary_key=True)
    qualification = models.CharField(max_length=50, choices=Degrees, default="MBBS")
    postgrad = models.CharField(
        max_length=50, choices=Postgrad, default=None, null=True
    )
    speciality = models.CharField(
        max_length=50, choices=Specialization, default=None, null=True
    )
    daily_start_time=models.TimeField(null=True,blank=True)
    daily_end_time=models.TimeField(null=True,blank=True)
    description=models.TextField(blank=True,null=True)

    def __str__(self):
        main=""
        if self.username.first_name != None and self.username.last_name != None:
            main=self.username.first_name +self.username.last_name
        else:
            main=self.username.username

        # print(self.username.first_name)
        return (main) 


class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    username = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
     # doc under which patient is working
    conditions=models.CharField(max_length=200,blank=True,null=True)
    history=models.CharField(max_length=200,blank=True,null=True)
    def __str__(self):
        main=""
        if self.username.first_name != None and self.username.last_name != None:
            main=self.username.first_name +self.username.last_name
        else:
            main=self.username.username

        # print(self.username.first_name)
        return (main) 


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, related_name="doc", on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    type_of = models.CharField(max_length=50)  # not sure what is this
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    

    def __str__(self):
        return 'Patient='+str(self.patient.username.username)+' '+'Doctor='+ str(self.doctor.username.username)+'Type-of'+ str(self.type_of)


class Report(models.Model):
    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE
    )  # the patient to whom this report belongs
    typeof = models.CharField(
        max_length=50
    )  # x-ray, blood, etc. Maybe make it dropdown in future?
    published_on = models.DateField()
    appointment = models.ForeignKey(Appointment,on_delete=models.CASCADE,null=True,blank=True)
    filelocation = models.FileField(upload_to="uploads/%Y/%m/%d/")


class Receipt(models.Model):
    filelocation = models.FileField(upload_to="uploads/%Y/%m/%d/",null=True,blank=True)
    appointment = models.ForeignKey(Appointment,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    price = models.IntegerField()


class DailyDoctorQueue(models.Model):

    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    
    token = models.IntegerField()
    present=models.BooleanField(default=False)

