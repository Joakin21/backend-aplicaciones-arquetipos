
from django.conf.urls import url, include
from editor import views
from rest_framework.urlpatterns import format_suffix_patterns

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
	#url(r'^mensajes/$', views.mensajesList.as_view()),
	#para los arquetipos
	url(r'^arquetipos/$', views.paraListaArquetipos),
	url(r'^arquetipos/(?P<question_id>[\w\-]+)/$', views.paraEditorArquetipos),
	#para el login
	url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]
#probar para el editor, a lo mejor necesite la linea de abajo para cargar archivos xml 
#urlpatterns = format_suffix_patterns(urlpatterns)