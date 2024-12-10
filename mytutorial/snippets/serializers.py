from rest_framework import serializers
from snippets.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User


class SnippetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    class Meta:
        model = Snippet
        fields = ['id','owner', 'title','created', 'code', 'linenos', 'language', 'style']
        read_only_fields = [ 'created'] 

class UserSerializer(serializers.ModelSerializer):
    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())
    # The 'snippets' field is a reverse relationship on User, so it must be explicitly added to the serializer.
    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']
         