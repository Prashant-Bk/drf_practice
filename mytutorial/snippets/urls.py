from django.urls import path 
from .views import (SnippetList,
                    SnippetDetail,
                    UserList,
                    UserRetrieve,
                    SnippetHighlight,
                    api_root,
                    make_request ,
                    get_users_highlights)

urlpatterns = [
    path('',api_root , name = "api_root") , 
    path('snippets/', SnippetList.as_view() , name = "snippet_list"),
    path('snippets/<int:pk>/', SnippetDetail.as_view() , name = "snippet_detail_fun"),
    path('snippets/<int:id>/highlight/', SnippetHighlight.as_view() , name = "snippet_highlighted"),
    path('users/',UserList.as_view() , name = "user_list" ),
    path('users/<int:pk>/',UserRetrieve.as_view() , name = "user_detail" ),
    path('snippets/<str:username>/highlights/',get_users_highlights , name = "user_highlights" ),
    path('request_info/' , make_request)
]


