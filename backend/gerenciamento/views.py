from django.shortcuts import render
# gerenciamento/views.py

from rest_framework import viewsets
from .serializers import ( UnidadeSolicitanteSerializer, SolicitanteSerializer, TipoExameSerializer, RequisicaoSerializer, PeritoSerializer, ProtocoloSerializer, EquipamentoSerializer, TipoEquipamentoSerializer, ArmazenamentoSerializer, LaudoSerializer, AuditoriaSerializer
)
from .models import (
    UnidadeSolicitante, Solicitante, TipoExame, Requisicao,
    Perito, Protocolo, Equipamento, TipoEquipamento,
    Armazenamento, Laudo, Auditoria
)
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
    
class PeritoViewSet(viewsets.ModelViewSet):
    queryset = Perito.objects.all()
    serializer_class = PeritoSerializer

class ProtocoloViewSet(viewsets.ModelViewSet):
    queryset = Protocolo.objects.all()
    serializer_class = ProtocoloSerializer

class EquipamentoViewSet(viewsets.ModelViewSet):
    queryset = Equipamento.objects.all()
    serializer_class = EquipamentoSerializer

class TipoEquipamentoViewSet(viewsets.ModelViewSet):
    queryset = TipoEquipamento.objects.all()
    serializer_class = TipoEquipamentoSerializer

class ArmazenamentoViewSet(viewsets.ModelViewSet):
    queryset = Armazenamento.objects.all()
    serializer_class = ArmazenamentoSerializer

class LaudoViewSet(viewsets.ModelViewSet):
    queryset = Laudo.objects.all()
    serializer_class = LaudoSerializer

class AuditoriaViewSet(viewsets.ModelViewSet):
    queryset = Auditoria.objects.all()
    serializer_class = AuditoriaSerializer