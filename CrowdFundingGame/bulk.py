from django.contrib.auth import get_user_model
import random
from CrowdFundingGame.models import *
User = get_user_model()


for i in range(100):
    user = User.objects.create_user(
                username='user%d' %random.randint(1, 15000) ,
                password='pitchit',
                )


    print(user)

#User.objects.bulk_create(users)