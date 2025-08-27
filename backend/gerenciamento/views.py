# gerenciamento/views.py

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Q # Para buscas mais flexíveis
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
        Recebe uma query e retorna uma lista de nomes correspondentes.
        """
        query = request.query_params.get('q', '')
        if not query:
            return Response([])

        # Filtra solicitantes cujo nome contenha a query (case-insensitive)
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

        # Filtra tipos de exame cuja descricao contenha a query (case-insensitive)
        tipos_exame = TipoExame.objects.filter(
            Q(nome_exame__icontains=query)
        ).values_list('nome_exame', flat=True).distinct()

        return Response(list(tipos_exame))

# -----------------------------------------------------------------------------
# RequisicaoViewSet (com lógica de normalização)
# -----------------------------------------------------------------------------

class RequisicaoViewSet(viewsets.ModelViewSet):
    queryset = Requisicao.objects.all()
    serializer_class = RequisicaoSerializer

    def create(self, request, *args, **kwargs):
        """
        Sobrescreve o método CREATE para normalizar os dados antes de salvar.
        """
        # Extrai os nomes de solicitante e tipo de exame do corpo da requisição
        data = request.data
        solicitante_nome = data.get('solicitante', '')
        tipo_exame_nome = data.get('tipo_exame', '')
        
        if not solicitante_nome or not tipo_exame_nome:
            return Response(
                {"error": "Os campos 'solicitante' e 'tipo_exame' são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 1. Normalização do Solicitante
        # Usa get_or_create para buscar o solicitante ou criá-lo se não existir.
        solicitante, created_sol = Solicitante.objects.get_or_create(
            nome_solicitante=solicitante_nome
        )
        if created_sol:
            print(f"Novo solicitante criado: {solicitante_nome}")

        # 2. Normalização do Tipo de Exame
        # Usa get_or_create para buscar o tipo de exame ou criá-lo se não existir.
        tipo_exame, created_te = TipoExame.objects.get_or_create(
            nome_exame=tipo_exame_nome
        )
        if created_te:
            print(f"Novo tipo de exame criado: {tipo_exame_nome}")
            
        # 3. Atualiza os dados da requisição com os IDs normalizados
        data['solicitante'] = solicitante.pk
        data['tipo_exame'] = tipo_exame.pk

        # O serializador agora receberá os IDs e validará normalmente
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# -----------------------------------------------------------------------------
# Outros ViewSets (mantidos como estão)
# -----------------------------------------------------------------------------

class UnidadeSolicitanteViewSet(viewsets.ModelViewSet):
    queryset = UnidadeSolicitante.objects.all()
    serializer_class = UnidadeSolicitanteSerializer

# ... inclua os outros ViewSets aqui
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
