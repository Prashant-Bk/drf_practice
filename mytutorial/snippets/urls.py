from django.urls import path 
from rest_framework import renderers
from .views import (SnippetViewSet,
                    UserViewSet,
                    api_root,
                    make_request ,
)

snippet_list = SnippetViewSet.as_view({
    'get':'list',
    'post':'create'
})
snippet_detai = SnippetViewSet.as_view({
    'get':'retrieve',
    'put':'update',
    'patch':'partial_update',
    'delete':'destroy'
})
snippet_highlight = SnippetViewSet.as_view({
    'get':'highlight',
}, renderer_classes=[renderers.StaticHTMLRenderer])
user_list = UserViewSet.as_view({
    'get':'list'
})
user_detail = UserViewSet.as_view({
    'get':'retrieve'
})
get_users_highlights = UserViewSet.as_view({
    'get':'get_users_highlights'
}, renderer_classes=[renderers.StaticHTMLRenderer])

urlpatterns = [
    path('',api_root , name = "api_root") , 
    path('snippets/',snippet_list , name = "snippet_list"),
    path('snippets/<int:pk>/', snippet_detai , name = "snippet_detail_fun"),
    path('snippets/<int:pk>/highlight/', snippet_highlight , name = "snippet_highlighted"),
    path('users/',user_list, name = "user_list" ),
    path('users/<int:pk>/',user_detail, name = "user_detail" ),
    path('snippets/<str:username>/highlights/',get_users_highlights , name = "user_highlights" ),
    path('request_info/' , make_request)
]


