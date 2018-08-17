from django.conf import settings
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save

from .utils import code_generator

User = settings.AUTH_USER_MODEL


class ProfileManager(models.Manager):
    def toogle_follow(self, requested_user, username_to_toggle):
        profile_ = Profile.objects.get(user__username__iexact=username_to_toggle)
        user = requested_user  # Logged in user.

        is_following = False
        if user in profile_.followers.all():
            profile_.followers.remove(user)
        else:
            is_following = True
            profile_.followers.add(user)

        return profile_, is_following


class Profile(models.Model):
    user = models.OneToOneField(User)  # user.profile
    followers = models.ManyToManyField(User, related_name='is_following', blank=True)  # user.profile.followers.all()
    # following = models.ManyToManyField(User, related_name='following', blank=True)  # user.profile.following.all()
    activation_key = models.CharField(max_length=36, blank=True, null=True)
    activated = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = ProfileManager()

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def send_activation_email(self, path=''):
        if not self.activated:
            path_ = path[:-2] + str(self.activation_key)

            subject = 'Activation Account'
            from_email = settings.DEFAULT_FROM_EMAIL
            message = f'Activate your account here: {path_}'
            recipient_list = [self.user.email]
            html_message = f'<h3>Activate your account here: {path_}</h3> '

            sent_mail = send_mail(subject, message, from_email, recipient_list, fail_silently=False,
                                  html_message=html_message)

            return sent_mail


def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)

        # Adding to the created user a default follower profile.
        default_user_profile = Profile.objects.get_or_create(user__id=1)[0]
        default_user_profile.followers.add(instance)

        # Adding to the created user a default following profile.
        profile.followers.add(default_user_profile.user)
        profile.followers.add(3)

        # Adding activation key.
        profile.activation_key = code_generator(profile)
        profile.save()


post_save.connect(post_save_user_receiver, sender=User)
