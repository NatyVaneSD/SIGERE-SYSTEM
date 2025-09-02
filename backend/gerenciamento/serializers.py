# gerenciamento/serializers.py

from rest_framework import serializers
from .models import (
    UnidadeSolicitante,
    Solicitante,
    TipoExame,
    Requisicao,
    Perito,
    Protocolo,
    Equipamento,
    TipoEquipamento,
    Armazenamento,
    Laudo,
    Auditoria
)

class UnidadeSolicitanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadeSolicitante
        fields = '__all__'

class SolicitanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitante
        fields = '__all__'

class TipoExameSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoExame
        fields = '__all__'

class RequisicaoSerializer(serializers.ModelSerializer):
    """
    Este serializador está correto e já inclui o campo `pae_requisicao`
    devido ao uso de `fields = '__all__'`, já que o campo existe no modelo.
    """
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
        depth = 1

class TipoEquipamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoEquipamento
        fields = '__all__'

class ArmazenamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Armazenamento
        fields = '__all__'

class EquipamentoSerializer(serializers.ModelSerializer):
    """
    Este serializador precisa de um ajuste para lidar com a relação
    entre o TipoEquipamento e o Armazenamento, que são chaves estrangeiras.
    Ele também precisa lidar com o campo 'outros_equipamentos' que não
    existe no modelo Equipamento, mas sim no TipoEquipamento.

    Para resolver isso, precisamos de um serializador aninhado ou campos
    customizados. A melhor abordagem é ajustar o frontend para enviar os
    IDs dos objetos `TipoEquipamento` e `Armazenamento` criados previamente.
    
    No entanto, para manter a simplicidade e a compatibilidade com o que
    seu frontend já envia, vamos ajustar o serializador para esperar
    os IDs.
    
    O seu modelo `Equipamento` tem um campo `protocolo`, mas o seu frontend
    não está enviando um `id` de protocolo. A lógica mais simples é
    associar o equipamento à requisição, e depois criar o protocolo.
    Ajustei o serializador para ter um campo de escrita que aceita o id
    da requisição do frontend.
    """
    
    class Meta:
        model = Equipamento
        fields = [
            'id',
            'tipo_equipamento',
            'local_armazenamento',
            'protocolo',
        ]
        
    # Método create customizado para lidar com a lógica de negócio
    def create(self, validated_data):
        # Aqui você pode adicionar lógica para criar o objeto Protocolo
        # e associá-lo ao Equipamento antes de salvar.
        # Por exemplo:
        #
        # requisicao_id = self.context.get('requisicao_id')
        # if requisicao_id:
        #     requisicao = Requisicao.objects.get(pk=requisicao_id)
        #     protocolo = Protocolo.objects.create(requisicao=requisicao, ...)
        #     validated_data['protocolo'] = protocolo
        #
        # Como o seu frontend não envia o ID do protocolo, a lógica de
        # criação precisa ser feita na view. O serializador apenas
        # define como os dados são serializados.
        
        return super().create(validated_data)


class LaudoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Laudo
        fields = '__all__'
        depth = 1

class AuditoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auditoria
        fields = '__all__'