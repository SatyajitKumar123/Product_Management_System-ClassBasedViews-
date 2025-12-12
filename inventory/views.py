from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib import messages

from .models import Product

class UserSignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('login')
    
    
    
class SuccessMessageMixin:
    success_message = None
    
    def form_valid(self, form):
        response = super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response
    
    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        if self.success_message:
            messages.success(self.request, self.success_message)
        return response
    
class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    success_message = "You logged in successfully!"

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset
    
class ProductCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Product
    template_name = 'product_form.html'
    fields = ['name', 'description', 'price', 'in_stock']
    success_url = reverse_lazy('product-list')
    success_message = "Product created successfully!"
    
    
    
class ProductUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Product 
    template_name = 'product_form.html'
    fields = ['name', 'description', 'price', 'in_stock']
    success_url = reverse_lazy('product-list')
    success_message = "Product updated successfully!"
    
    
class ProductDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Product
    template_name = 'product_delete_confirm.html'
    success_url = reverse_lazy('product-list')
    success_message = "Product deleted successfully!"
    
