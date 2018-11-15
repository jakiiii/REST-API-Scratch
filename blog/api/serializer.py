from rest_framework import serializers

from blog.models import Blog


class BlogSerializers(serializers.ModelSerializer):
    # uri = serializers.CharField(read_only=True, source='get_api_url')
    uri = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Blog
        fields = [
            'uri',
            'id',
            'user',
            'title',
            'content',
            'timestamp',
        ]
        read_only_fields = ['id', 'user']

    def get_uri(self, obj):
        request = self.context.get('request')
        return obj.get_api_url(request=request)

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
