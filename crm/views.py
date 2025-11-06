from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Sum
from .models import Company, Contact, Pipeline, Stage, Deal, Activity
from .serializers import (
    CompanySerializer, ContactSerializer, PipelineSerializer,
    StageSerializer, DealSerializer, ActivitySerializer
)

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    
    def get_queryset(self):
        queryset = Company.objects.all()
        # Фильтрация по назначенному пользователю
        assigned_to = self.request.query_params.get('assigned_to')
        if assigned_to:
            queryset = queryset.filter(assigned_to_id=assigned_to)
        return queryset

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    
    def get_queryset(self):
        queryset = Contact.objects.all()
        company_id = self.request.query_params.get('company_id')
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        return queryset

class PipelineViewSet(viewsets.ModelViewSet):
    queryset = Pipeline.objects.filter(is_active=True)
    serializer_class = PipelineSerializer

class StageViewSet(viewsets.ModelViewSet):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer

class DealViewSet(viewsets.ModelViewSet):
    queryset = Deal.objects.all()
    serializer_class = DealSerializer
    
    def get_queryset(self):
        queryset = Deal.objects.all()
        stage_id = self.request.query_params.get('stage_id')
        assigned_to = self.request.query_params.get('assigned_to')
        
        if stage_id:
            queryset = queryset.filter(stage_id=stage_id)
        if assigned_to:
            queryset = queryset.filter(assigned_to_id=assigned_to)
            
        return queryset
    
    @action(detail=True, methods=['post'])
    def change_stage(self, request, pk=None):
        deal = self.get_object()
        new_stage_id = request.data.get('stage_id')
        
        try:
            new_stage = Stage.objects.get(id=new_stage_id)
            deal.stage = new_stage
            deal.save()
            return Response({'status': 'stage changed'})
        except Stage.DoesNotExist:
            return Response({'error': 'Stage not found'}, status=status.HTTP_400_BAD_REQUEST)

class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    
    def get_queryset(self):
        queryset = Activity.objects.all()
        company_id = self.request.query_params.get('company_id')
        deal_id = self.request.query_params.get('deal_id')
        completed = self.request.query_params.get('completed')
        
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        if deal_id:
            queryset = queryset.filter(deal_id=deal_id)
        if completed is not None:
            queryset = queryset.filter(completed=completed.lower() == 'true')
            
        return queryset
    
    @action(detail=True, methods=['post'])
    def mark_completed(self, request, pk=None):
        activity = self.get_object()
        activity.completed = True
        activity.save()
        return Response({'status': 'activity completed'})

class DashboardViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def stats(self, request):
        total_companies = Company.objects.count()
        total_deals = Deal.objects.count()
        total_activities = Activity.objects.count()
        
        # Статистика по воронке
        pipeline_stats = Stage.objects.annotate(
            deal_count=Count('deal')
        ).values('name', 'deal_count')
        
        # Активные задачи
        pending_activities = Activity.objects.filter(completed=False).count()
        
        return Response({
            'total_companies': total_companies,
            'total_deals': total_deals,
            'total_activities': total_activities,
            'pending_activities': pending_activities,
            'pipeline_stats': list(pipeline_stats),
        })
