from django.http import HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import viewsets, permissions, status, mixins
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from blog.models import *
from blog.permissions import IsOwnerOrReadOnly
from blog.serializers import *


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]
#
#
# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]

class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BlogPostReplyViewSet(mixins.CreateModelMixin,
                           mixins.RetrieveModelMixin,
                           # mixins.UpdateModelMixin,
                           # mixins.DestroyModelMixin,
                           GenericViewSet):
    queryset = BlogPostComment.objects.all()
    serializer_class = SubCommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@ensure_csrf_cookie
def csrf_view(request):
    return HttpResponse('ok')
