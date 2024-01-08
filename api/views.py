from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from rest_framework import permissions


# region APIVIEW CBV
class PostListView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PostSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'status': serializer.errors})


class PostDetailView(APIView):

    def get_post(self, request, slug):
        try:
            return Post.objects.get(slug=slug)
        except Post.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND})

    def get(self, request, slug):

        post = self.get_post(request, slug)

        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, slug):
        post = self.get_post(request, slug)

        serializer = PostSerializer(data=request.data, instance=post)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, slug):
        post = self.get_post(request, slug)
        post.delete()
        return Response({'message': 'deleting post successfully'}, status=status.HTTP_200_OK)


# endregion

# region MIXINS
class PostListViewGenerics(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailApiViewGenerics(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# endregion

# region VIEWSETS

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [permissions.IsAuthenticated]
# endregion
