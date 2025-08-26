# gerenciamento/serializers.py

from rest_framework import serializers
from .models import UnidadeSolicitante, Solicitante, TipoExame, Requisicao

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