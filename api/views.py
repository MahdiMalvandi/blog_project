from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from .serializers import *


@api_view(['GET', 'POST'])
def all_posts(request: Request):
    """
    Get all posts or add a new one
    :param request:
    :return:
    """

    if request.method == 'GET':
        post = Post.objects.all()
        serialized = PostSerializer(post, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serialized = PostSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)