from django.urls import path

from model_status.views import ChangeStatusView

urlpatterns = [
    path('<str:app_label>/<str:model>/<int:object_id>/toggle/<str:status>/', ChangeStatusView.as_view(),
         name='change-status')
]
