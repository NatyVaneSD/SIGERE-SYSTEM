from django.db import models
from django.contrib.auth.models import User

# Listas de escolhas para os campos
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
    ("CARTAO_MICROSD", "CARTÃO MICROSD"),
    ("OUTROS", "Outros"),
]

DEPOSITO_CHOICES = [
    ("D1", "Deposito 01"),
    ("D2", "Deposito 02"),
    ("D3", "Deposito 03"),
]

class UnidadeSolicitante(models.Model):
    nome_UnidadeSolicitante = models.CharField(max_length=255, verbose_name="Nome da Unidade Solicitante")
    
    class Meta:
        verbose_name = "Unidade Solicitante"
        verbose_name_plural = "Unidades Solicitantes"
        ordering = ['nome_UnidadeSolicitante']

    def __str__(self):
        return self.nome_UnidadeSolicitante

class Solicitante(models.Model):
    nome_solicitante = models.CharField(max_length=255, verbose_name="Nome do Solicitante")
    unidade_solicitante = models.ForeignKey(UnidadeSolicitante, on_delete=models.CASCADE, verbose_name="Unidade Solicitante")
    
    class Meta:
        verbose_name = "Solicitante"
        verbose_name_plural = "Solicitantes"
        ordering = ['nome_solicitante']

    def __str__(self):
        return f"{self.nome_solicitante} - {self.unidade_solicitante}"

class TipoExame(models.Model):
    nome_exame = models.CharField(max_length=225, verbose_name="Tipo de Exame", unique=True)
    
    class Meta:
        verbose_name = "Tipo de Exame"
        verbose_name_plural = "Tipos de Exame"
        ordering = ['nome_exame']
    
    def __str__(self):
        return self.nome_exame

class Perito(models.Model):
    nome = models.CharField(max_length=255, verbose_name="Nome do Perito", unique=True)
    
    class Meta:
        verbose_name = "Perito"
        verbose_name_plural = "Peritos"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome

class Requisicao(models.Model):
    tipo_documento = models.CharField(max_length=4, choices=TIPO_DOCUMENTO_CHOICES, verbose_name="Tipo de Documento")
    numero_caso = models.CharField(max_length=9, unique=True, verbose_name="Número do Caso")
    data_requisicao = models.DateField(verbose_name="Data da Requisição")
    data_recebimento = models.DateField(verbose_name="Data de Recebimento")
    objetivo_pericia = models.TextField(verbose_name="Objetivo da Perícia")
    status_requisicao = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Status da Requisição")
    peso_requisicao = models.CharField(max_length=2, choices=PESO_CHOICES, verbose_name="Peso da Requisição")
    pae_requisicao = models.CharField(max_length=25, blank=True, null=True, verbose_name="PAE da Requisição")
    solicitante = models.ForeignKey(Solicitante, on_delete=models.SET_NULL, null=True, verbose_name="Solicitante")
    tipo_exame = models.ForeignKey(TipoExame, on_delete=models.SET_NULL, null=True, verbose_name="Tipo de Exame")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    data_atualizacao = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")
    
    class Meta:
        verbose_name = "Requisição"
        verbose_name_plural = "Requisições"
        ordering = ['-data_criacao']
        indexes = [
            models.Index(fields=['numero_caso']),
            models.Index(fields=['status_requisicao']),
            models.Index(fields=['data_recebimento']),
        ]

    def __str__(self):
        return f"REQ-{self.numero_caso} - {self.get_status_requisicao_display()}"

class Protocolo(models.Model):
    numero_protocolo = models.CharField(max_length=50, unique=True, verbose_name="Número do Protocolo")
    data_entrega_perito = models.DateField(verbose_name="Data de Entrega ao Perito")
    perito = models.ForeignKey(Perito, on_delete=models.SET_NULL, null=True, verbose_name="Perito")
    requisicao = models.ForeignKey(Requisicao, on_delete=models.CASCADE, verbose_name="Requisição")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    
    class Meta:
        verbose_name = "Protocolo"
        verbose_name_plural = "Protocolos"
        ordering = ['-data_criacao']
        indexes = [
            models.Index(fields=['numero_protocolo']),
        ]

    def __str__(self):
        return self.numero_protocolo

class TipoEquipamento(models.Model):
    tipo = models.CharField(max_length=50, choices=EQUIPAMENTO_CHOICES, verbose_name="Tipo de Equipamento")
    outros_tipo = models.CharField(max_length=50, blank=True, null=True, verbose_name="Outro Tipo (se necessário)")
    
    class Meta:
        verbose_name = "Tipo de Equipamento"
        verbose_name_plural = "Tipos de Equipamento"
        ordering = ['tipo']

    def __str__(self):
        if self.tipo == "OUTROS" and self.outros_tipo:
            return self.outros_tipo
        return self.get_tipo_display()

class Armazenamento(models.Model):
    deposito = models.CharField(max_length=50, choices=DEPOSITO_CHOICES, verbose_name="Depósito")
    prateleira = models.CharField(max_length=50, verbose_name="Prateleira")
    
    class Meta:
        verbose_name = "Armazenamento"
        verbose_name_plural = "Armazenamentos"
        unique_together = ['deposito', 'prateleira']
        ordering = ['deposito', 'prateleira']

    def __str__(self):
        return f"{self.get_deposito_display()} - Prateleira {self.prateleira}"

class Equipamento(models.Model):
    tipo_equipamento = models.ForeignKey(TipoEquipamento, on_delete=models.CASCADE, verbose_name="Tipo de Equipamento")
    quant_equipamente = models.PositiveSmallIntegerField(verbose_name="Quantidade de Equipamentos")
    local_armazenamento = models.ForeignKey(Armazenamento, on_delete=models.SET_NULL, null=True, verbose_name="Local de Armazenamento")
    protocolo = models.ForeignKey(Protocolo, on_delete=models.CASCADE, verbose_name="Protocolo")
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name="Data de Cadastro")
    
    class Meta:
        verbose_name = "Equipamento"
        verbose_name_plural = "Equipamentos"
        ordering = ['-data_cadastro']

    def __str__(self):
        return f"{self.tipo_equipamento} - Protocolo: {self.protocolo.numero_protocolo}"

class Laudo(models.Model):
    numero_laudo = models.CharField(max_length=100, unique=True, verbose_name="Número do Laudo")
    data_entrega_expedicao = models.DateField(verbose_name="Data de Entrega na Expedição")
    data_entrega_custodia = models.DateField(verbose_name="Data de Entrega na Custódia")
    anexo_digital = models.BooleanField(default=True, verbose_name="Anexo Digital")
    peritos = models.ManyToManyField(Perito, verbose_name="Peritos")
    equipamentos = models.ManyToManyField(Equipamento, verbose_name="Equipamentos")
    protocolo = models.ForeignKey(Protocolo, on_delete=models.SET_NULL, null=True, verbose_name="Protocolo")
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    
    class Meta:
        verbose_name = "Laudo"
        verbose_name_plural = "Laudos"
        ordering = ['-data_criacao']
        indexes = [
            models.Index(fields=['numero_laudo']),
        ]

    def __str__(self):
        return self.numero_laudo

class Auditoria(models.Model):
    ACAO_CHOICES = [
        ('INSERT', 'Inserção'),
        ('UPDATE', 'Atualização'),
        ('DELETE', 'Exclusão'),
    ]
    
    tabela_afetada = models.CharField(max_length=255, verbose_name="Tabela Afetada")
    id_registro = models.IntegerField(verbose_name="ID do Registro")
    acao = models.CharField(max_length=10, choices=ACAO_CHOICES, verbose_name="Ação")
    dados_antigos = models.JSONField(blank=True, null=True, verbose_name="Dados Antigos")
    data_hora = models.DateTimeField(auto_now_add=True, verbose_name="Data e Hora")
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Usuário")
    
    class Meta:
        verbose_name = "Auditoria"
        verbose_name_plural = "Auditorias"
        ordering = ['-data_hora']
        indexes = [
            models.Index(fields=['tabela_afetada', 'id_registro']),
            models.Index(fields=['data_hora']),
        ]

    def __str__(self):
        return f"Auditoria - {self.tabela_afetada} - {self.acao} - {self.data_hora}"