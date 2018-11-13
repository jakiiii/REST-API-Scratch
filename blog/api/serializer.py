from rest_framework import serializers

from blog.models import Blog


class BlogSerializers(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            'pk',
            'user',
            'title',
            'content',
            'timestamp'
        ]


# Serializers Doing two things
#   - Convert Data to JSON
#   - Validation to data passed
