import django_filters
from .models import Organization, Team


class OrganizationFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    industry = django_filters.CharFilter(field_name='industry', lookup_expr='icontains')
    city = django_filters.CharFilter(field_name='city', lookup_expr='icontains')
    country = django_filters.CharFilter(field_name='country', lookup_expr='icontains')

    class Meta:
        model = Organization
        fields = ['size', 'industry', 'is_active', 'city', 'country']


class TeamFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Team
        fields = ['name', 'organization']
