from rest_framework.routers import DefaultRouter

from .views import ConsultaViewSet, ProfissionalViewSet

router = DefaultRouter()

router.register(r"profissionais", ProfissionalViewSet)
router.register(r"consultas", ConsultaViewSet)

urlpatterns = router.urls