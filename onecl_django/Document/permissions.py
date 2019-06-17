from rest_framework import permissions
from User.models import CustomUser
from Club.models import Club
from Join.models import Join
from .models import DocumentType, Document


class DocumentListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = CustomUser.objects.get(username=request.user.username)
        club = None
        if request.method == 'GET':
            club = Club.objects.get(id=request.GET.get('club'))
        elif request.method == 'POST':
            club = Club.objects.get(id=request.data['club'])
        try:
            join = Join.objects.get(user=user, club=club)
        except Join.DoesNotExist:
            return False

        if request.method == 'GET':
            return True

        if request.method == 'POST':
            doc_type = DocumentType.objects.get(id=request.data['type'])
            if doc_type.club is None:
                if doc_type.name == 'notice':
                    return join.auth_level > 1
            return True


class DocumentDetailPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = CustomUser.objects.get(username=request.user.username)
        club = obj.club
        try:
            join = Join.objects.get(user=user, club=club)
        except Join.DoesNotExist:
            return False

        if request.method == 'GET':
            return True
        if request.method == 'PUT':
            return obj.owner == user
        if request.method == 'DELETE':
            return obj.owner == user or join.auth_level >= 2


class DocumentTypeListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = CustomUser.objects.get(username=request.user.username)
        club = None
        if request.method == 'GET':
            club = Club.objects.get(id=request.GET.get('club'))
        elif request.method == 'POST':
            club = Club.objects.get(id=request.data['club'])
        try:
            join = Join.objects.get(user=user, club=club)
        except Join.DoesNotExist:
            return False

        if request.method == 'GET':
            return True

        if request.method == 'POST':
            return join.auth_level > 1


class DocumentTypeDetailPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = CustomUser.objects.get(username=request.user.username)
        club = obj.club
        try:
            join = Join.objects.get(user=user, club=club)
        except Join.DoesNotExist:
            return False

        return join.auth_level > 1


class CommentListPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if request.method == 'POST':
            document = Document.objects.get(id=request.data['document'])
            user = CustomUser.objects.get(username=request.user.username)
            try:
                join = Join.objects.get(club=document.club, user=user)
            except Join.DoesNotExist:
                return False
            return True


class CommentDetailPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        owner = CustomUser.objects.get(username=request.user.username)
        return obj.owner == owner
