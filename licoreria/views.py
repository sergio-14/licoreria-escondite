from django.shortcuts import render, redirect
from .models import Detalle
from .forms import DetalleForm
from django.core.paginator import Paginator

def home(request):
    return render(request, 'home.html')

def detalle_list(request):
    # Obtener el término de búsqueda desde los parámetros GET
    filtro_detalle = request.GET.get('detalle', '')

    if filtro_detalle:
        detalles = Detalle.objects.filter(detalle__servicio__icontains=filtro_detalle)
    else:
        detalles = Detalle.objects.all()
    
    # Cálculo del total de monto_total
    total_monto = sum(detalle.monto_total for detalle in detalles)

    # Configuración de la paginación
    paginator = Paginator(detalles, 10)  # Mostrar 10 detalles por página
    page_number = request.GET.get('page')  # Obtener el número de página
    page_obj = paginator.get_page(page_number)

    return render(request, 'detalle_list.html', {
        'page_obj': page_obj,  
        'total_monto': total_monto,  
        'filtro_detalle': filtro_detalle,  
    })

def detalle_create(request):
    if request.method == 'POST':
        form = DetalleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('detalle_list')
    else:
        form = DetalleForm()
    return render(request, 'detalle_form.html', {'form': form})


from .models import Venta,Local
from .forms import VentaForm
from django.db.models import Sum

# Listar Ventas
def venta_list(request):
    # Obtener los valores de filtro enviados por GET
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    
    # Filtrar las ventas por rango de fechas si se especifican
    if fecha_inicio and fecha_fin:
        ventas = Venta.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
    else:
        ventas = Venta.objects.all()

    # Calcular el total de ganancias sumando los precios totales
    total_ganancia = ventas.aggregate(Sum('precio_total'))['precio_total__sum'] or 0

    return render(request, 'venta_list.html', {
        'ventas': ventas,
        'total_ganancia': total_ganancia,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    })

# Crear Venta
def venta_create(request):
    servicio = request.GET.get('servicio')  # El servicio seleccionado desde el formulario de filtro

    # Filtrar los detalles solo si se ha seleccionado un servicio
    if servicio:
        detalles = Detalle.objects.filter(detalle__servicio=servicio)  # Filtrar por el servicio
    else:
        detalles = []  # No mostrar detalles si no se ha filtrado por servicio

    # Sumar los 'monto_total' de los detalles, si existen
    total_monto = sum(detalle.monto_total for detalle in detalles)

    # Manejo del formulario
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)  # No guardar todavía para modificar el precio_total
            venta.precio_total = total_monto  # Asignar el total de monto calculado
            venta.save()  # Ahora sí guardamos la instancia
            return redirect('venta_list')  # Redirigir a la lista de ventas tras guardar el formulario
    else:
        form = VentaForm()

    # Pasar el formulario, los detalles filtrados y el total a la plantilla
    return render(request, 'venta_form.html', {
        'form': form,
        'detalles': detalles,  # Solo mostrar detalles filtrados
        'servicio': servicio,  # Pasamos el servicio seleccionado para que se mantenga en el formulario
        'servicios': Local.objects.all(),  # Pasamos los servicios para el filtro
        'total_monto': total_monto  # Pasamos el total de monto
    })


"""def filtro_por_servicio(request):
    servicio = request.GET.get('servicio')  # Obtener el servicio desde el parámetro de la URL
    detalles = Detalle.objects.filter(detalle__servicio=servicio)  # Filtrar Detalle por servicio en Local

    return render(request, 'nombre_template.html', {'detalles': detalles, 'servicio': servicio})"""

from .models import Detalle
from django.http import JsonResponse

"""
def obtener_detalles(request):
    detalle_id = request.GET.get('detalle_id')
    print("detalle_id recibido:", detalle_id)  # Verifica el valor del detalle_id
    if detalle_id:
        # Filtra los detalles por el id recibido
        detalles = Detalle.objects.filter(id_det=detalle_id).select_related('producto', 'detalle')
        print("Detalles encontrados:", detalles)  # Imprime los detalles encontrados

        if detalles.exists():
            data = [
                {
                    'id_det': detalle.id_det,
                    'razon': detalle.razon,
                    'producto__nombre_pro': detalle.producto.nombre_pro,
                    'cantidad': detalle.cantidad,
                    'monto_total': float(detalle.monto_total),
                    'servicio': detalle.detalle.servicio,  # Accede al servicio del Local relacionado
                }
                for detalle in detalles
            ]
            return JsonResponse(data, safe=False)
        else:
            return JsonResponse({'error': 'No se encontraron detalles'}, status=404)
    return JsonResponse({'error': 'No se proporcionó un detalle_id'}, status=400) """