from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    USERCHOICES = (
        ('A', 'Audience'),
        ('P', 'Player'),
    )
    college = models.CharField(max_length=200)
    money = models.IntegerField(default='0')
    type = models.CharField(choices=USERCHOICES,max_length=1)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Profile)
def give_money_audience(sender, instance, **kwargs):
    if instance.type == 'A':
        instance.money = 1000000
