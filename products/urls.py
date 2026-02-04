from django.urls import path

from .views import productsView, searchProducts

from .views import (
    CreateProduct, ProductDetail, UpdateProduct, DeleteProduct,AddImages
    
)

from .views import(
    EditProductImage, DeleteProductImage
)

urlpatterns = [
    path('',productsView,name='products'),
    path('all/', productsView, name = 'products_all'),
    
    path('search', searchProducts, name='search_products'),
    
    path('add/',CreateProduct.as_view(), name="add_product"),
    path('<int:pk>/', ProductDetail.as_view(), name='product_details'),
    path('<int:pk>/edit/',UpdateProduct.as_view(), name='edit_product'),
    path('<int:pk>/delete',DeleteProduct.as_view(), name='delete_product'),
    path('<int:pk>/add/',AddImages,name='add_images'),
    
    # product image
    
    path('image/edit/<int:pk>',EditProductImage.as_view(), name='edit_pro_image'),
    path('image/del/<int:pk>',DeleteProductImage.as_view(), name='del_pro_image'),
]