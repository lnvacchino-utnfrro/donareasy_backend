from rest_framework.permissions import BasePermission

class IsInstitucionPermission(BasePermission):
    """Permiso global que valida si el usuario es una institución"""
    message = 'Esta página sólo es permitida para las institucines'

    def has_permission(self,request,view):
        group = request.user.groups.first()
        return group is not None and group.id == 2


class IsDonantePermission(BasePermission):
    """Permiso global que valida si el usuario es un donante"""
    message = 'Esta página sólo es permitida para los donantes'

    def has_permission(self,request,view):
        group = request.user.groups.first()
        return group is not None and group.id == 1


class IsCadetePermission(BasePermission):
    """Permiso global que valida si el usuario es un cadete"""
    message = 'Esta página sólo es permitida para los cadetes'

    def has_permission(self,request,view):
        group = request.user.groups.first()
        return group is not None and group.id == 3
        