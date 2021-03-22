from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.views.generic.list import ListView
from django.views.generic import DetailView
from .models import Pedido, lineaPedido
from carrito.cart import Cart


# Create your views here.
@login_required(login_url='bases:login')
def process_pedido(request):
    pedido = Pedido.objects.create(user=request.user, completado=True)
    cart = Cart(request)
    linea_Pedido = list()
    for key, value in cart.cart.items():
        linea_Pedido.append(
            lineaPedido(
                producto_id=key,
                cantidad=value["cantidad"],
                user=request.user,
                pedido=pedido
            )
        )

    lineaPedido.objects.bulk_create(linea_Pedido)

    send_order_email(
        pedido=pedido,
        linea_Pedido=linea_Pedido,
        username=request.user.username,
        user_email=request.user.email
    )

    cart.clear()

    messages.success(request, "El pedido se ha creado correctamente!")
    return redirect("inv:listado_productos")


def send_order_email(**kwargs):
    subject = "Gracias por tu pedido"
    html_message = render_to_string("emails/nuevo_pedido.html", {
        "pedido": kwargs.get("pedido"),
        "linea_Pedido": kwargs.get("linea_Pedido"),
        "username": kwargs.get("username")
    })
    plain_message = strip_tags(html_message)
    from_email = "soporte.samanaj@gmail.com"
    to = kwargs.get("user_email")
    send_mail(subject, plain_message, from_email, [to], html_message=html_message)


class peididoList(ListView):
    model = Pedido
    ordering = ["-id"]
    template_name = "pedidos/listado.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class pedidoDetail(DetailView):
    model = Pedido
    template_name = "pedidos/detalle.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
