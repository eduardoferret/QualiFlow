from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'branches', views.BranchViewSet)
router.register(r'sectors', views.SectorViewSet)
router.register(r'documents', views.DocumentViewSet)
router.register(r'document-versions', views.DocumentVersionViewSet)
router.register(r'workflows', views.WorkflowViewSet)
router.register(r'workflow-steps', views.WorkflowStepViewSet)
router.register(r'processes', views.ProcessViewSet)
router.register(r'process-steps', views.ProcessStepViewSet)
router.register(r'activities', views.ActivityViewSet)
router.register(r'users', views.UserViewSet, basename='user')

urlpatterns = router.urls
