from phonenumber_field.modelfields import PhoneNumberField
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    USERCHOICES = (
        (0, 'Audience'),
        (1, 'Player'),
    )
    college = models.CharField(max_length=200)
    contact = PhoneNumberField()
    money = models.IntegerField(default='0')
    type = models.BooleanField(choices=USERCHOICES, default='0')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Profile)
def give_money_audience(sender, instance, **kwargs):
    if instance.type == 0:
        instance.money = 1000000
