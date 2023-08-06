from netbox.api.routers import NetBoxRouter
from . import views

app_name = 'netbox_manage_project'

router = NetBoxRouter()
router.register('project', views.ProjectViewSet)
router.register('quotatemplate', views.QuotaTemplateViewSet)

urlpatterns = router.urls