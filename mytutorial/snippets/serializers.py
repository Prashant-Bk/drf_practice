from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Snippet , Project

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.HyperlinkedRelatedField(view_name='user-detail', read_only=True)   
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', lookup_field='pk', format='html')

    class Meta:
        model = Snippet
        fields = ['url', 'id', 'owner',
                  'title', 'code','highlight','linenos', 'language', 'style']
        extra_kwargs = {
            'url': {'view_name': 'snippet-detail'}
        }
         

class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)
    highlights = serializers.HyperlinkedIdentityField(
        view_name='user-highlights',
        lookup_field = "pk",
        format='html' )

    class Meta:
        model = User
        fields = ['url', 'pk', 'username' , 'snippets' , 'highlights' ]
        extra_kwargs = {
            'url': {'view_name': 'user-detail'} , 
        }
        
        
        
        
class ProjectSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedIdentityField(many = True , view_name = "snippet-detail")
    class Meta:
        model = Project
        fields = ['url','title' , 'created' , 'image', 'snippets']
        # extra_kwargs = {
        #     'url': {'view_name': 'project-detail'} , 
        # }
        read_only_fields = ['created']
        