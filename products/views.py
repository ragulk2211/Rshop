from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Product

# Create your views here.

def productsView(request):
    template = 'product/product.html'
    context = {
        'products' : Product.objects.all(),
        'current_page' : 'products'
    }
    
    return render (request, template, context)

# search product
from django.db.models import Q

def searchProducts(request):
    template = 'product/search_results.html',
    query = request.GET.get('q')
    if query:
        search_results = Product.objects.filter(
            Q(title__icontains = query) |
            Q(desc__icontains = query)
        )
        
        contaxt = {
            'query' : query,
            'products' : search_results
        }
    else :
          contaxt = {
            'query' : query,
            'products' : None
        }
        
    return render(request, template, contaxt)

# CURD operations using Generic Class Bases Views of Django

from django.views.generic import (
    CreateView, DetailView,UpdateView,DeleteView
)

# Listview 

class CreateProduct(CreateView):
    model = Product
    template_name = 'product/add_product.html'
    
    fields = "__all__"
    
    success_url = '/'
    
class ProductDetail(DetailView):
    model = Product
    template_name = 'product/product_details.html'
    context_object_name = 'product'
    
    def get_queryset(self):
        return Product.objects.prefetch_related('images')
    
from django.shortcuts import get_object_or_404, redirect
from .models import Product, ProductImage
from .forms import ProductImageForm

def AddImages(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            media = form.save(commit=False)
            media.product = product
            media.save()
            return redirect('product_details', pk=pk)
    else:
        form = ProductImageForm()

    return render(
        request,
        'product/add_images.html',
        {
            'form': form,
            'product': product
        }
    )
    
class UpdateProduct(UpdateView):
    model = Product
    template_name = 'product/update_product.html'
    fields = '__all__'
    
    success_url = '/'
    
class DeleteProduct(DeleteView):
    model = Product
    template_name = 'product/delete_product.html'
    success_url = '/'
    
# Edit product image 
from .models import ProductImage

class EditProductImage(UpdateView):
    model = ProductImage
    template_name = 'product/image_edit.html'
    fields = '__all__'
    context_object_name = 'image'
    def get_success_url(self):
        return reverse('product_details', kwargs={'pk':self.object.product.pk})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.object.product
        return context

class DeleteProductImage(DeleteView):
    model = ProductImage
    template_name = 'product/image_del.html'
    context_object_name = 'image'
    
    def get_success_url(self):
        return reverse('product_details', 
               kwargs={'pk': self.object.product.pk})

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.object.product
        return context