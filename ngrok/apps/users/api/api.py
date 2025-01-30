from rest_framework.views import APIView # ya no se llama view sino apiview
from apps.users.models import User
from apps.users.api.serializers import UserSerializer, TestUserSerializer 
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view #para usar las funciones como en django necesitamos usar decoradores del fraework de rest, api view es un decorador

# se gun vayas poniendo los metodos guardados en api_view nos saldra su plantilla
@api_view(['GET', 'POST'] ) # decorador @ view ha q pasarle 2 cosas: metodos http q tienen esta funcion, dentro de la lista
def user_api_view(request): #nombre de la funcion es el titulo  #recibe la herencia de API view, ahora al no ser una clase sino una funcion recibe request en lucar de APIView

    #list
    if request.method == 'GET': #def get(get,request): # peticion q me envie cualquier front cuando teniamos la clase
        users = User.objects.all()  # es decir todos los usuarios, no devulve un unico valor sino un listado de valores
        users_serializer = UserSerializer(users, many=True) # y le paso la consulta, como tiene varios valores usamos "many", convertirá a json cada uno d elos elementos del listado
        print(TestUserSerializer())
        test_data ={ # crear una instancia de testuserserializer y enviarle una informacion de prueba
            'name': 'develop',
            'email': 'develop@gmail.com'
        }        
        test_user = TestUserSerializer(data = test_data, context = test_data ) # context en caso de que queramos comparar valores dentro del modelo  otras opciones
        if test_user.is_valid():
            print('Paso validaciones')
        else:
            print(test_user.errors)

        return Response(users_serializer.data, status=status.HTTP_200_OK) # no puedes enviar la variable de forma directa se encuantra en un atributo llamado data
    
    #create
    elif request.method == 'POST':
        #print(request.data)
        user_serializer = UserSerializer(data = request.data) # pilla la informacion con request data y la serializamos
        
        #validacion
        if user_serializer.is_valid(): # hacemos una validacion, si esta correcto avanzamos
            user_serializer.save() # y lo guardamos
            return Response({'message':'Usuario creado correctamente!'}, status = status.HTTP_201_CREATED) # cuando el serializador guarda la info la pone en una varibale llamada DATA, user_serializer.data, poner los datos del usuario creado o un mensaje simple {'message':'Usuario Eliminado correctamente!'}
#DATA PUEDE guardar: la informacion serializada cuando se envia una serie de parametros para get y la creacion de la informacion tambien serializada 
# se registra se serializa y se manda a data
        return Response(user_serializer.errors, status = status.HTTP_400_BAD_REQUEST) # en caso de que surja un error, como poner el mismo correo electronico o nombre.. pueden ser mas de uno
    

@api_view(['GET', 'PUT', 'DELETE'])
def user_detail_api_view(request,pk): #el pk lo introduce en la url, 1 el primer user, 2 el segundo-...
    
    #pk primary key,   queryset, todo sobre la misma consulta, se basa en la pk
    user = User.objects.filter(id = pk ).first()

    #validacion
    if user: 

        if request.method =='GET':
            #user = User.objects.filter(id = pk ).first() # filtra de entre todos los obejtos del usuario hasta dar con el id(el primer elemento)
            # si no encuentra nada devuelve una cadena vacia
            user_serializer = UserSerializer(user) # no ponemos "many" pues se trata de un solo valor
            return Response(user_serializer.data, status = status.HTTP_200_OK) #serializer.data para siempre a cceder a la info dentro del serializer (igual que .text si fuera un string o .json() asus respectivos datos)
        
        elif request.method == 'PUT':
            #user = User.objects.filter(id = pk).first() añadimos un caso comun arriba del if 
            user_serializer = UserSerializer(user,data = request.data)
            if user_serializer.is_valid():
                user_serializer.save() # viene ya la accion realizada de rest framework, es decir estamos sobreescribiendo el dato en el campo automaticamente
                return Response(user_serializer.data,  status = status.HTTP_200_OK)
            return Response(user_serializer.errors,  status = status.HTTP_400_BAD_REQUEST)

        elif request.method== 'DELETE':
            #user = User.objects.filter(id = pk ).first()      
            user.delete()  # viene ya la accion realizada por restframework
            return Response({'message':'Usuario Eliminado correctamente!'},status = status.HTTP_200_OK )   #no podemos enseñar los datos obviamente por lo que ponemos un mensaje

    return Response({'message':'No se ha encontrado un usuario con estos datos'},status = status.HTTP_400_BAD_REQUEST )    # en caso de que no haya usuario con esos datos
