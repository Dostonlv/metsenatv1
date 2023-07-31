from django.db import models

class Sponsor(models.Model):
    STATUS = (
        ('new', 'Yangi'),
        ('processing', 'Moderatsiyada'),
        ('approved', 'Tasdiqlangan'),
        ('canceled', 'Bekor qilingan')
    )
    INDIVIDUALITY = (
        ('physical', 'Jismoniy shaxs'),
        ('legalentity', 'Yuridik shaxs')
    )
    full_name = models.CharField(max_length=128, null=True)
    phone_number = models.CharField(max_length=13, null=True)
    amount = models.BigIntegerField(null=False, blank=False)
    person_type = models.CharField(max_length=16, choices=INDIVIDUALITY, null=True)
    company_name = models.CharField(max_length=256, null=True, blank=True)
    status = models.CharField(max_length=64, choices=STATUS, default='new')
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.full_name 


class University(models.Model):
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'University'
        verbose_name_plural = 'Universities'


class Student(models.Model):
    DEGREE = (
        ('bachelor', 'Bakalavr'),
        ('master', 'Magistr')
    )
    full_name = models.CharField(max_length=200, null=True)
    phone_number = models.CharField(max_length=13, null=True)
    university = models.ForeignKey(University, related_name='students', on_delete=models.SET_NULL, null=True)
    degree = models.CharField(max_length=64, choices=DEGREE, null=True)
    tution_fee = models.BigIntegerField(null=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.full_name 

class Sponsorship(models.Model):
    sponsor = models.ForeignKey(Sponsor, related_name='sponsorships', on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey(Student, related_name='sponsorships', on_delete=models.CASCADE, null=True)
    amount = models.BigIntegerField(null=True)
    date_created = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.sponsor.full_name

    class Meta:
        verbose_name = 'Sponsorship'
        verbose_name_plural = 'Sponsorships'
