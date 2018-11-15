from rest_framework import generics, mixins

from django.db.models import Q

from blog.models import Blog
from .serializer import BlogSerializers
from .permission import IsOwnerOrReadOnly


# Create your api views here.
class BlogPostAPIView(generics.CreateAPIView):
    lookup_field = 'pk'
    serializer_class = BlogSerializers

    def get_queryset(self):
        return Blog.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BlogPostListAPIView(mixins.CreateModelMixin, generics.ListAPIView):
    lookup_field = 'pk'
    serializer_class = BlogSerializers

    def get_queryset(self):
        qs = Blog.objects.all()
        query = self.request.GET.get('q')
        if query is not None:
            qs = qs.filter(
                Q(title__icontains=query) | Q(content__contains=query)
            )
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}


class BlogPostRudView(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'pk'
    serializer_class = BlogSerializers
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Blog.objects.all()

    def get_serializer_context(self, *args, **kwargs):
        return {"request": self.request}
