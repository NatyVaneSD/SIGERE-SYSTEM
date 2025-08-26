# gerenciamento/models.py

from django.db import models

# Listas de escolhas (choices) para os campos
# Definidas como tuplas, não dicionários, e fora das classes para melhor reuso
PERITO_CHOICES = [
    ("Marcelo", "Marcelo Maués"),
    ("Fernando", "Luiz Fernando"),
    ("Verônica", "Verônica"),
    ("Natanael", "Natanael"),
    ("Samira", "Samira Luz"),
]

TIPO_DOCUMENTO_CHOICES = [
    ("FLAG", "FLAG"),
    ("IPL", "IPL"),
    ("BOP", "BOP"),
    ("OF", "OF"),
    ("TCO", "TCO"),
    ("MEMO", "MEMO"),
]

STATUS_CHOICES = [
    ("ESPERA", "Em Espera"),
    ("PROCESSAMENTO", "Em Processamento"),
    ("ENTREGUE", "Entregue"),
    ("TRANSFERIDO", "Transferido"),
    ("DEVOLVIDO", "Devolvido"),
    ("CANCELADO", "Cancelado"),
]

PESO_CHOICES = [
    ("P1", "PESO 01"),
    ("P2", "PESO 02"),
    ("P3", "PESO 03"),
    ("P4", "PESO 04"),
]

EQUIPAMENTO_CHOICES = [
    ("SMARTPHONE", "SMARTPHONE"),
    ("NOTEBOOK", "NOTEBOOK"),
    ("PENDRIVE", "PENDRIVE"),
    ("HD", "HD"),
    ("SSD", "SSD"),
    ("CPU", "CPU"),
    ("CARTAO MICROSD", "CARTÃO MICROSD"),
    ("OUTROS", "Outros"),
]

DEPOSITO_CHOICES = [
    ("D1", "Deposito 01"),
    ("D2", "Deposito 02"),
    ("D3", "Deposito 03"),
]

# ----------------------------------------------------------------------------------------------------------------------

# Classes corrigidas (modelos)

class UnidadeSolicitante(models.Model):
    # O Django já cria o campo 'id' automaticamente
    nome_UnidadeSolicitante = models.CharField(max_length=255)

    def __str__(self):
        return self.nome_UnidadeSolicitante

class Solicitante(models.Model):
    nome_solicitante = models.CharField(max_length=255)
    # Adicionando a chave estrangeira para UnidadeSolicitante
    unidade_solicitante = models.ForeignKey(UnidadeSolicitante, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome_solicitante

class TipoExame(models.Model):
    nome_exame = models.CharField(max_length=225)
    
    def __str__(self):
        return self.nome_exame

class Perito(models.Model):
    # Criando um modelo de Perito para ter uma tabela própria
    nome = models.CharField(max_length=255)
    # Relação com a tabela de Laudo e Protocolo será feita usando ForeingKey
    
    def __str__(self):
        return self.nome
    
class Requisicao(models.Model):
    # O id é gerado automaticamente
    tipo_documento = models.CharField(max_length=4, choices=TIPO_DOCUMENTO_CHOICES)
    # numero_caso não precisa ser max_length=50, 9 é o suficiente
    numero_caso = models.CharField(max_length=9, unique=True)
    # Adicionando parênteses para os campos de data
    data_requisicao = models.DateField()
    data_recebimento = models.DateField()
    # TextField não precisa de max_length
    objetivo_pericia = models.TextField()
    status_requisicao = models.CharField(max_length=20, choices=STATUS_CHOICES)
    peso_requisicao = models.CharField(max_length=2, choices=PESO_CHOICES)
    # PAE não precisa ser unique, pois pode haver requisições sem PAE
    pae_requisicao = models.CharField(max_length=25, blank=True, null=True)

    # Adicionando as chaves estrangeiras para Solicitante e TipoExame
    solicitante = models.ForeignKey(Solicitante, on_delete=models.SET_NULL, null=True)
    tipo_exame = models.ForeignKey(TipoExame, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"Req. {self.numero_caso} - Status: {self.status_requisicao}"


class Protocolo(models.Model):
    numero_protocolo = models.CharField(max_length=50, unique=True)
    data_entrega_perito = models.DateField()  # Adicionando parênteses
    
    # Perito deve ser uma chave estrangeira, não um campo de texto com escolhas
    perito = models.ForeignKey(Perito, on_delete=models.SET_NULL, null=True)
    
    # Chave estrangeira para a Requisição
    requisicao = models.ForeignKey(Requisicao, on_delete=models.CASCADE)

    def __str__(self):
        return self.numero_protocolo


class Equipamento(models.Model):
    # Chave estrangeira para o Tipo_Equipamento
    tipo_equipamento = models.ForeignKey('TipoEquipamento', on_delete=models.CASCADE)
    # Chave estrangeira para o Armazenamento
    local_armazenamento = models.ForeignKey('Armazenamento', on_delete=models.SET_NULL, null=True)
    
    # Ligação N:M com Laudo e N:1 com Protocolo
    protocolo = models.ForeignKey(Protocolo, on_delete=models.CASCADE)

    def __str__(self):
        return f"Equipamento {self.pk}" # Retornando o PK para identificação única

class TipoEquipamento(models.Model):
    # A classe se chamava Tipo_Equipamento
    tipo = models.CharField(max_length=50, choices=EQUIPAMENTO_CHOICES)
    # other_type pode ser opcional
    outros_tipo = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
         # Retorna o valor do campo 'outros_tipo' se 'tipo' for "OUTROS", caso contrário, retorna o valor de 'tipo'
        return self.get_tipo_display() if self.tipo != "OUTROS" else self.outros_tipo


class Armazenamento(models.Model):
    deposito = models.CharField(max_length=50, choices=DEPOSITO_CHOICES)
    prateleira = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.deposito} - {self.prateleira}"

class Laudo(models.Model):
    numero_laudo = models.CharField(max_length=100, unique=True)
    data_entrega_expedicao = models.DateField()
    data_entrega_custodia = models.DateField()
    anexo_digital = models.BooleanField(default=True)
    
    # Laudo pode ter um ou mais peritos, então a melhor forma é usar ManyToManyField
    peritos = models.ManyToManyField(Perito)
    
    # Laudo se liga a um ou mais equipamentos
    equipamentos = models.ManyToManyField(Equipamento)
    
    # Laudo se liga a um protocolo
    protocolo = models.ForeignKey(Protocolo, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.numero_laudo

class Auditoria(models.Model):
    tabela_afetada = models.CharField(max_length=255)
    id_registro = models.IntegerField()
    acao = models.CharField(max_length=10) # insert, update, delete
    dados_antigos = models.JSONField(blank=True, null=True)
    data_hora = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Auditoria em {self.tabela_afetada} - Ação: {self.acao}"