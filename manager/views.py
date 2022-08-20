from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from manager.mixins import ManagerRequiredMixin
from core.models import Product, Category
from manager.forms import ProductForm, CategoryForm, SubCategoryFormSet

class ProductCreateView(ManagerRequiredMixin, CreateView):
    """View for creating a product."""
    template_name = 'manager/form.html'
    form_class = ProductForm
    extra_context = {'title': 'New product'}

    def get_success_url(self):
        return reverse('manager:product-detail', kwargs={'pk':self.object.pk})

class ProductUpdateView(ManagerRequiredMixin, UpdateView):
    """View for updating a product."""
    model = Product
    template_name = 'manager/form.html'
    form_class = ProductForm
    extra_context = {'title': 'Update product'}

    def get_success_url(self):
        return reverse('manager:product-detail', kwargs={'pk':self.object.pk})

class ProductListView(ManagerRequiredMixin, ListView):
    """View for listing products with pagination."""
    model = Product
    paginate_by = 10
    context_object_name = 'products'
    template_name = 'manager/product-list.html'

class ProductDetailView(ManagerRequiredMixin, DetailView):
    """Detailed view of a product."""
    model = Product
    template_name = 'manager/product-detail.html'

class ProductDeleteView(ManagerRequiredMixin, DeleteView):
    """View for deleting a product."""
    model = Product
    template_name = 'manager/product-delete.html'
    success_url = reverse_lazy('manager:product-list')
    context_object_name = 'product'

class CategoryCreateView(ManagerRequiredMixin, CreateView):
    """View for creating a category with inlineformset factory to sub category."""
    model = Category
    form_class = CategoryForm
    template_name = 'manager/category-form.html'
    extra_context = {'title': 'Create category'}

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            data['subcategories'] = SubCategoryFormSet(self.request.POST)
        else:
            data['subcategories'] = SubCategoryFormSet()
        return data
    
    def form_valid(self, form):
        context = self.get_context_data()
        subcategories = context['subcategories']
        response = super().form_valid(form)
        if subcategories.is_valid():
            subcategories.instance = self.object
            subcategories.save()
        else:
            return self.render_to_response(self.get_context_data(form=form))
        return response

    def get_success_url(self):
        return reverse('manager:category-list')
    
class CategoryUpdateView(ManagerRequiredMixin, UpdateView):
    """View for updating a category with inlineformset factory to sub category."""
    model = Category
    form_class = CategoryForm
    template_name = 'manager/category-form.html'
    extra_context = {'title': 'Update category'}

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['subcategories'] = SubCategoryFormSet(self.request.POST, instance=self.get_object())
        else:
            data['subcategories'] = SubCategoryFormSet(instance=self.get_object())
        return data
    
    def form_valid(self, form):
        context = self.get_context_data()
        subcategories = context['subcategories']
        if subcategories.is_valid():
            subcategories.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('manager:category-list')

class CategoryListView(ManagerRequiredMixin, ListView):
    """View for listing categories."""
    template_name = 'manager/category-list.html'
    model = Category
    context_object_name = 'categories'

class CategoryDeleteView(ManagerRequiredMixin, DeleteView):
    """View for deleting a category."""
    model = Category
    template_name = 'manager/category-delete.html'
    success_url = reverse_lazy('manager:category-list')
    context_object_name = 'category'