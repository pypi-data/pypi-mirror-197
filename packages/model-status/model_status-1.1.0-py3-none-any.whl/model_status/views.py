from django.apps import apps
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views import View

from model_status.models import HasStatus


class ChangeStatusView(LoginRequiredMixin, View):
    def post(self, request, app_label, model, object_id, status, *args, **kwargs):
        model_class = apps.get_model(app_label, model)
        assert issubclass(model_class, HasStatus)
        instance = model_class.objects.get(pk=object_id)

        if status not in dict(instance.STATUS_CHOICES).keys():
            raise ValueError("invalid status")

        status_method = 'toggle_%s' % status
        if hasattr(instance, status_method) and callable(getattr(instance, status_method)):
            success, message = getattr(instance, status_method)(request)
        else:
            if hasattr(instance, 'STATUS_PERMISSIONS'):
                permission = instance.get_status_permissions(status).get(status)
                if permission:
                    if type(permission) is not list:
                        permission = [permission, []]
                    assert request.user.has_perm(permission[0] % permission[1])

            success, message = instance.update_status(status, request.user)

        return JsonResponse({"message": message})
