
from django.conf.urls import url, include
from editor import views
from rest_framework.urlpatterns import format_suffix_patterns

from rest_framework import routers
from rest_framework.authtoken.views import ObtainAuthToken

from editor.views import UserViewSet
from editor.views import CustomAuthToken

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'adminPatientJourney', views.AdminViewSet)

#user_detail = UserViewSet.as_view({'get': 'retrieve'})

urlpatterns = [
	#url(r'^mensajes/$', views.mensajesList.as_view()),
	#para los arquetipos
	url(r'^arquetipos/$', views.paraListaArquetipos),
	url(r'^arquetipos/(?P<question_id>[\w\-]+)/$', views.paraEditorArquetipos),
	#para el login
	url(r'^', include(router.urls)),
	#url(r'^auth/', ObtainAuthToken.as_view()),
	url(r'^auth/', CustomAuthToken.as_view()),

	url(r'^pacientes/(?P<rut_paciente>[\w\-]+)/$', views.pacienteEspecificoView),
	url(r'^pacientes/$', views.pacientesView),
	#trae pacientes atendidos por el user:
	url(r'^pacientes_atendidos/(?P<usuario>[\w\-]+)/$', views.pacientesAtendidosView),

	url(r'^languageConfiguration/$', views.languageConfigurationView)
	#url(r'^myUser/<int:pk>/', user_detail, name='user_detail')
	#para obtener usuario
	#url(r'^test/(?P<question_id>[\w\-]+)/$', views.obtenerUsuarioLogeado)

]
#probar para el editor, a lo mejor necesite la linea de abajo para cargar archivos xml 
#urlpatterns = format_suffix_patterns(urlpatterns)