from django.test import TestCase, Client
from django.urls import reverse
from .models import ProfesionalSalud

# Create your tests here.
class TestViews(TestCase):

    def test_prject_list_GET(self):
        client = Client()
        
        response = client.get(reverse('list'))

        self.assertEquals(response.status_code, 200)
