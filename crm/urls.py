from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'companies', views.CompanyViewSet)
router.register(r'contacts', views.ContactViewSet)
router.register(r'pipelines', views.PipelineViewSet)
router.register(r'stages', views.StageViewSet)
router.register(r'deals', views.DealViewSet)
router.register(r'activities', views.ActivityViewSet)
router.register(r'dashboard', views.DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
]
