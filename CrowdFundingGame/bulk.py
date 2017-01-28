from django.contrib.auth import get_user_model
import random
from CrowdFundingGame.models import *
User = get_user_model()
users = []

for i in range(100):
    user = User(
                username='user%d' %random.randint(1, 15000) ,
                password='pbkdf2_sha256$30000$O7fqpkuf0dUD$lx6BdckGtenISV6DNijUgvKHahe/SiCK+77q52S1qDA=',

                )
    users.append(user)
    user.save()
    print(user)

#User.objects.bulk_create(users)