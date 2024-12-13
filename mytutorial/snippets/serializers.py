from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Snippet

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(view_name='user_detail', read_only=True)   
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet_highlighted', lookup_field='pk', format='html')

    class Meta:
        model = Snippet
        fields = ['url', 'id', 'owner',
                  'title', 'code','highlight','linenos', 'language', 'style']
        extra_kwargs = {
            'url': {'view_name': 'snippet_detail_fun'}
        }
         

class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet_detail_fun', read_only=True)
    highlights = serializers.HyperlinkedIdentityField(
        view_name='user_highlights',
        lookup_field = "username",
        format='html' )

    class Meta:
        model = User
        fields = ['url', 'pk', 'username' , 'snippets' , 'highlights']
        extra_kwargs = {
            'url': {'view_name': 'user_detail'} , 
        }
         