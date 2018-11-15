from django.urls import path
from .views import (
    BlogPostRudView,
    BlogPostAPIView,
    BlogPostListAPIView
)


urlpatterns = [
    path('', BlogPostAPIView.as_view(), name='post-create'),
    path('list/', BlogPostListAPIView.as_view(), name='post-list'),
    path('<int:pk>/', BlogPostRudView.as_view(), name='post-rud'),
]
