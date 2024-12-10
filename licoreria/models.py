from django.db import models

class Tipo(models.Model):
    id_tipo = models.AutoField(primary_key=True)  
    nombre_tipo = models.CharField(max_length=100)  

    def __str__(self):
        return self.nombre_tipo


class Producto(models.Model):
    id_pro = models.AutoField(primary_key=True)  
    nombre_pro = models.CharField(max_length=100)  
    precio = models.DecimalField(max_digits=10, decimal_places=2)  
    id_tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE, related_name="productos")

    def __str__(self):
        return f"{self.nombre_pro} - por Unidad {self.precio} Bs."

class Local(models.Model):
    ESTADO_CHOICES = [
        ('libre', 'Libre'),
        ('ocupado', 'Ocupado'),
    ]

    servicio = models.CharField(max_length=150)  # Descripción del servicio
    estado = models.CharField(
        max_length=10,
        choices=ESTADO_CHOICES,
        default='libre'
    )  # Campo con las opciones de estado

    def __str__(self):
        return f"{self.servicio}"

class Detalle(models.Model):
    id_det = models.AutoField(primary_key=True)   
    razon = models.CharField(max_length=150)  
    detalle = models.ForeignKey(Local, on_delete=models.CASCADE, related_name="localidad")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name="Productos")
    cantidad = models.IntegerField()
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)  

    def __str__(self):
        return self.razon


class Venta(models.Model):
    id_det_venta = models.AutoField(primary_key=True)  
    fecha = models.DateTimeField()
    detalle = models.ForeignKey(Detalle, on_delete=models.CASCADE, related_name="detalle_ventas")
    precio_total = models.DecimalField(max_digits=10, decimal_places=2) 

    def __str__(self):
        return f"Detalle Venta {self.id_det_venta}"
    
    

