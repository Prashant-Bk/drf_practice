from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

class SnippetSerializer(serializers.ModelSerializer):
          
    class Meta:
        model = Snippet
        fields = ['id', 'title','created', 'code', 'linenos', 'language', 'style']
        read_only_fields = [ 'created'] 