from DonacionesApp.models import Donacion, Bien, Necesidad
from baseApp.models import Donante, Institucion
from django.contrib.auth.models import User

class Indicadores():
    def get_indicadores(usuario):
        user = User.objects.get(username=usuario)
        if user.groups.filter(pk=1).exists():
            donante = Donante.objects.get(usuario=user)
            result = {
                'cant_donaciones_total': IndicadoresDonante.get_cantidad_total_donaciones(donante),
                'cant_donaciones_por_estado': IndicadoresDonante.get_cantidad_donaciones_por_estado(donante),
                'cant_donaciones_por_institucion': IndicadoresDonante.get_cantidad_donaciones_por_institucion(donante),
                'cant_donaciones_bienes': IndicadoresDonante.get_cantidad_total_donaciones_bienes(donante),
                'cant_donaciones_bienes_por_estado': IndicadoresDonante.get_cantidad_donaciones_bienes_por_estado(donante),
                'cant_donaciones_bienes_por_institucion': IndicadoresDonante.get_cantidad_donaciones_bienes_por_institucion(donante),
                'cant_donaciones_bienes_por_tipo_bien': IndicadoresDonante.get_cantidad_donaciones_bienes_por_tipo_bien(donante),
                'cant_donaciones_por_tipo_bien_por_estado': IndicadoresDonante.get_cantidad_donaciones_bienes_por_tipo_bien_por_estado(donante),
                'cant_donaciones_monetarias': IndicadoresDonante.get_cantidad_total_donaciones_monetarias(donante),
                'cant_donaciones_monetarias_por_estado': IndicadoresDonante.get_cantidad_donaciones_monetarias_por_estado(donante),
                'cant_donaciones_monetarias_por_institucion': IndicadoresDonante.get_cantidad_donaciones_monetarias_por_institucion(donante),
                'monto_donaciones_monetarias': IndicadoresDonante.get_monto_donaciones_monetarias(donante),
                'monto_donaciones_monetarias_por_estado': IndicadoresDonante.get_monto_donaciones_monetarias_por_estado(donante),
                'monto_donaciones_monetarias_por_institucion': IndicadoresDonante.get_monto_donaciones_monetarias_por_institucion(donante),
                'porc_donaciones_entregadas': IndicadoresDonante.get_porcentaje_donaciones_entregadas_sobre_total(donante),
                'porc_donaciones_bienes_entregadas': IndicadoresDonante.get_porcentaje_donaciones_bienes_entregadas_sobre_total(donante),
                'porc_donaciones_monetarias_entregadas': IndicadoresDonante.get_porcentaje_donaciones_monetarias_entregadas_sobre_total(donante),
                'porc_donaciones_rechazadas': IndicadoresDonante.get_porcentaje_donaciones_rechazadas_sobre_total(donante),
                'porc_donaciones_bienes_rechazadas': IndicadoresDonante.get_porcentaje_donaciones_bienes_rechazadas_sobre_total(donante),
                'porc_donaciones_monetarias_rechazadas': IndicadoresDonante.get_porcentaje_donaciones_monetarias_rechazadas_sobre_total(donante),
                'porc_donaciones_pendientes': IndicadoresDonante.get_porcentaje_donaciones_pendientes_sobre_total(donante),
                'porc_donaciones_bienes_pendientes': IndicadoresDonante.get_porcentaje_donaciones_bienes_pendientes_sobre_total(donante),
                'porc_donaciones_monetarias_pendientes': IndicadoresDonante.get_porcentaje_donaciones_monetarias_pendientes_sobre_total(donante),
            }

        elif user.groups.filter(pk=2).exists():
            institucion = Institucion.objects.get(usuario=user)
            
            result = {
                'cant_donaciones_total': IndicadoresInstitucion.get_cantidad_total_donaciones(institucion),
                'cant_donaciones_por_estado': IndicadoresInstitucion.get_cantidad_donaciones_por_estado(institucion),
                'cant_donaciones_por_institucion': IndicadoresInstitucion.get_cantidad_donaciones_por_donante(institucion),
                'cant_donaciones_bienes': IndicadoresInstitucion.get_cantidad_total_donaciones_bienes(institucion),
                'cant_donaciones_bienes_por_estado': IndicadoresInstitucion.get_cantidad_donaciones_bienes_por_estado(institucion),
                'cant_donaciones_bienes_por_institucion': IndicadoresInstitucion.get_cantidad_donaciones_bienes_por_donante(institucion),
                'cant_donaciones_bienes_por_tipo_bien': IndicadoresInstitucion.get_cantidad_donaciones_bienes_por_tipo_bien(institucion),
                'cant_donaciones_por_tipo_bien_por_estado': IndicadoresInstitucion.get_cantidad_donaciones_bienes_por_tipo_bien_por_estado(institucion),
                'cant_donaciones_monetarias': IndicadoresInstitucion.get_cantidad_total_donaciones_monetarias(institucion),
                'cant_donaciones_monetarias_por_estado': IndicadoresInstitucion.get_cantidad_donaciones_monetarias_por_estado(institucion),
                'cant_donaciones_monetarias_por_institucion': IndicadoresInstitucion.get_cantidad_donaciones_monetarias_por_donante(institucion),
                'monto_donaciones_monetarias': IndicadoresInstitucion.get_monto_donaciones_monetarias(institucion),
                'monto_donaciones_monetarias_por_estado': IndicadoresInstitucion.get_monto_donaciones_monetarias_por_estado(institucion),
                'monto_donaciones_monetarias_por_institucion': IndicadoresInstitucion.get_monto_donaciones_monetarias_por_donante(institucion),
                'porc_donaciones_entregadas': IndicadoresInstitucion.get_porcentaje_donaciones_entregadas_sobre_total(institucion),
                'porc_donaciones_bienes_entregadas': IndicadoresInstitucion.get_porcentaje_donaciones_bienes_entregadas_sobre_total(institucion),
                'porc_donaciones_monetarias_entregadas': IndicadoresInstitucion.get_porcentaje_donaciones_monetarias_entregadas_sobre_total(institucion),
                'porc_donaciones_rechazadas': IndicadoresInstitucion.get_porcentaje_donaciones_rechazadas_sobre_total(institucion),
                'porc_donaciones_bienes_rechazadas': IndicadoresInstitucion.get_porcentaje_donaciones_bienes_rechazadas_sobre_total(institucion),
                'porc_donaciones_monetarias_rechazadas': IndicadoresInstitucion.get_porcentaje_donaciones_monetarias_rechazadas_sobre_total(institucion),
                'porc_donaciones_pendientes': IndicadoresInstitucion.get_porcentaje_donaciones_pendientes_sobre_total(institucion),
                'porc_donaciones_bienes_pendientes': IndicadoresInstitucion.get_porcentaje_donaciones_bienes_pendientes_sobre_total(institucion),
                'porc_donaciones_monetarias_pendientes': IndicadoresInstitucion.get_porcentaje_donaciones_monetarias_pendientes_sobre_total(institucion),
                'cant_necesidades_activas_total': IndicadoresInstitucion.get_cantidad_total_necesidades_activas(institucion),
                'cant_necesidades_inactivas_total': IndicadoresInstitucion.get_cantidad_total_necesidades_inactivas(institucion),
                'porc_necesidades_activas': IndicadoresInstitucion.get_porcentaje_necesidades_activas_sobre_total(institucion),
                'porc_necesidades_inactivas': IndicadoresInstitucion.get_porcentaje_necesidades_inactivas_sobre_total(institucion),
                'cant_necesidades_por_tipo': IndicadoresInstitucion.get_cantidad_necesidades_por_tipo(institucion),
                'cant_necesidades_por_tipo_por_estado': IndicadoresInstitucion.get_cantidad_necesidades_por_tipo_por_estado(institucion),
            }

        return result


class IndicadoresInstitucion():
    def get_cantidad_total_donaciones(institucion):
        # Cantidad total de donaciones de una institucion
        return Donacion.get_cantidad_total_donaciones(institucion=institucion)
        
    def get_cantidad_donaciones_por_estado(institucion):
        """Cantidad de donaciones por estado"""
        result = {}
        codigos_estados = [i[0] for i in Donacion.CODIGOS_ESTADO]

        for cod_estado in codigos_estados:
            result[cod_estado] = Donacion.get_cantidad_total_donaciones(institucion=institucion, cod_estado=cod_estado)

        return result

    def get_cantidad_donaciones_por_donante(institucion):
        """Cantidad de donaciones por donante"""
        result = {}
        donantes = Donacion.get_donantes(institucion=institucion)

        for donante in donantes:
            result[str(donante)] = Donacion.get_cantidad_total_donaciones(institucion=institucion,donante=donante)

        return result

    def get_cantidad_total_donaciones_bienes(institucion):
         # Cantidad total de donaciones de una institucion
        return Donacion.get_cantidad_total_donaciones(institucion=institucion,tipo='bienes')

    def get_cantidad_donaciones_bienes_por_estado(institucion):
        """Cantidad de donaciones por estado"""
        result = {}
        codigos_estados = [i[0] for i in Donacion.CODIGOS_ESTADO]

        for i in codigos_estados:
            result[i] = Donacion.get_cantidad_total_donaciones(institucion=institucion,tipo='bienes',cod_estado=i)

        return result

    def get_cantidad_donaciones_bienes_por_donante(institucion):
        """Cantidad de donaciones por donante"""
        result = {}
        donantes = Donacion.get_donantes(institucion=institucion)

        for donante in donantes:
            result[str(donante)] = Donacion.get_cantidad_total_donaciones(institucion=institucion,tipo='bienes',donante=donante)

        return result

    def get_cantidad_donaciones_bienes_por_tipo_bien(institucion):
        """Cantidad de donaciones de bienes agrupado por tipo de bien"""
        result = {}
        tipos_bien = [i[0] for i in Bien.TIPOS_BIEN]

        for tipo_bien in tipos_bien:
            result[tipo_bien] = Donacion.get_cantidad_total_donaciones_por_bien(institucion=institucion,tipo_bien=tipo_bien)

        return result

    def get_cantidad_total_donaciones_monetarias(institucion):
         # Cantidad total de donaciones de una institucion
        return Donacion.get_cantidad_total_donaciones(institucion=institucion,tipo='monetarias')

    def get_cantidad_donaciones_monetarias_por_estado(institucion):
        """Cantidad de donaciones por estado"""
        result = {}
        codigos_estados = [i[0] for i in Donacion.CODIGOS_ESTADO]

        for i in codigos_estados:
            result[i] = Donacion.get_cantidad_total_donaciones(institucion=institucion,tipo='monetarias',cod_estado=i)

        return result

    def get_cantidad_donaciones_monetarias_por_donante(institucion):
        """Cantidad de donaciones por donante"""
        result = {}
        donantes = Donacion.get_donantes(institucion=institucion)

        for donante in donantes:
            result[str(donante)] = Donacion.get_cantidad_total_donaciones(institucion=institucion,tipo='monetarias',donante=donante)

        return result

    def get_monto_donaciones_monetarias(institucion):
        """Monto total de todas las donaciones monetarias realizadas para la institución"""
        return Donacion.get_monto_total_donaciones_monetarias(institucion=institucion)

    def get_monto_donaciones_monetarias_por_estado(institucion):
        """Monto total de todas las donaciones monetarias realizadas para la institución
        agrupado por estado"""
        result = {}
        codigos_estados = [i[0] for i in Donacion.CODIGOS_ESTADO]

        for i in codigos_estados:
            result[i] = Donacion.get_monto_total_donaciones_monetarias(institucion=institucion,cod_estado=i)

        return result

    def get_monto_donaciones_monetarias_por_donante(institucion):
        """Monto total de todas las donaciones monetarias realizadas para la institución
        agrupado por donante"""
        result = {}
        donantes = Donacion.get_donantes(institucion=institucion)

        for donante in donantes:
            result[str(donante)] = Donacion.get_monto_total_donaciones_monetarias(institucion=institucion,donante=donante)

        return result

    def get_porcentaje_donaciones_entregadas_sobre_total(institucion):
        """"""
        return (
            Donacion.get_cantidad_total_donaciones(institucion=institucion,tipo='monetarias',cod_estado=3)
            + Donacion.get_cantidad_total_donaciones(institucion=institucion,tipo='bienes',cod_estado=5)
            ) / Donacion.get_cantidad_total_donaciones(institucion=institucion)
    
    def get_porcentaje_donaciones_bienes_entregadas_sobre_total(institucion):
        """"""
        return (Donacion.get_cantidad_total_donaciones(institucion=institucion,tipo='bienes',cod_estado=5)
            ) / Donacion.get_cantidad_total_donaciones(institucion=institucion,tipo='bienes')
    
    def get_porcentaje_donaciones_monetarias_entregadas_sobre_total(institucion):
        """"""
        return (Donacion.get_cantidad_total_donaciones(institucion=institucion,tipo='monetarias',cod_estado=3)
            ) / Donacion.get_cantidad_total_donaciones(institucion=institucion,tipo='monetarias')

    def get_porcentaje_donaciones_rechazadas_sobre_total(institucion):
        """"""
        return (Donacion.get_cantidad_total_donaciones(institucion=institucion,cod_estado=0)
            ) / Donacion.get_cantidad_total_donaciones(institucion=institucion)
    
    def get_porcentaje_donaciones_bienes_rechazadas_sobre_total(institucion):
        """"""
        return (Donacion.get_cantidad_total_donaciones(institucion=institucion,tipo='bienes',cod_estado=0)
            ) / Donacion.get_cantidad_total_donaciones(institucion=institucion,tipo='bienes')
    
    def get_porcentaje_donaciones_monetarias_rechazadas_sobre_total(institucion):
        """"""
        return (Donacion.get_cantidad_total_donaciones(institucion=institucion,tipo='monetarias',cod_estado=0)
            ) / Donacion.get_cantidad_total_donaciones(institucion=institucion,tipo='monetarias')
    
    def get_porcentaje_donaciones_pendientes_sobre_total(institucion):
        """"""
        return (Donacion.get_cantidad_total_donaciones(institucion=institucion,tipo='bienes',cod_estado=1)
            + Donacion.get_cantidad_total_donaciones(institucion=institucion,tipo='bienes',cod_estado=2)
            + Donacion.get_cantidad_total_donaciones(institucion=institucion,tipo='monetarias',cod_estado=4)
            ) / Donacion.get_cantidad_total_donaciones(institucion=institucion)
    
    def get_porcentaje_donaciones_bienes_pendientes_sobre_total(institucion):
        """"""
        return (Donacion.get_cantidad_total_donaciones(institucion=institucion,tipo='bienes',cod_estado=1)
            + Donacion.get_cantidad_total_donaciones(institucion=institucion,tipo='bienes',cod_estado=2)
            ) / Donacion.get_cantidad_total_donaciones(institucion=institucion)
    
    def get_porcentaje_donaciones_monetarias_pendientes_sobre_total(institucion):
        """"""
        return (Donacion.get_cantidad_total_donaciones(institucion=institucion,tipo='monetarias',cod_estado=4)
            ) / Donacion.get_cantidad_total_donaciones(institucion=institucion)

    def get_cantidad_total_necesidades_activas(institucion):
        """"""
        return Necesidad.get_cantidad_total_necesidades_activas(institucion=institucion)

    def get_cantidad_total_necesidades_inactivas(institucion):
        """"""
        return Necesidad.get_cantidad_total_necesidades_inactivas(institucion=institucion)
    
    def get_porcentaje_necesidades_activas_sobre_total(institucion):
        """"""
        if Necesidad.get_cantidad_total_necesidades(institucion=institucion) == 0:
            return None
        return Necesidad.get_cantidad_total_necesidades_activas(institucion=institucion)/Necesidad.get_cantidad_total_necesidades(institucion=institucion)

    def get_porcentaje_necesidades_inactivas_sobre_total(institucion):
        """"""
        if Necesidad.get_cantidad_total_necesidades(institucion=institucion) == 0:
            return None
        return Necesidad.get_cantidad_total_necesidades_inactivas(institucion=institucion)/Necesidad.get_cantidad_total_necesidades(institucion=institucion)

    def get_cantidad_necesidades_por_tipo(institucion):
        """"""
        result = {}
        tipo_necesidad = [i[0] for i in Necesidad.TIPOS_NECESIDAD]

        for i in tipo_necesidad:
            result[str(i)] = Necesidad.get_cantidad_total_necesidades(institucion=institucion,tipo=i)

        return result
    
    def get_cantidad_donaciones_bienes_por_tipo_bien_por_estado(institucion):
        result = {}
        tipos_bien = [i[0] for i in Bien.TIPOS_BIEN]

        for tipo_bien in tipos_bien:
            estados_tipo_bien = {}
            codigos_estados = [i[0] for i in Donacion.CODIGOS_ESTADO]

            for codigo_estado in codigos_estados:
                estados_tipo_bien[codigo_estado] = Donacion.get_cantidad_total_donaciones_por_bien(institucion=institucion,cod_estado=codigo_estado,tipo_bien=tipo_bien)

            result[tipo_bien] = estados_tipo_bien

        return result
    
    def get_cantidad_necesidades_por_tipo_por_estado(institucion):
        result = {}
        tipos_necesidad = [i[0] for i in Necesidad.TIPOS_NECESIDAD]

        for i in tipos_necesidad:
            estados_tipo_necesidad = {}
            estados_tipo_necesidad['1'] = Necesidad.get_cantidad_total_necesidades_activas(institucion=institucion,tipo=i)
            estados_tipo_necesidad['0'] = Necesidad.get_cantidad_total_necesidades_inactivas(institucion=institucion,tipo=i)

            result[i] = estados_tipo_necesidad

        return result


class IndicadoresDonante():
    def get_cantidad_total_donaciones(donante):
        # Cantidad total de donaciones de una institucion
        return Donacion.get_cantidad_total_donaciones(donante=donante)
        
    def get_cantidad_donaciones_por_estado(donante):
        """Cantidad de donaciones por estado"""
        result = {}
        codigos_estados = [i[0] for i in Donacion.CODIGOS_ESTADO]

        for i in codigos_estados:
            result[i] = Donacion.get_cantidad_total_donaciones(donante=donante,cod_estado=i)

        return result

    def get_cantidad_donaciones_por_institucion(donante):
        """Cantidad de donaciones por institucion"""
        result = {}
        instituciones = Donacion.get_institucion(donante=donante)

        for institucion in instituciones:
            result[str(institucion)] = Donacion.get_cantidad_total_donaciones(donante=donante,institucion=institucion)

        return result

    def get_cantidad_total_donaciones_bienes(donante):
         # Cantidad total de donaciones de una institucion
        return Donacion.get_cantidad_total_donaciones(donante=donante,tipo='bienes')

    def get_cantidad_donaciones_bienes_por_estado(donante):
        """Cantidad de donaciones por estado"""
        result = {}
        codigos_estados = [i[0] for i in Donacion.CODIGOS_ESTADO]

        for i in codigos_estados:
            result[i] = Donacion.get_cantidad_total_donaciones(donante=donante,tipo='bienes',cod_estado=i)

        return result

    def get_cantidad_donaciones_bienes_por_institucion(donante):
        """Cantidad de donaciones por donante"""
        result = {}
        instituciones = Donacion.get_institucion(donante=donante)

        for institucion in instituciones:
            result[str(institucion)] = Donacion.get_cantidad_total_donaciones(donante=donante,tipo='bienes',institucion=institucion)

        return result

    def get_cantidad_donaciones_bienes_por_tipo_bien(donante):
        """Cantidad de donaciones de bienes agrupado por tipo de bien"""
        result = {}
        tipos_bien = [i[0] for i in Bien.TIPOS_BIEN]

        for tipo_bien in tipos_bien:
            result[tipo_bien] = Donacion.get_cantidad_total_donaciones_por_bien(donante=donante,tipo_bien=tipo_bien)

        return result

    def get_cantidad_total_donaciones_monetarias(donante):
         # Cantidad total de donaciones de una institucion
        return Donacion.get_cantidad_total_donaciones(donante=donante,tipo='monetarias')

    def get_cantidad_donaciones_monetarias_por_estado(donante):
        """Cantidad de donaciones por estado"""
        result = {}
        codigos_estados = [i[0] for i in Donacion.CODIGOS_ESTADO]

        for i in codigos_estados:
            result[i] = Donacion.get_cantidad_total_donaciones(donante=donante,tipo='monetarias',cod_estado=i)

        return result

    def get_cantidad_donaciones_monetarias_por_institucion(donante):
        """Cantidad de donaciones por donante"""
        result = {}
        instituciones = Donacion.get_institucion(donante=donante)

        for institucion in instituciones:
            result[str(institucion)] = Donacion.get_cantidad_total_donaciones(donante=donante,tipo='monetarias',institucion=institucion)

        return result

    def get_monto_donaciones_monetarias(donante):
        """Monto total de todas las donaciones monetarias realizadas para la institución"""
        return Donacion.get_monto_total_donaciones_monetarias(donante=donante)

    def get_monto_donaciones_monetarias_por_estado(donante):
        """Monto total de todas las donaciones monetarias realizadas para la institución
        agrupado por estado"""
        result = {}
        codigos_estados = [i[0] for i in Donacion.CODIGOS_ESTADO]

        for i in codigos_estados:
            result[i] = Donacion.get_monto_total_donaciones_monetarias(donante=donante,cod_estado=i)

        return result

    def get_monto_donaciones_monetarias_por_institucion(donante):
        """Monto total de todas las donaciones monetarias realizadas para la institución
        agrupado por donante"""
        result = {}
        instituciones = Donacion.get_institucion(donante=donante)

        for institucion in instituciones:
            result[str(institucion)] = Donacion.get_monto_total_donaciones_monetarias(donante=donante,institucion=institucion)

        return result

    def get_porcentaje_donaciones_entregadas_sobre_total(donante):
        """"""
        return (
            Donacion.get_cantidad_total_donaciones(donante=donante,tipo='monetarias',cod_estado=3)
            + Donacion.get_cantidad_total_donaciones(donante=donante,tipo='bienes',cod_estado=5)
            ) / Donacion.get_cantidad_total_donaciones(donante=donante)
    
    def get_porcentaje_donaciones_bienes_entregadas_sobre_total(donante):
        """"""
        return (Donacion.get_cantidad_total_donaciones(donante=donante,tipo='bienes',cod_estado=5)
            ) / Donacion.get_cantidad_total_donaciones(donante=donante,tipo='bienes')
    
    def get_porcentaje_donaciones_monetarias_entregadas_sobre_total(donante):
        """"""
        return (Donacion.get_cantidad_total_donaciones(donante=donante,tipo='monetarias',cod_estado=3)
            ) / Donacion.get_cantidad_total_donaciones(donante=donante,tipo='monetarias')

    def get_porcentaje_donaciones_rechazadas_sobre_total(donante):
        """"""
        return (Donacion.get_cantidad_total_donaciones(donante=donante,cod_estado=0)
            ) / Donacion.get_cantidad_total_donaciones(donante=donante)
    
    def get_porcentaje_donaciones_bienes_rechazadas_sobre_total(donante):
        """"""
        return (Donacion.get_cantidad_total_donaciones(donante=donante,tipo='bienes',cod_estado=0)
            ) / Donacion.get_cantidad_total_donaciones(donante=donante,tipo='bienes')
    
    def get_porcentaje_donaciones_monetarias_rechazadas_sobre_total(donante):
        """"""
        return (Donacion.get_cantidad_total_donaciones(donante=donante,tipo='monetarias',cod_estado=0)
            ) / Donacion.get_cantidad_total_donaciones(donante=donante,tipo='monetarias')
    
    def get_porcentaje_donaciones_pendientes_sobre_total(donante):
        """"""
        return (Donacion.get_cantidad_total_donaciones(donante=donante,tipo='bienes',cod_estado=1)
            + Donacion.get_cantidad_total_donaciones(donante=donante,tipo='bienes',cod_estado=2)
            + Donacion.get_cantidad_total_donaciones(donante=donante,tipo='monetarias',cod_estado=4)
            ) / Donacion.get_cantidad_total_donaciones(donante=donante)
    
    def get_porcentaje_donaciones_bienes_pendientes_sobre_total(donante):
        """"""
        return (Donacion.get_cantidad_total_donaciones(donante=donante,tipo='bienes',cod_estado=1)
            + Donacion.get_cantidad_total_donaciones(donante=donante,tipo='bienes',cod_estado=2)
            ) / Donacion.get_cantidad_total_donaciones(donante=donante)
    
    def get_porcentaje_donaciones_monetarias_pendientes_sobre_total(donante):
        """"""
        return (Donacion.get_cantidad_total_donaciones(donante=donante,tipo='monetarias',cod_estado=4)
            ) / Donacion.get_cantidad_total_donaciones(donante=donante)
    
    def get_cantidad_donaciones_bienes_por_tipo_bien_por_estado(donante):
        result = {}
        tipos_bien = [i[0] for i in Bien.TIPOS_BIEN]

        for tipo_bien in tipos_bien:
            estados_tipo_bien = {}
            codigos_estados = [i[0] for i in Donacion.CODIGOS_ESTADO]

            for codigo_estado in codigos_estados:
                estados_tipo_bien[codigo_estado] = Donacion.get_cantidad_total_donaciones_por_bien(donante=donante,cod_estado=codigo_estado,tipo_bien=tipo_bien)

            result[tipo_bien] = estados_tipo_bien

        return result