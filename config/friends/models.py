from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db import models
from rest_framework.exceptions import ValidationError


from config.settings import AUTH_USER_MODEL

class FriendshipManager(models.Manager):
    def friends(self, user):
        """ Return a list of all friends """
        # key = cache_key("friends", user.pk)
        # friends = cache.get(key)
        # if friends is None:


        # qs = Friend.objects.select_related("from_user").filter(to_user=user1)
        # friends = qs
        #     [u.from_user for u in qs]
        #     cache.set(key, friends)
        #
        return True

class Friend(models.Model):
    to_user = models.ForeignKey(AUTH_USER_MODEL, models.CASCADE, related_name="friends")
    from_user = models.ForeignKey(
        AUTH_USER_MODEL, models.CASCADE, related_name="_unused_friend_relation"
    )
    created = models.DateTimeField(default=timezone.now)

    objects = FriendshipManager()

    class Meta:
        verbose_name = _("Friend")
        verbose_name_plural = _("Friends")
        unique_together = ("from_user", "to_user")

    def __str__(self):
        return f"User #{self.to_user_id} is friends with #{self.from_user_id}"

    def save(self, *args, **kwargs):
        # Ensure users can't be friends with themselves
        if self.to_user == self.from_user:
            raise ValidationError("Users cannot be friends with themselves.")
        super().save(*args, **kwargs)