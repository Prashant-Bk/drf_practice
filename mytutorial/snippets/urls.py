from django.urls import path 
from .views import (SnippetList,
                    SnippetDetail,
                    UserList,
                    UserRetrieve,
                    make_request)

urlpatterns = [
    path('snippets/', SnippetList.as_view() , name = "snippet_list"),
    path('snippets/<int:pk>/', SnippetDetail.as_view() , name = "snippet_detail"),
    path('users/',UserList.as_view() , name = "user_list" ),
    path('users/<int:pk>/',UserRetrieve.as_view() , name = "user_list" ),
    path('make_request/' , make_request)
]


