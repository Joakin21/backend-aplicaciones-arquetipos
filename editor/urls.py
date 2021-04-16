
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

urlpatterns = [

	url(r'^arquetipos/$', views.paraListaArquetipos),
	url(r'^arquetipos/(?P<question_id>[\w\-]+)/$', views.paraEditorArquetipos),
	url(r'^', include(router.urls)),
	url(r'^auth/', CustomAuthToken.as_view()),
	url(r'^pacientes/(?P<rut_paciente>[\w\-]+)/$', views.pacienteEspecificoView),
	url(r'^setEsAtendidoAhora/(?P<rut_paciente>[\w\-]+)/$', views.setEsAtendidoAhoraView),
	url(r'^pacientes/$', views.pacientesView),
	url(r'^getSkipPatients/$', views.getSkipPatientsView),
	url(r'^pacientes_atendidos/(?P<usuario>[\w\-]+)/$', views.pacientesAtendidosView),

	url(r'^setPatientStatus/$', views.setPatientStatusView),
	
	url(r'^amountDocuments/$', views.getAmountDocuments),
	url(r'^languageConfiguration/$', views.languageConfigurationView),
	url(r'^arquetipos_usuario/(?P<pk>[\w\-]+)/$', views.arquetiposParaUsuarioView),

]
