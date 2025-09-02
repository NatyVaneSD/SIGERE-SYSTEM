# gerenciamento/views.py

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q
from django.utils import timezone
from .serializers import (
    UnidadeSolicitanteSerializer, SolicitanteSerializer, TipoExameSerializer, RequisicaoSerializer,
    PeritoSerializer, ProtocoloSerializer, EquipamentoSerializer, TipoEquipamentoSerializer,
    ArmazenamentoSerializer, LaudoSerializer, AuditoriaSerializer
)
from .models import (
    UnidadeSolicitante, Solicitante, TipoExame, Requisicao,
    Perito, Protocolo, Equipamento, TipoEquipamento,
    Armazenamento, Laudo, Auditoria
)

# -----------------------------------------------------------------------------
# Endpoints de Autocomplete
# -----------------------------------------------------------------------------

class SolicitanteViewSet(viewsets.ModelViewSet):
    queryset = Solicitante.objects.all()
    serializer_class = SolicitanteSerializer

    @action(detail=False, methods=['get'])
    def autocomplete(self, request):
        """
        Endpoint para preenchimento automático de solicitantes.
        """
        query = request.query_params.get('q', '')
        if not query:
            return Response([])

        solicitantes = Solicitante.objects.filter(
            Q(nome_solicitante__icontains=query)
        ).values_list('nome_solicitante', flat=True).distinct()

        return Response(list(solicitantes))

class TipoExameViewSet(viewsets.ModelViewSet):
    queryset = TipoExame.objects.all()
    serializer_class = TipoExameSerializer

    @action(detail=False, methods=['get'])
    def autocomplete(self, request):
        """
        Endpoint para preenchimento automático de tipos de exame.
        """
        query = request.query_params.get('q', '')
        if not query:
            return Response([])

        tipos_exame = TipoExame.objects.filter(
            Q(nome_exame__icontains=query)
        ).values_list('nome_exame', flat=True).distinct()

        return Response(list(tipos_exame))

# -----------------------------------------------------------------------------
# RequisicaoViewSet
# -----------------------------------------------------------------------------

class RequisicaoViewSet(viewsets.ModelViewSet):
    queryset = Requisicao.objects.all()
    serializer_class = RequisicaoSerializer

    def create(self, request, *args, **kwargs):
        """
        Sobrescreve o método CREATE para normalizar os dados antes de salvar.
        """
        data = request.data
        solicitante_nome = data.get('solicitante', '')
        tipo_exame_nome = data.get('tipo_exame', '')
        
        if not solicitante_nome or not tipo_exame_nome:
            return Response(
                {"error": "Os campos 'solicitante' e 'tipo_exame' são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        solicitante, _ = Solicitante.objects.get_or_create(nome_solicitante=solicitante_nome)
        tipo_exame, _ = TipoExame.objects.get_or_create(nome_exame=tipo_exame_nome)
            
        data['solicitante'] = solicitante.pk
        data['tipo_exame'] = tipo_exame.pk

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

# -----------------------------------------------------------------------------
# Outros ViewSets
# -----------------------------------------------------------------------------

class UnidadeSolicitanteViewSet(viewsets.ModelViewSet):
    queryset = UnidadeSolicitante.objects.all()
    serializer_class = UnidadeSolicitanteSerializer

class PeritoViewSet(viewsets.ModelViewSet):
    queryset = Perito.objects.all()
    serializer_class = PeritoSerializer

class ProtocoloViewSet(viewsets.ModelViewSet):
    queryset = Protocolo.objects.all()
    serializer_class = ProtocoloSerializer

class EquipamentoViewSet(viewsets.ModelViewSet):
    queryset = Equipamento.objects.all()
    serializer_class = EquipamentoSerializer

    def create(self, request, *args, **kwargs):
        """
        Sobrescreve o método CREATE para criar um Equipamento
        e associá-lo ao Protocolo fornecido pelo usuário.
        """
        data = request.data
        numero_protocolo = data.get('numero_protocolo', '')
        tipo_equipamento_data = data.get('tipo_equipamento')
        local_armazenamento_data = data.get('local_armazenamento')
        requisicao_id = data.get('requisicao') # O frontend deve enviar o ID da requisição

        if not numero_protocolo:
            return Response(
                {"error": "O campo 'numero_protocolo' é obrigatório para criar um equipamento."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Busca ou cria a instância de Protocolo
            protocolo, _ = Protocolo.objects.get_or_create(
                numero_protocolo=numero_protocolo,
                defaults={'requisicao_id': requisicao_id, 'data_entrega_perito': timezone.now().date()}
            )
            
            # Busca as instâncias de TipoEquipamento e Armazenamento
            tipo_equipamento = TipoEquipamento.objects.get(pk=tipo_equipamento_data)
            local_armazenamento = Armazenamento.objects.get(pk=local_armazenamento_data)
            
        except (TipoEquipamento.DoesNotExist, Armazenamento.DoesNotExist, Protocolo.DoesNotExist):
            return Response(
                {"error": "Tipo de equipamento, local de armazenamento ou protocolo não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Cria a instância do equipamento associando aos objetos
        equipamento = Equipamento.objects.create(
            tipo_equipamento=tipo_equipamento,
            local_armazenamento=local_armazenamento,
            protocolo=protocolo
        )

        serializer = self.get_serializer(equipamento)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
