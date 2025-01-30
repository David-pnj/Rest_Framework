from rest_framework import serializers
from apps.users.models import User

#convierte una instancia de un modelo especifico o una estructura de django la convierte en una estructura de json para devolverla con un reponse

class UserSerializer(serializers.ModelSerializer): # este serializador me transforma cualquier estructura modelo usuario a json
	class Meta: #q convierte json en una consulta, que retorne una instancia o varias instancias del tipo de modelo q lleve asocidado (usuario en este caso)
		model = User
		fields = '__all__' # con all tenemos todos los campos #campos especificos podemos hacerlo con una lista = ['name', 'last_name',..]


#vamos a crearnos un serializador de prueba

class TestUserSerializer(serializers.Serializer): # ahora en lugar de un modelo, ponemos el ¡serilizador directamente

	name = serializers.CharField(max_length = 200) 
	email = serializers.EmailField()

	#validation custom, is_valid haria todo esto
	def validate_name(self, value): # EL VALOR QUE PONE ES EL DE VALIDATE_<FIELD_NAME> ESE ES VALOR QE ADOPTA VALE DENTRO DE LA FUNCION
		if 'developer' in value:			# por ejemoplo un caso de un usuario que no puede existir con ese nombre
			raise serializers.ValidationError('Error, no puede existir un usuario con ese nombre') # si devolvemos un error, no funcionara el validate
		
		print(self.context) # para acceder debo colocar si o si el self. no se pone context en los parametros junto a self y value
		#=>{'name': 'develop', 'email': 'develop@gmail.com'}
		return value
	
	#MiguelDN o mpsdiaz@gmail.com
	
	#validation custom
	def validate_email(self,value): 
		if value == '':
			raise serializers.ValidationError('Tiene que indicar un correo')
		
		if self.validate_name(self.context['name']) in value: # el name no es el que ha pasado la validacion anterior por lo que pillamos la funcion anterior y el dato que estaba validado para q sea el mismo, basicamente cosegios el valor q devuelve en return e la anterior funcion
			raise serializers.ValidationError('El mail no puede contener el nombre') #si el nombre esta en el correo dara error como el caso de mario, igual q abajo pero ahora sin usar el validate general
		return value

	def validate(self,data): # el conjunto de campos, toda la data
		# if data['name'] in data['email']:
		# 	raise serializers.ValidationError('El mail no puede contener el nombre') # mario no puede poner mario@gmail.com por ejemplo
		# print('validate general')
		return data

# si ponemos el "raise serializers.ValidationError('El mail no puede contener el nombre')" comparando los campos entre si, y accediendo entre ellos:
#{'email': [ErrorDetail(string='El mail no puede contener el nombre', code='invalid')]}

#si ponemos el "raise serializers.ValidationError('El mail no puede contener el nombre')" cunado lo colocamos al final en el conjunto de campos data
#{'non_field_errors': [ErrorDetail(string='El mail no puede contener el nombre', code='invalid')]}

#la diferencia es el non field error q solo sale si todos los demas campos estan bien y estamos con data, en otro caso se asociará con el campo correspondiente 'email' en este caso

# class User(AbstractBaseUser, PermissionsMixin):
# 	username = models.CharField(max_length=255, unique = True)
# 	email = models.EmailField('Correo Electrónico',max_length= 255, unique = True,) 
# 	name = models.CharField('Nombres', max_length = 255, blank = True, null = True)
# 	last_name = models.CharField('Apellidos', max_length= 255, blank=True, null = True)
# 	image =  models.ImageField('Imagen de perfil', upload_to= 'perfil/', max_length=255, null =True, blank = True)
# 	is_active = models.BooleanField(default = True)
# 	is_staff = models.BooleanField(default = False)
# 	historical = HistoricalRecords()
# 	objects = UserManager()
	