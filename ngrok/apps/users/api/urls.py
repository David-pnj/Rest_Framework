from django.urls import path
from apps.users.api.api import user_api_view,user_detail_api_view  #UserAPIiew

urlpatterns = [
    path('usuario/', user_api_view, name = 'usuario_api'), # 
   # path('usuario/', UserAPIiew.as_view(), name = 'usuario_api') # al ser una clase se añadia el as_view() cuando se tratan de funciones no hace falta
    path('usuario/<int:pk>/', user_detail_api_view, name= "user_detail_api_view")
]