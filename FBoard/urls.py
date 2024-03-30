from django.urls import path
from .views import (PostList, PostDetail, PostCreate, PostUpdate, PostDelete, ResponseCreate, Responses,
                    response_accept, response_delete, )

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('<int:pk>/response/create/', ResponseCreate.as_view(), name='response_create'),
    path('responses/', Responses.as_view(), name='responses'),
    path('response/accept/<int:pk>', response_accept, name='response_accept'),
    path('response/delete/<int:pk>', response_delete, name='response_delete'),
   # path('subscriptions/', subscriptions, name='subscriptions'),
]