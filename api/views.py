from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import permissions


# region APIVIEW CBV
class PostListView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PostCreateUpdateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            thumbnail = request.data.get('thumbnail')
            if thumbnail:
                serializer.validated_data['thumbnail'] = thumbnail

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'status': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()

    serializer_class = PostSerializer
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return PostCreateUpdateSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=['get'])
    def get_by_slug(self, request, slug=None):
        post = Post.objects.get(slug=slug)
        serializer = self.get_serializer(post)
        return Response(serializer.data)



# class PostDetailView(APIView):
#
#     def get_post(self, request, slug):
#         try:
#             return Post.objects.get(slug=slug)
#         except Post.DoesNotExist:
#             return Response(data={'status': status.HTTP_404_NOT_FOUND})
#
#     def get(self, request, slug):
#
#         post = self.get_post(request, slug)
#
#         serializer = PostSerializer(post)
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     def put(self, request, slug):
#         post = self.get_post(request, slug)
#         serializer = PostCreateSerializer(data=request.data, instance=post)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response({'status': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


    # def delete(self, request, slug):
    #     post = self.get_post(request, slug)
    #     post.delete()
    #     return Response({'message': 'deleting post successfully'}, status=status.HTTP_200_OK)


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
