from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from rest_framework.exceptions import ValidationError

from config.settings import AUTH_USER_MODEL


class Friend(models.Model):
    to_user = models.ForeignKey(
        AUTH_USER_MODEL,
        models.CASCADE,
        related_name="friends",
        verbose_name="Отправитель",
    )
    from_user = models.ForeignKey(AUTH_USER_MODEL, models.CASCADE, verbose_name="Получатель")
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _("Friend")
        verbose_name_plural = _("Friends")
        unique_together = ("from_user", "to_user")

    def __str__(self) -> str:
        return f"User #{self.to_user} is subscribed with #{self.from_user}"

    def save(self, *args, **kwargs) -> None:
        if self.to_user == self.from_user:
            raise ValidationError("Users cannot be friends with themselves.")
        super().save(*args, **kwargs)
