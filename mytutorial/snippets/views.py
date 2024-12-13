from snippets.models import Snippet ,Project
from django.contrib.auth.models import User
from snippets.serializers import SnippetSerializer , ProjectSerializer
from snippets.serializers import  UserSerializer
from rest_framework import generics
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view , renderer_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework.decorators import action

class ProjectListView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectDetailView(generics.RetrieveUpdateAPIView):
    lookup_field = 'pk'
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


@api_view(http_method_names=["GET"])
def api_root(request , format = None):
    username = request.user.username
    return Response(
        data = {
            "snippet":reverse("snippet-list", request=request, format=format),
            "user":reverse("user-list", request=request, format=format),
            "request info":reverse(make_request, request=request, format=format),
            "projects":reverse('project-list' , request=request, format=format),
            "my highlights":reverse('user-highlights' ,args=[username], request=request, format=format)
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

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
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
    
    @action(detail= True , renderer_classes = [renderers.StaticHTMLRenderer] )
    def highlights(self, request, *args, **kwargs):
        pk = kwargs["pk"]
        user = User.objects.get(id = pk)
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