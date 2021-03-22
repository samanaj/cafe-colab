from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import F, Sum, FloatField
from inv.models import Producto

User = get_user_model()


class Pedido(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completado = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)
    #para usar una propiedad de agregate para obtener el total, columan calculada en base de datos.
    @property
    def total(self):
        return self.lineapedido_set.aggregate(
            #agregar lo que queremos, la F es para sacar toda la información que necesitamos. outputfiel tipo de salida.
            total=Sum(F("producto__precio") * F("cantidad"), output_field=FloatField())
        )["total"] or FloatField(0)

    def __str__(self):
        return self.id

    class Meta:        
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'
        ordering = ['id']


class lineaPedido(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.cantidad} de {self.producto.nombre}'

    class Meta:        
        verbose_name = 'Línea de pedido'
        verbose_name_plural = 'Líneas de pedidos'
        ordering = ['id']
