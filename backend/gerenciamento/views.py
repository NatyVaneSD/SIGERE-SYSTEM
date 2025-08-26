from django.shortcuts import render
# gerenciamento/views.py

from rest_framework import viewsets
from .serializers import UnidadeSolicitanteSerializer, SolicitanteSerializer, TipoExameSerializer, RequisicaoSerializer
from .models import UnidadeSolicitante, Solicitante, TipoExame, Requisicao

class UnidadeSolicitanteViewSet(viewsets.ModelViewSet):
    queryset = UnidadeSolicitante.objects.all()
    serializer_class = UnidadeSolicitanteSerializer

class SolicitanteViewSet(viewsets.ModelViewSet):
    queryset = Solicitante.objects.all()
    serializer_class = SolicitanteSerializer

class TipoExameViewSet(viewsets.ModelViewSet):
    queryset = TipoExame.objects.all()
    serializer_class = TipoExameSerializer

class RequisicaoViewSet(viewsets.ModelViewSet):
    queryset = Requisicao.objects.all()
    serializer_class = RequisicaoSerializer