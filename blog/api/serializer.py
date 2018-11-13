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
        read_only_fields = ['pk', 'user']

        def validate_title(self, value):
            qs = Blog.objects.filter(title__iexact=value)
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise serializers.ValidationError("This title has been used already.")
            return value


# Serializers Doing two things
#   - Convert Data to JSON
#   - Validation to data passed
