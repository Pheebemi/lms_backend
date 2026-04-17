from django.urls import path
from .views import (
    CourseCatalogListView,
    StudentRecordListCreateView,
    StudentRecordDetailView,
    StudentRecordApproveView,
    ManagementStatsView,
)

urlpatterns = [
    path('courses/', CourseCatalogListView.as_view(), name='course-catalog-list'),
    path('records/', StudentRecordListCreateView.as_view(), name='student-record-list-create'),
    path('records/<uuid:pk>/', StudentRecordDetailView.as_view(), name='student-record-detail'),
    path('records/<uuid:pk>/status/', StudentRecordApproveView.as_view(), name='student-record-status'),
    path('stats/', ManagementStatsView.as_view(), name='management-stats'),
]
