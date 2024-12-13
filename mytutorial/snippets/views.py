from snippets.models import Snippet 
from django.contrib.auth.models import User
from snippets.serializers import SnippetSerializer
from snippets.serializers import  UserSerializer
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view , renderer_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import action


@api_view(http_method_names=["GET"])
def api_root(request , format = None):
    username = request.user.username
    return Response(
        data = {
            "snippet":reverse("snippet_list", request=request, format=format),
            "user":reverse("user_list", request=request, format=format),
            "request info":reverse(make_request, request=request, format=format),
            "my highlights":reverse('user_highlights' ,args=[username], request=request, format=format)
        })
    

class SnippetViewSet(viewsets.ModelViewSet):
    """
    This ViewSet automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    @action(detail=True) #get detail of a object using pk
    def highlight(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


            
        
        
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    
    
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `retrieve` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail= False , renderer_classes = [renderers.StaticHTMLRenderer] )
    def get_users_highlights(self, request, *args, **kwargs):
        username = kwargs["username"]
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