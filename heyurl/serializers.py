from rest_framework_json_api import serializers
from django.contrib.sites.models import Site

from heyurl.models import Url, Click


class ClickSerializer(serializers.ModelSerializer):
    class Meta:
        model = Click
        fields = ('created_at', 'browser', 'platform')


class UrlSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(source='short_url', read_only=True)
    metrics = serializers.ResourceRelatedField(many=True, read_only=True, source='click_set')

    def get_url(self, instace):
        return "".join(["http://", Site.objects.get_current().domain, "/", instace.short_url])

    class Meta:
        model = Url
        fields = ('created_at', 'original_url', 'url', 'clicks', 'metrics')
