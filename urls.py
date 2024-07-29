from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('risk-assessment/', include('risk_assessment.urls')),
    path('accounts/', include('users.urls')),  # Include the users app URLs
    path('', include('risk_assessment.urls')),
]
