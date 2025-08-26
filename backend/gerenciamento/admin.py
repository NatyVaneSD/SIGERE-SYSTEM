from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import UnidadeSolicitante, Solicitante, TipoExame, Requisicao, Perito, Protocolo, Equipamento, TipoEquipamento, Armazenamento, Laudo, Auditoria

admin.site.register(UnidadeSolicitante)
admin.site.register(Solicitante)
admin.site.register(TipoExame)
admin.site.register(Requisicao)
admin.site.register(Perito)
admin.site.register(Protocolo)
admin.site.register(Equipamento)
admin.site.register(TipoEquipamento)
admin.site.register(Armazenamento)
admin.site.register(Laudo)
admin.site.register(Auditoria)