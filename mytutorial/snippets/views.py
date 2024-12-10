from snippets.models import Snippet 
from django.contrib.auth.models import User
from snippets.serializers import SnippetSerializer , UserSerializer
from rest_framework import generics

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


class SnippetList(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    
    def perform_create(self, serializer):  #over riding perform_create with owner equals to current user 
     serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    
class UserList(generics.ListAPIView): #adding read only views
    queryset = User.objects.all()
    serializer_class = UserSerializer
 
class UserRetrieve(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


from django.shortcuts import HttpResponse
from django.http import request as http_request

@api_view(http_method_names=["GET"])
def make_request(http_request):
    print("http request made successfully")
    print("\nrequest: ", http_request)
    print("\ntype(request): ", type(http_request))
    print("\nuser: ", http_request.user )
    print("\ntype(user): ", type(http_request.user) )
    
    data = {
        "request":       str(http_request) , 
        "type(request)": str( type(http_request)) , 
        "user":          str(http_request.user)  , 
        "type(user)":    str(type(http_request.user)) ,
        }
    return Response(data , status = status.HTTP_200_OK)