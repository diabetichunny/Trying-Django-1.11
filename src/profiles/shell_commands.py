from django.contrib.auth import get_user_model

User = get_user_model()

random_ = User.objects.last()

# My Followers
random_.profile.followers.all()

# Who I Follow
random_.is_following.all()
