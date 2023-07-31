from django_filters import FilterSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAdminUser
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .permissions import IsAdminOrCreateOnly
from rest_framework import filters
from . import serializers
from .models import *


class DateRangeFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        date_fields = view.date_range_filter_fields
        filter_mask = {}
        for date_field in date_fields:
            date_field__gte = date_field + '__gte'
            date_field__lte = date_field + '__lte'
            date_field_gte = date_field + '-gte'
            date_field_lte = date_field + '-lte'
            if date_field_gte in request.query_params:
                filter_mask[date_field__gte] = request.query_params[date_field_gte]
            if date_field_lte in request.query_params:
                filter_mask[date_field__lte] = request.query_params[date_field_lte]
    
        queryset = queryset.filter(**filter_mask)
        return queryset





        
    

    


class SponsorView(generics.ListCreateAPIView):
    permission_classes = [IsAdminOrCreateOnly]
    queryset = Sponsor.objects.all()
    serializer_class = serializers.SponsorSerializer
    filter_backends = [DateRangeFilter, SearchFilter, DjangoFilterBackend]
    search_fields = ['full_name', 'company_name']
    filterset_fields = ['amount', 'status']
    date_range_filter_fields = ['date_created']


class SponsorDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Sponsor.objects.all()
    serializer_class = serializers.SponsorSerializer


class StudentView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer
    filter_backends = [DateRangeFilter, SearchFilter, DjangoFilterBackend]
    search_fields = ['full_name']
    filterset_fields = ['degree', 'university']
    date_range_filter_fields = ['date_created']


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer


class SponsorshipView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Sponsorship.objects.all()
    serializer_class = serializers.SponsorshipSerializer
    filter_backends = [DateRangeFilter, SearchFilter, DjangoFilterBackend]
    search_fields = ['sponsor__full_name', 'sponsor__company_name', 'student__full_name']
    date_range_filter_fields = ['date_created']


class SponsorshipDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Sponsorship.objects.all()
    serializer_class = serializers.SponsorshipSerializer


class SponsorshipsByStudentView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = serializers.SponsorshipsByStudentSerializer

    def get_queryset(self):
        student = get_object_or_404(Student, id=self.kwargs['pk'])
        queryset = student.sponsorships.all()
        return queryset


class SponsorshipsBySponsorView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = serializers.SponsorshipsBySponsorSerializer

    def get_queryset(self):
        sponsor = get_object_or_404(Sponsor, id=self.kwargs['pk'])
        queryset = sponsor.sponsorships.all()
        return queryset


class UniversityView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = University.objects.all()
    serializer_class = serializers.UniversitySerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']


class UniversityDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = University.objects.all()
    serializer_class = serializers.UniversitySerializer


class DashboardAmountView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        serializer = serializers.DashboardAmountSerializer()
        return Response(data={
            'total_sponsored_amount': serializer.get_total_sponsored_amount(),
            'total_tution_fee_amount': serializer.get_total_tution_fee_amount(),
            'total_need_amount': serializer.get_total_needed_amount(),
        })


class DashboardGraphView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        serializer = serializers.DashboardGraphSerializer()
        return Response(data={
            'sponsor_graph': serializer.get_sponsors_stats(),
            'student_graph': serializer.get_students_stats(),
        })


class DashboardView(APIView):
    permission_classes = [IsAdminUser]

    def get(request, *args, **kwargs):
        dashboard_amount_serializer = DashboardAmountView()
        dashboard_graph_serializer = DashboardGraphView()
        return Response(data={
            'amount_stats': dashboard_amount_serializer.get(request).data,
            'graph_stats': dashboard_graph_serializer.get(request).data,
        })
