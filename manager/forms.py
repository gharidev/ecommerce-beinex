from django import forms
from django_select2 import forms as s2forms

from core.models import Product, Category, SubCategory

class CategoriesWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "name__icontains",
    ]

class SubCategoriesWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "name__icontains",
    ]

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'image', 'description', 'price', 'categories', 'subcategories']
        widgets = {
            'categories': CategoriesWidget,
            'subcategories': SubCategoriesWidget,
        }

class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name']

class SubCategoryForm(forms.ModelForm):

    class Meta:
        model = SubCategory
        fields = ['name', 'category']

SubCategoryFormSet = forms.inlineformset_factory(Category, SubCategory, form=SubCategoryForm, extra=2)