from django.urls import path, include

urlpatterns = [
    path('status', include('model_status.urls'))
]
