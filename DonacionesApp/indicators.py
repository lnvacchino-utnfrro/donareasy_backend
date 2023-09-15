from DonacionesApp.models import Donacion, Bien, Necesidad

class IndicadoresInstitucion():
    def get_cantidad_total_donaciones(institucion):
        # Cantidad total de donaciones de una institucion
        return Donacion.get_cantidad_total_donaciones(institucion=institucion)
        
    def get_cantidad_donaciones_por_estado(institucion):
        """Cantidad de donaciones por estado"""
        result = []
        codigos_estados = [i[0] for i in Donacion.CODIGOS_ESTADO]

        for i in codigos_estados:
            cantidad_por_estado = (i,Donacion.get_cantidad_total_donaciones(institucion=institucion,cod_estado=i))
            result.append(cantidad_por_estado)

        return result

    def get_cantidad_donaciones_por_donante(institucion):
        """Cantidad de donaciones por donante"""
        result = []
        donantes = Donacion.get_donantes(institucion=institucion)

        for donante in donantes:
            cantidad_por_donante = (str(donante),Donacion.get_cantidad_total_donaciones(institucion=institucion,donante=donante))
            result.append(cantidad_por_donante)

        return result

    def get_cantidad_total_donaciones_bienes(institucion):
         # Cantidad total de donaciones de una institucion
        return Donacion.get_cantidad_total_donaciones(institucion=institucion,tipo='bienes')

    def get_cantidad_donaciones_bienes_por_estado(institucion):
        """Cantidad de donaciones por estado"""
        result = []
        codigos_estados = [i[0] for i in Donacion.CODIGOS_ESTADO]

        for i in codigos_estados:
            cantidad_por_estado = (i,Donacion.get_cantidad_total_donaciones(institucion=institucion,tipo='bienes',cod_estado=i))
            result.append(cantidad_por_estado)

        return result

    def get_cantidad_donaciones_bienes_por_donante(institucion):
        """Cantidad de donaciones por donante"""
        result = []
        donantes = Donacion.get_donantes(institucion=institucion)

        for donante in donantes:
            cantidad_por_donante = (str(donante),Donacion.get_cantidad_total_donaciones(institucion=institucion,tipo='bienes',donante=donante))
            result.append(cantidad_por_donante)

        return result

    def get_cantidad_donaciones_bienes_por_tipo_bien(institucion):
        """Cantidad de donaciones de bienes agrupado por tipo de bien"""
        result = []
        tipos_bien = [i[0] for i in Bien.TIPOS_BIEN]

        for tipo_bien in tipos_bien:
            cantidad_por_tipo_bien = (tipo_bien,Donacion.get_cantidad_total_donaciones_por_bien(institucion=institucion,tipo_bien=tipo_bien))
            result.append(cantidad_por_tipo_bien)

        return result

    def get_cantidad_total_donaciones_monetarias(institucion):
         # Cantidad total de donaciones de una institucion
        return Donacion.get_cantidad_total_donaciones(institucion=institucion,tipo='monetarias')

    def get_cantidad_donaciones_monetarias_por_estado(institucion):
        """Cantidad de donaciones por estado"""
        result = []
        codigos_estados = [i[0] for i in Donacion.CODIGOS_ESTADO]

        for i in codigos_estados:
            cantidad_por_estado = (i,Donacion.get_cantidad_total_donaciones(institucion=institucion,tipo='monetarias',cod_estado=i))
            result.append(cantidad_por_estado)

        return result

    def get_cantidad_donaciones_monetarias_por_donante(institucion):
        """Cantidad de donaciones por donante"""
        result = []
        donantes = Donacion.get_donantes(institucion=institucion)

        for donante in donantes:
            cantidad_por_donante = (str(donante),Donacion.get_cantidad_total_donaciones(institucion=institucion,tipo='monetarias',donante=donante))
            result.append(cantidad_por_donante)

        return result

    def get_monto_donaciones_monetarias(institucion):
        """Monto total de todas las donaciones monetarias realizadas para la institución"""
        return Donacion.get_monto_total_donaciones_monetarias(institucion=institucion)

    def get_monto_donaciones_monetarias_por_estado(institucion):
        """Monto total de todas las donaciones monetarias realizadas para la institución
        agrupado por estado"""
        result = []
        codigos_estados = [i[0] for i in Donacion.CODIGOS_ESTADO]

        for i in codigos_estados:
            monto_por_estado = (i,Donacion.get_monto_total_donaciones_monetarias(institucion=institucion,cod_estado=i))
            result.append(monto_por_estado)

        return result

    def get_monto_donaciones_monetarias_por_donante(institucion):
        """Monto total de todas las donaciones monetarias realizadas para la institución
        agrupado por donante"""
        result = []
        donantes = Donacion.get_donantes(institucion=institucion)

        for donante in donantes:
            cantidad_por_donante = (str(donante),Donacion.get_monto_total_donaciones_monetarias(institucion=institucion,donante=donante))
            result.append(cantidad_por_donante)

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
    
# //NECESIDADES
# Cantidad total activas
# Cantidad total registradas
# Cantidad total agrupado por tipo

    def get_cantidad_total_necesidades_activas(institucion):
        """"""
        return Necesidad.get_cantidad_total_necesidades_activas(institucion=institucion)

    def get_cantidad_total_necesidades_inactivas(institucion):
        """"""
        return Necesidad.get_cantidad_total_necesidades_inactivas(institucion=institucion)
    
    def get_porcentaje_necesidades_activas_sobre_total(institucion):
        """"""
        return Necesidad.get_cantidad_total_necesidades_activas(institucion=institucion)/Necesidad.get_cantidad_total_necesidades(institucion=institucion)

    def get_porcentaje_necesidades_inactivas_sobre_total(institucion):
        """"""
        return Necesidad.get_cantidad_total_necesidades_inactivas(institucion=institucion)/Necesidad.get_cantidad_total_necesidades(institucion=institucion)

    def get_cantidad_necesidades_por_tipo(institucion):
        """"""
        result = []
        codigos_estados = [i[0] for i in Necesidad.TIPOS_NECESIDAD]

        for i in codigos_estados:
            cantidad_por_tipo = (str(i),Necesidad.get_cantidad_total_necesidades(institucion=institucion,tipo=i))
            result.append(cantidad_por_tipo)
        return result
