from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Consulta, Profissional
from .serializers import ConsultaSerializer, ProfissionalSerializer


class ProfissionalViewSet(viewsets.ModelViewSet):
    queryset = Profissional.objects.all()
    serializer_class = ProfissionalSerializer

    @action(detail=True, methods=["get"])
    def consultas(self, request, pk=None):
        profissional = self.get_object()
        consultas = profissional.consultas.all()
        serializer = ConsultaSerializer(consultas, many=True)

        return Response(serializer.data)


class ConsultaViewSet(viewsets.ModelViewSet):
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer