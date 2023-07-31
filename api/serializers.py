from django.db.models import Sum, Count
from django.db.models.functions import Coalesce
from django.forms.models import model_to_dict
from rest_framework import serializers
from django.core.validators import MinValueValidator
from .models import Sponsor, Student, University, Sponsorship
from .validator import sponsor_amount_validator_for_create, sponsor_amount_validator_for_update


class SponsorSerializer(serializers.ModelSerializer):
    spent_amount = serializers.SerializerMethodField()

    class Meta:
        model = Sponsor
        fields = '__all__'
        extra_kwargs = {
            'full_name': {'allow_null': False, 'required': True},
            'phone_number': {'allow_null': False, 'required': True},
            'amount': {'allow_null': False, 'required': True, 'validators': [MinValueValidator(0.0)]},
            'person_type': {'allow_null': False, 'required': True}
        }

    def create(self, validated_data):
        validated_data['status'] = 'new'
        sponsor = Sponsor.objects.create(**validated_data)
        return sponsor

    @staticmethod
    def get_spent_amount(sponsor):
        spent_amount = sponsor.sponsorships.aggregate(amount_sum=Coalesce(Sum('amount'), 0))['amount_sum']
        return spent_amount

    def validate_company_name(self, value):
        if self.initial_data.get('person_type') == 'legalentity':
            return value
        else:
            return None


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    university = UniversitySerializer(read_only=True)
    university_id = serializers.IntegerField(allow_null=False, required=True, write_only=True)
    gained_amount = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'full_name', 'phone_number', 'tution_fee', 'gained_amount', 'degree', 'university',
                  'university_id']

        extra_kwargs = {
            'full_name': {'allow_null': False, 'required': True},
            'phone_number': {'allow_null': False, 'required': True},
            'tution_fee': {'allow_null': False, 'required': True, 'validators': [MinValueValidator(0.0)]},
            'degree': {'allow_null': False, 'required': True},
        }

    @staticmethod
    def get_gained_amount(student):
        gained_amount = student.sponsorships.aggregate(amount_sum=Coalesce(Sum('amount'), 0))['amount_sum']
        return gained_amount


class SponsorshipSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    student_id = serializers.IntegerField(allow_null=False, required=True, write_only=True)
    sponsor = SponsorSerializer(read_only=True)
    sponsor_id = serializers.IntegerField(allow_null=False, required=True, write_only=True)

    class Meta:
        model = Sponsorship
        fields = ['id', 'student', 'student_id', 'sponsor', 'sponsor_id', 'amount', 'date_created']
        extra_kwargs = {'amount': {'required': True, 'validators': [MinValueValidator(0.0)]}}

    def update(self, instance, validated_data):
        instance = sponsor_amount_validator_for_update(instance, validated_data)
        return instance

    def create(self, validated_data):
        instance = sponsor_amount_validator_for_create(validated_data)
        return instance


class SponsorshipsByStudentSerializer(serializers.ModelSerializer):
    sponsor = serializers.SerializerMethodField()

    class Meta:
        model = Sponsorship
        fields = ['id', 'sponsor', 'amount']

    def get_sponsor(sponsorship):
        data = model_to_dict(sponsorship)
        print(data)

        return data


class SponsorshipsBySponsorSerializer(serializers.ModelSerializer):
    student = serializers.SerializerMethodField()

    class Meta:
        model = Sponsorship
        fields = ['id', 'student', 'amount']

    @staticmethod
    def get_student(sponsorship):
        data = model_to_dict(sponsorship)
        return data


class DashboardAmountSerializer(serializers.Serializer):
    total_sponsored_amount = serializers.SerializerMethodField()
    total_tution_fee_amount = serializers.SerializerMethodField()
    total_needed_amount = serializers.SerializerMethodField()

    def get_total_sponsored_amount(self):
        total_sponsored_amount = Sponsorship.objects.aggregate(Sum('amount'))['amount__sum']
        return total_sponsored_amount

    def get_total_tution_fee_amount(self):
        total_tution_fee_amount = Student.objects.aggregate(Sum('tution_fee'))['tution_fee__sum']
        return total_tution_fee_amount

    def get_total_needed_amount(self):
        total_sponsored_amount = Sponsorship.objects.aggregate(Sum('amount'))['amount__sum']
        total_tution_fee_amount = Student.objects.aggregate(Sum('tution_fee'))['tution_fee__sum']
        total_needed_amount = total_tution_fee_amount - total_sponsored_amount
        return total_needed_amount

    def data(self):
        return self.__dict__


class DashboardGraphSerializer(serializers.Serializer):
    sponsors_stats = serializers.SerializerMethodField()
    students_stats = serializers.SerializerMethodField()

    def get_sponsors_stats(self):
        sponsors_stats = Sponsor.objects.extra({'date_created': "date(date_created)"}).values(
            'date_created').annotate(
            count=Count('id')).values_list('date_created', 'count')
        return sponsors_stats

    def get_students_stats(self):
        students_stats = Student.objects.extra({'date_created': "date(date_created)"}).values(
            'date_created').annotate(
            count=Count('id')).values_list('date_created', 'count')
        return students_stats

    def data(self):
        return self.__dict__
