import django_filters
from django.db import models
from django.db.models.query_utils import Q

from core.models import Product, Category, SubCategory
from django_select2.forms import Select2MultipleWidget

class ProductFilter(django_filters.FilterSet):
    """
    Filter product with `categories` & `subcategories`.
    Product belonging to a subcategory will show up when filtering by its parent category.
    """
    categories = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        widget=Select2MultipleWidget,
        method='categories_filter'
    )
    subcategories = django_filters.ModelMultipleChoiceFilter( 
        queryset=SubCategory.objects.all(),
        widget=Select2MultipleWidget
    )

    def categories_filter(self, queryset, value, *args, **kwargs):
        cat_ids = []
        sub_ids = []
        for category in args[0]:
            cat_ids.append(category.id)
            for subcategory in category.subcategory_set.all():
                sub_ids.append(subcategory.id)
        q = Q()
        if cat_ids:
            q |= Q(categories__in=cat_ids)
        if sub_ids:
            q |= Q(subcategories__in=sub_ids)
        return queryset.filter(q).distinct()

    class Meta:
        model = Product
        fields = ['categories', 'subcategories']