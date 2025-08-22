from django.db import models

perito_opicoes = {
    "Marcelo": "Marcelo Maués",
    "Fernando":"Luiz Fernando",
    "Verônica": "Verônica",
    "Natanael": "Natanael",
    "Samira": "Samira Luz",
    }

class Requisicao(models.Model):
    id = primary_Key=True
    tipo_documento_opicoes = {
        "FLAG": "FLAG",
        "IPL": "IPL",
        "BOP": "BOP",
        "OF": "OF",
        "TCO": "TCO",
        "MEMO": "MEMO",        
    }
    tipo_documeto = models.CharField(
        max_length=4,
        choices = tipo_documento_opicoes,
    )
    numero_caso = models.CharField(max_length=50, unique= True)
    data_requisicao = models.DateField
    data_recebimento = models.DateField
    objetivo_pericia =models.TextField(max_length=225)
    
    status_documento_opicoes = {
        "ESPERA": "Em Espera",
        "PROCESSAMENTO": "Em Processamento",
        "ENTREGUE": "Entregue",
        "TRANSFERIDO": "Transferido",
        "DEVOLVIDO": "Devolvido",
        "CANCELADO": "Cancelado",    
    }
    status_requisicao = models.CharField(choices=status_documento_opicoes)
    
    peso_documento_opicoes = {
        "P1": "PESO 01",
        "P2": "PESO 02",
        "P3": "PESO 03",
        "P4": "PESO 04", 
    }
    peso_requisicao = models.CharField(choices=peso_documento_opicoes)
    pae_requisicao = models.CharField(max_length=25, unique=True)
    
    
class Solicitante(models.Model):
    nome_solicitante = models.CharField(max_length=255)
    
    def __str__(self):
        return self.nome_Solicitante


class UnidadeSolicitante(models.Model):
    nome_UnidadeSolicitante = models.CharField(max_length=255)

    def __str__(self):
        return self.nome_UnidadeSolicitante
    
class TipoExame(models.Models):
    nome_exame =models.CharField(max_length=225)
    
    def __str__(self):
        return self.nome_exame
    
class Protocolo (models.Models):
    numero_protocolo = models.CharField(max_length=50, unique=True)
    data_entrega_perito = models.DateField
    perito= models.CharField(choices=perito_opicoes)

    def __str__(self):
        return self.numero_protocolo, self.perito, self.data_entrega_perito
    
class Equipamento(models.Models):
    quantidade_equipamento = models.IntegerField(max_length=50)
    
    def __str__(self):
        return self.quantidade_equipamento

class Tipo_Equipamento(models.Models):
    tipo_opicoes = {
    "SMARTPHONE": "SMARTPHONE",
    "NOTEBOOK": "NOTEBOOK",
    "PENDRIVE": "PENDRIVE",
    "HD": "HD",
    "SSD": "SSD",
    "CPU": "CPU",
    "CARTÃO MICROSD": "CARTÃO MICROSD",
    }
    tipo= models.CharField(choices=tipo_opicoes)
    outros_tipo = models.CharField(max_length=50)
    
    def __str__(self):
        return self.tipo, self.outros_tipo
    
class Armazenamento(models.Models):
    deposito_opicoes = {
    "Deposito 01": "D1",
    "Deposito 02": "D2",
    "Deposito 03": "D3",
    }
    deposito= models.CharField(choices=deposito_opicoes)
    prateleira = models.CharField(max_length=50)
    def __str__(self):
        return self.deposito, self.prateleira

class Laudo(models.Models):
    numero_laudo = models.CharField(max_length=100)    
    data_entrega_expedicao= models.DateField()
    data_entrega_custodia= models.DateField()
    anexo_digital = models.BooleanField(default=True)
    perito1 = models.CharField(choices=perito_opicoes)
    perito2 =models.BooleanField(default=False)
    def __str__(self):
        return self.numero_laudo, self.data_entrega_expedicao, self.data_entrega_custodia, self.anexo_digital, self.anexo_digital, self.perito1, self.perito2
    

class Auditoria(models.Models):
    dados_antigos = models.JSONField
    
    
    

    


    
    