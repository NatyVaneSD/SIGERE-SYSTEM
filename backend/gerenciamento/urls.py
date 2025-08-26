# gerenciamento/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UnidadeSolicitanteViewSet, SolicitanteViewSet, TipoExameViewSet, RequisicaoViewSet

router = DefaultRouter()
router.register('unidades', UnidadeSolicitanteViewSet)
router.register('solicitantes', SolicitanteViewSet)
router.register('tipos-exame', TipoExameViewSet)
router.register('requisicoes', RequisicaoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]