import datetime
import pytz
from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField




class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    website =  models.URLField(max_length=255, blank=True, null=True)
    location =  models.CharField(max_length=100, blank=True, null=True)
    description = HTMLField(null=True, blank=True)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ['name']

    def __str__(self):
        return self.name



class Position(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Position"
        verbose_name_plural = "Positions"
        ordering = ['title']

    def __str__(self):
        return self.title

class Status(models.Model):
    STATUS_CHOICES = [
        ('a', 'Applied'),
        ('i', 'Interview'),
        ('o', 'Offer'),
        ('r', 'Rejected'),
        ('ach', 'Achieved'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='a', help_text='Status')

    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"

    def __str__(self):
        return self.status

class JobType(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Job Type"
        verbose_name_plural = "Job Types"
        ordering = ['name']

    def __str__(self):
        return self.name

class JobApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications')
    company = models.ForeignKey('Company', on_delete=models.CASCADE, help_text='Company')
    position = models.CharField('Position', max_length=100, null=True, blank=True ,help_text='Position')
    job_type = models.CharField('Job Type', max_length=100, null=True, blank=True ,help_text='Job type')
    status = models.ForeignKey('Status', on_delete=models.SET_NULL, null=True, blank=True ,help_text='Status')
    job_link = models.URLField(max_length=255, blank=True, null=True ,help_text='Job link')
    date_applied = models.DateField(default=datetime.datetime.now ,help_text='Date Applied')
        #automatick CALCULATIONS
    expected_date = models.DateField( default=datetime.date.today() + datetime.timedelta(days=30), help_text='Expected Date' )
    wage = models.PositiveIntegerField(blank=True,null=True,validators=[MinValueValidator(0)],help_text='Monthly salary')
    notes = HTMLField(null=True, blank=True,help_text='Notes about job application')

    class Meta:
        verbose_name = "Job Application"
        verbose_name_plural = "Job Applications"
        ordering = ['-date_applied']


    def get_queryset(self):
        return JobApplication.objects.filter(reader=self.request.user).filter(status__exact='a').order_by('due_back')

    utc = pytz.UTC
    @property
    def due_back(self):
        if self.expected_date and datetime.today().replace(tzinfo=self.utc) > self.date_applied.replace(tzinfo=self.utc):
            return True
        return False

    def __str__(self):
        return f"{self.user} - {self.position.title} at {self.company.name}"
