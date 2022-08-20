from django.contrib.auth.views import LoginView
from django.views.generic import DetailView
from django.urls import reverse
from django_filters.views import FilterView

from core.models import User, Product
from core.filters import ProductFilter

class ProductListView(FilterView):
    """Product list view with filtering."""
    model = Product
    filterset_class = ProductFilter
    paginate_by = 10
    context_object_name = 'products'
    template_name = 'core/product-list.html'


class CustomLoginView(LoginView):
    """Custom login view for all users."""
    template_name = 'core/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        """Redirect users according to user type."""
        if self.request.user.type == User.Types.MANAGER:
            return reverse('manager:product-list')
        else:
            return reverse('core:product-list')

class ProductDetailView(DetailView):
    """Customer product detail view."""
    model = Product
    template_name = 'manager/product-detail.html'
    context_object_name = 'product'
    extra_context = {'viewer': True}
    