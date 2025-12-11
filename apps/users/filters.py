import django_filters
from .models import User, Profile


class UserFilter(django_filters.FilterSet):
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    first_name = django_filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = django_filters.CharFilter(field_name='last_name', lookup_expr='icontains')
    email = django_filters.CharFilter(field_name='email', lookup_expr='icontains')
    username = django_filters.CharFilter(field_name='username', lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['role', 'is_active', 'username', 'email', 'first_name', 'last_name']


class ProfileFilter(django_filters.FilterSet):
    years_experience = django_filters.NumberFilter(field_name='years_experience', lookup_expr='gte')
    location = django_filters.CharFilter(field_name='location', lookup_expr='icontains')
    current_position = django_filters.CharFilter(field_name='current_position', lookup_expr='icontains')

    class Meta:
        model = Profile
        fields = ['location', 'current_position', 'years_experience']
