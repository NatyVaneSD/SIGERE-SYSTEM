# gerenciamento/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UnidadeSolicitanteViewSet, SolicitanteViewSet, TipoExameViewSet, RequisicaoViewSet,
    PeritoViewSet, ProtocoloViewSet, EquipamentoViewSet, TipoEquipamentoViewSet,
    ArmazenamentoViewSet, LaudoViewSet, AuditoriaViewSet
)
router = DefaultRouter()
router.register('unidades', UnidadeSolicitanteViewSet)
router.register('solicitantes', SolicitanteViewSet)
router.register('tipos-exame', TipoExameViewSet)
router.register('requisicoes', RequisicaoViewSet)
router.register('peritos', PeritoViewSet)
router.register('protocolos', ProtocoloViewSet)
router.register('equipamentos', EquipamentoViewSet)
router.register('tipos-equipamento', TipoEquipamentoViewSet)
router.register('armazenamento', ArmazenamentoViewSet)
router.register('laudos', LaudoViewSet)
router.register('auditoria', AuditoriaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]