from snippets.models import Snippet 
from django.contrib.auth.models import User
from snippets.serializers import SnippetSerializer , UserSerializer
from rest_framework import generics
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly



class SnippetList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    #if user is authenticated it can read and write else read only
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    
    def perform_create(self, serializer):  #over riding perform_create with owner equals to current user 
     serializer.save(owner=self.request.user)


class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly]
    #IsOwnerOrReadOnly => only the owner could make changes if not owner then read only
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    
    
class UserList(generics.ListAPIView): #adding read only views
    queryset = User.objects.all()
    serializer_class = UserSerializer
 
class UserRetrieve(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    

# for checking current request and user
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


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