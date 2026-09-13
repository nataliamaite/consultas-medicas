from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Consulta, Profissional


class ProfissionalAPITests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="teste",
            password="senha123"
        )

        self.client.force_authenticate(user=self.user)

        self.profissional = Profissional.objects.create(
            nome_social="Maria Silva",
            profissao="Médica",
            endereco="Rua Central, 100",
            contato="83999999999",
        )

    def test_criar_profissional(self):
        url = reverse("profissional-list")

        data = {
            "nome_social": "João Santos",
            "profissao": "Dentista",
            "endereco": "Rua das Flores, 200",
            "contato": "83988887777",
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["nome_social"], "João Santos")

    def test_listar_profissionais(self):
        url = reverse("profissional-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_buscar_profissional(self):
        url = reverse(
            "profissional-detail",
            args=[self.profissional.id]
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["nome_social"],
            "Maria Silva"
        )

    def test_atualizar_profissional(self):
        url = reverse(
            "profissional-detail",
            args=[self.profissional.id]
        )

        data = {
            "nome_social": "Maria Silva Santos",
            "profissao": "Cardiologista",
            "endereco": "Avenida Central, 500",
            "contato": "83977776666",
        }

        response = self.client.put(
            url,
            data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["nome_social"],
            "Maria Silva Santos"
        )

    def test_excluir_profissional(self):
        url = reverse(
            "profissional-detail",
            args=[self.profissional.id]
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            Profissional.objects.filter(
                id=self.profissional.id
            ).exists()
        )

    def test_profissional_com_dados_obrigatorios_ausentes(self):
        url = reverse("profissional-list")

        data = {
            "nome_social": "",
            "profissao": "",
        }

        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )


class ConsultaAPITests(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create_user(
            username="teste",
            password="senha123"
        )

        self.client.force_authenticate(user=self.user)

        self.profissional = Profissional.objects.create(
            nome_social="Maria Silva",
            profissao="Médica",
            endereco="Rua Central, 100",
            contato="83999999999",
        )

        self.profissional2 = Profissional.objects.create(
            nome_social="João Santos",
            profissao="Dentista",
            endereco="Rua das Flores, 200",
            contato="83988887777",
        )

        self.consulta = Consulta.objects.create(
            data="2026-09-15T14:00:00Z",
            profissional=self.profissional,
        )

    def test_criar_consulta(self):
        url = reverse("consulta-list")

        data = {
            "data": "2026-09-20T10:00:00Z",
            "profissional": self.profissional.id,
        }

        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            response.data["profissional"],
            self.profissional.id
        )

    def test_listar_consultas(self):
        url = reverse("consulta-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(len(response.data), 1)

    def test_buscar_consulta(self):
        url = reverse(
            "consulta-detail",
            args=[self.consulta.id]
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_atualizar_consulta(self):
        url = reverse(
            "consulta-detail",
            args=[self.consulta.id]
        )

        data = {
            "data": "2026-09-17T10:00:00Z",
            "profissional": self.profissional.id,
        }

        response = self.client.put(
            url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

    def test_excluir_consulta(self):
        url = reverse(
            "consulta-detail",
            args=[self.consulta.id]
        )

        response = self.client.delete(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertFalse(
            Consulta.objects.filter(
                id=self.consulta.id
            ).exists()
        )

    def test_buscar_consultas_por_profissional(self):
        Consulta.objects.create(
            data="2026-09-20T10:00:00Z",
            profissional=self.profissional,
        )

        Consulta.objects.create(
            data="2026-09-21T10:00:00Z",
            profissional=self.profissional2,
        )

        url = reverse(
            "profissional-consultas",
            args=[self.profissional.id]
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(len(response.data), 2)

        for consulta in response.data:
            self.assertEqual(
                consulta["profissional"],
                self.profissional.id
            )

    def test_consulta_com_profissional_inexistente(self):
        url = reverse("consulta-list")

        data = {
            "data": "2026-09-25T10:00:00Z",
            "profissional": 99999,
        }

        response = self.client.post(
            url,
            data,
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    def test_consulta_sem_dados_obrigatorios(self):
        url = reverse("consulta-list")

        response = self.client.post(
            url,
            {},
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )


class AuthenticationAPITests(APITestCase):

    def test_api_sem_autenticacao(self):
        url = reverse("profissional-list")

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED
        )