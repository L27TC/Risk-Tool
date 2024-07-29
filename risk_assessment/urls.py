from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('general_info/', views.general_info, name='general_info'),
    path('asset_assessments/', views.asset_assessments, name='asset_assessments'),
    path('threat_hazard_assessment/', views.threat_hazard_assessment, name='threat_hazard_assessment'),
    path('save_threat_hazard_assessment/', views.save_threat_hazard_assessment, name='save_threat_hazard_assessment'),
    path('controls_assessment/', views.controls_assessment, name='controls_assessment'),
    path('save_controls_assessment/', views.save_controls_assessment, name='save_controls_assessment'),
    path('save_changes/', views.save_changes, name='save_changes'),
    path('save_asset_criteria/', views.save_asset_criteria, name='save_asset_criteria'),
    path('save_intent/', views.save_intent, name='save_intent'),
    path('save_capability/', views.save_capability, name='save_capability'),
    path('save_tolerance/', views.save_tolerance, name='save_tolerance'),
    path('save_matrix/', views.save_matrix, name='save_matrix'),
    path('save_control_effectiveness/', views.save_control_effectiveness, name='save_control_effectiveness'),
    path('save_hazard_criteria/', views.save_hazard_criteria, name='save_hazard_criteria'),  # Add this line
    path('threat_tool/', views.threat_tool, name='threat_tool'),
    path('completed_assessment/', views.completed_assessment, name='completed_assessment'),
    path('download_pdf/', views.download_pdf, name='download_pdf'),
    path('download_word/', views.download_word, name='download_word'),
    path('404/', views.custom_404, name='custom_404'),
    path('500/', views.custom_500, name='custom_500'),
]
