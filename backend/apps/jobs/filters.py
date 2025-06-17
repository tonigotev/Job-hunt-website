from django_filters import rest_framework as filters
from .models import Job


class JobFilter(filters.FilterSet):
    """FilterSet allowing salary range filtering along with existing fields."""
    min_salary = filters.NumberFilter(field_name="salary", lookup_expr="gte")
    max_salary = filters.NumberFilter(field_name="salary", lookup_expr="lte")

    class Meta:
        model = Job
        fields = ["employment_type", "company__location", "min_salary", "max_salary"] 