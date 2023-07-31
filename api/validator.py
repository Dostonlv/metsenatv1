from rest_framework.validators import ValidationError
from rest_framework.generics import get_object_or_404
from .models import *
from django.db.models import Sum
from django.db.models.functions import Coalesce



def sponsor_amount_validator_for_update(instance, validated_data):
    sponsor = get_object_or_404(Sponsor, id=validated_data['sponsor_id'])
    student =  instance.student
    amount = validated_data['amount']

    sponsor_spent_amount = \
        sponsor.sponsorships.exclude(id=instance.id).aggregate(amount=Coalesce(Sum('amount'), 0))['amount_sum']
    student_gained_amount = \
        student.sponsorships.exclude(id=instance.id).aggregate(amount=Coalesce(Sum('amount'), 0))['amount_sum']
    sponsor_left_amount = sponsor.amount - sponsor_spent_amount

    if amount <= sponsor_left_amount:
        if student_gained_amount + amount <= student.tution_fee:
            instance.amount = amount
            instance.sponsor = sponsor
            instance.save()
            return instance
        else:
            raise ValidationError('Student gained amount must be less than tution fee')
    else:
        raise ValidationError('Sponsor left amount must be greater than amount')
    

def sponsor_amount_validator_for_create(validated_data):
    sponsor = get_object_or_404(Sponsor, id=validated_data['sponsor_id'])
    student = get_object_or_404(Student, id=validated_data['student_id'])
    amount = validated_data['amount']

    sponsor_spent_amount = sponsor.sponsorships.aggregate(amount=Coalesce(Sum('amount'), 0))['amount_sum']
    student_gained_amount = student.sponsorships.aggregate(amount=Coalesce(Sum('amount'), 0))['amount_sum']
    sponsor_left_amount = sponsor.amount - sponsor_spent_amount

    if amount <= sponsor_left_amount:
        if student_gained_amount + amount <= student.tution_fee:
            return validated_data
        else:
            raise ValidationError('Student gained amount must be less than tution fee')
    else:
        raise ValidationError('Sponsor left amount must be greater than amount')
