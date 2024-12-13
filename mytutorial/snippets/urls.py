from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (SnippetViewSet,
                    UserViewSet,
                    api_root,
                    make_request ,
)



# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'snippets', SnippetViewSet, basename='snippet')
router.register(r'users', UserViewSet, basename='user')

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('',api_root , name = "api_root") , 
    path('router/', include(router.urls)),
     path('request_info/' , make_request)
]
