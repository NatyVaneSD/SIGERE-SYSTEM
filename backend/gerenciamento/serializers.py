# gerenciamento/serializers.py

from rest_framework import serializers
from .models import UnidadeSolicitante, Solicitante, TipoExame, Requisicao, Perito, Protocolo, Equipamento, TipoEquipamento, Armazenamento, Laudo, Auditoria

class UnidadeSolicitanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadeSolicitante
        fields = '__all__' # Inclui todos os campos do modelo

class SolicitanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitante
        fields = '__all__'

class TipoExameSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoExame
        fields = '__all__'

class RequisicaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requisicao
        fields = '__all__'
        

class PeritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perito
        fields = '__all__'

class ProtocoloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Protocolo
        fields = '__all__'
        depth = 1  # Inclui os dados do Perito e da Requisição

class TipoEquipamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEquipamento
        fields = '__all__'

class ArmazenamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Armazenamento
        fields = '__all__'

class EquipamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipamento
        fields = '__all__'
        depth = 1 # Inclui os dados do TipoEquipamento, Armazenamento e Protocolo

class LaudoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laudo
        fields = '__all__'
        depth = 1 # Inclui os dados dos Peritos, Equipamentos e Protocolo

class AuditoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditoria
        fields = '__all__'