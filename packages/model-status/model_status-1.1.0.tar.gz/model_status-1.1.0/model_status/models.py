from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext as _

UserModel = get_user_model()


class Status(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_PENDING = 'pending'
    STATUS_PUBLISHED = 'published'
    STATUS_ARCHIVED = 'archived'
    STATUS_SUSPENDED = 'suspended'
    STATUS_CANCELED = 'canceled'
    STATUS_REJECTED = 'rejected'
    STATUS_APPROVED = 'approved'
    STATUS_STARTED = 'started'
    STATUS_ENDED = 'ended'

    STATUS_DRAFT_CHOICE = (STATUS_DRAFT, _("Draft"))
    STATUS_PENDING_CHOICE = (STATUS_PENDING, _("Pending"))
    STATUS_PUBLISHED_CHOICE = (STATUS_PUBLISHED, _("Published"))
    STATUS_ARCHIVED_CHOICE = (STATUS_ARCHIVED, _("Archived"))
    STATUS_SUSPENDED_CHOICE = (STATUS_SUSPENDED, _("Suspended"))
    STATUS_CANCELED_CHOICE = (STATUS_CANCELED, _("Canceled"))
    STATUS_REJECTED_CHOICE = (STATUS_REJECTED, _("Rejected"))
    STATUS_APPROVED_CHOICE = (STATUS_APPROVED, _("Approved"))
    STATUS_STARTED_CHOICE = (STATUS_STARTED, _("Started"))
    STATUS_ENDED_CHOICE = (STATUS_ENDED, _("Ended"))

    STATUS_CHOICES = (
        STATUS_DRAFT_CHOICE,
        STATUS_PENDING_CHOICE,
        STATUS_PUBLISHED_CHOICE,
        STATUS_ARCHIVED_CHOICE,
        STATUS_SUSPENDED_CHOICE,
        STATUS_CANCELED_CHOICE,
        STATUS_REJECTED_CHOICE,
        STATUS_APPROVED_CHOICE,
        STATUS_STARTED_CHOICE,
        STATUS_ENDED_CHOICE,
    )

    class Meta:
        verbose_name = _("Status")
        verbose_name_plural = _("Status")

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='%(class)s_activity_log',
                             null=True, blank=True)
    at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_DRAFT)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    @property
    def get_status(self):
        return dict(self.STATUS_CHOICES).get(self.status)


class HasStatus(models.Model):
    STATUS_MESSAGES = {
        'success': _("Status Updated Successfully"),
        "permission_denied": _("You don't have permission to perform this action"),
    }
    STATUS_CHOICES = ()
    STATUS_PERMISSIONS = {}

    class Meta:
        abstract = True

    status_log = GenericRelation(Status, related_query_name='%(class)s_status')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=Status.STATUS_PENDING)

    def get_status_permissions(self, status):
        return self.STATUS_PERMISSIONS

    @property
    def get_status(self):
        return dict(self.STATUS_CHOICES).get(self.status)

    def update_status(self, status, user):
        self.status = status
        self.save()
        self.status_log.create(user=user, status=status)
        return True, self.STATUS_MESSAGES.get('success')


