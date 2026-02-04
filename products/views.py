from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Product

from .forms import ProductForm, ProductImageForm

# Create your views here.
def productsView(request):
    template = 'products/products.html'
    context = {
        'products' : Product.objects.all(),
        'current_page' : 'products'
    }
    return render(request, template, context)

# search Products
from django.db.models import Q 
def searchProducts(request):
    template = 'products/search_results.html'
    query = request.GET.get('q')
    if query:
        search_results = Product.objects.filter(
            Q(title__icontains = query) |
            Q(desc__icontains = query) 
        )
        
        context = {
            'query' : query,
            'products' : search_results
        }
    else:
        context = {
            'query' : query,
            'products' : None
        }
    return render(request, template_name=template, context = context)


# CRUD Operations using Generic Class Based Views of Django

from django.views.generic import ( CreateView, DetailView,
                                   UpdateView, DeleteView )

# ListView has already been implemented using a function above : productsView()

class CreateProduct(CreateView):
    model = Product
    template_name = 'products/add_product.html'
    form_class = ProductForm
    # redirection url for successful creation of resource
    def get_success_url(self):
        return reverse('product_details', kwargs={'pk':self.object.pk})

# -------
from django.views.generic.edit import FormMixin
# This mixin provides ability to render forms from the `form_class`

class ProductDetail(FormMixin, DetailView):
    model = Product
    template_name = 'products/product_details.html'
    context_object_name = 'product'
    # providing form class for Product Image
    form_class = ProductImageForm

    def get_success_url(self):
        return reverse('product_details', kwargs={'pk':self.object.pk})
    
    # overriding the queryset to pre-fetch 
    # and add the product images alongside products
    def get_queryset(self):
        return Product.objects.prefetch_related('images')   
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            image = form.save(commit = False)
            image.product = self.object 
            image.save()
            return redirect(self.get_success_url())



class UpdateProduct(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/update_product.html'
    
    def get_success_url(self):
        return reverse('product_details', kwargs={'pk':self.object.pk})

class DeleteProduct(DeleteView):
    model = Product
    template_name = 'products/delete_product.html'
    success_url = '/'



# Edit Product Image
from .models import ProductImage

class EditProductImage(UpdateView):
    model = ProductImage
    template_name = 'products/image_edit.html'
    form_class = ProductImageForm
    context_object_name = 'image'
    def get_success_url(self):
        return reverse('product_details', kwargs={'pk':self.object.product.pk})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.object.product
        return context
    
class DeleteProductImage(DeleteView):
    model = ProductImage
    template_name = 'products/image_del.html'
    context_object_name = 'image'

    def get_success_url(self):
        return reverse('product_details', kwargs={'pk':self.object.product.pk})
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.object.product
        return context
    