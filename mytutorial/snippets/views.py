from snippets.models import Snippet 
from django.contrib.auth.models import User
from snippets.serializers import SnippetSerializer
from snippets.serializers import  UserSerializer
from rest_framework import generics
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view , renderer_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers

from django.http import HttpRequest 




@api_view(http_method_names=["GET"])
def api_root(request , format = None):
    username = request.user.username
    return Response(
        data = {
            "snippet":reverse("snippet_list", request=request, format=format),
            "user":reverse("user_list", request=request, format=format),
            "request info":reverse(make_request, request=request, format=format),
            "my highlights":reverse(get_users_highlights ,args=[username], request=request, format=format)
        })
    
      
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
    
    
class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = [renderers.StaticHTMLRenderer]
    lookup_field = "id"
    
    def get(self, request, *args, **kwargs):
        snippet = self.get_object() #use pk here
        print(snippet.highlighted)
        return Response([snippet.highlighted])
        
       
    
#To get all the highlighted snippets of a user
@api_view(http_method_names=["GET"])
@renderer_classes([renderers.StaticHTMLRenderer])
#applying html renderer to @api based view
def get_users_highlights(request , username):
    user = User.objects.get(username = username)
    user_snippets = user.snippets.all()
    user_snippets_highlighted = [snippet.highlighted for snippet in user_snippets]
    return Response(user_snippets_highlighted)


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