from DonacionesApp.models import Donacion

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

    # def get_monto_donaciones_monetarias(institucion):
    #     """"""
    #     return Donacion.get_monto_total_donaciones_monetarias(institucion=institucion)

    # def get_monto_donaciones_monetarias_por_estado(institucion):
    #     """"""

    # def get_monto_donaciones_monetarias_por_donante(institucion):
    #     """"""