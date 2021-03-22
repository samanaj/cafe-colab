from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from inv.models import Producto
from .cart import Cart


@login_required(login_url="bases:login")
def add_product(request, product_id):
    cart = Cart(request)
    product = Producto.objects.get(id=product_id)
    cart.add(product=product)
    return redirect("inv:listado_productos")


@login_required(login_url="bases:login")
def remove_product(request, product_id):
    cart = Cart(request)
    product = Producto.objects.get(id=product_id)
    cart.remove(product)
    return redirect("inv:listado_productos")


@login_required(login_url="bases:login")
def decrement_product(request, product_id):
    cart = Cart(request)
    product = Producto.objects.get(id=product_id)
    cart.decrement(product=product)
    return redirect("inv:listado_productos")


@login_required(login_url="bases:login")
def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect("inv:listado_productos")
