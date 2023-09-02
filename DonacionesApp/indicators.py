from DonacionesApp.models import Donacion

def get_cantidad_total_donaciones(institucion):
    # Cantidad total de donaciones
    return Donacion.get_cantidad_total_donaciones(institucion)
    
def get_cantidad_donaciones_por_estado(institucion):
    """Cantidad de donaciones por estado"""

    return {'Creada': Donacion.get_cantidad_por_estado(institucion,1),
            'Aceptada': Donacion.get_cantidad_por_estado(institucion,2),
            'Enviada': Donacion.get_cantidad_por_estado(institucion,3),
            'Recibida': Donacion.get_cantidad_por_estado(institucion,4),
            'Cancedala': Donacion.get_cantidad_por_estado(institucion,0)
        }

def get_cantidad_donaciones_por_donante(institucion):
    """Cantidad de donaciones por donante"""
    result = {}
    for i in Donacion.objects.all():
        result[str(i.donante)] = result[str(i.donante)] + 1