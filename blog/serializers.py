from typing import List

import typing
from django.contrib.auth.models import User, Group
from drf_spectacular.helpers import lazy_serializer
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers, permissions
from rest_framework.fields import empty

from blog.models import BlogPost, BlogPostComment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'blogposts', 'first_name', 'last_name']
        permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']


class CommentSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField(
        read_only=True, method_name="get_comments")

    owner = UserSerializer(many=False, read_only=True)
    blogpost = serializers.PrimaryKeyRelatedField(many=False, queryset=BlogPost.objects.all())
    parent_comment = serializers.PrimaryKeyRelatedField(many=False, queryset=BlogPostComment.objects.all(),
                                                        write_only=True, required=False)

    class Meta:
        model = BlogPostComment
        fields = ('id', 'comments', 'created', 'owner', 'body', "blogpost", "parent_comment")

    def get_comments(self, obj):
        # check if current comment is a root node.
        children = BlogPostComment.objects.get(pk=obj.id).get_children()
        serializer = CommentSerializer(instance=children, many=True)
        return serializer.data

    def create(self, validated_data):
        parent_comment = validated_data.get('parent_comment', None)
        validated_data.pop('parent_comment', None)
        if parent_comment is not None:
            # we know at this point that the parent comment exists and the comment we would add is valid, so we can
            # add the child comment
            new_comment = parent_comment.add_child(**validated_data)
        else:
            # If the parent comment is None, then we are creating a new root
            new_comment = BlogPostComment.add_root(**validated_data)

        return new_comment


class BlogPostSerializer(serializers.ModelSerializer):
    owner = UserSerializer(many=False, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'subtitle', 'created', 'body', 'owner', 'comments']
