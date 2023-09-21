from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField, ImageField, TextField, BooleanField, ManyToManyField


class UserProfile(AbstractUser):
    fullname = CharField(max_length=100, null=True)
    password = CharField(max_length=255, null=True, blank=True)
    image = ImageField(upload_to='profile-image/', null=True, blank=True)
    bio = TextField(blank=True, null=True)
    is_public = BooleanField(default=True)
    followers = ManyToManyField('self', 'my_followers', symmetrical=False)
    following = ManyToManyField('self', 'my_following', symmetrical=False)

    @property
    def following_count(self):
        return self.following.count()

    @property
    def followers_count(self):
        return self.followers.count()

    @property
    def avatar(self):
        default = 'https://upload.wikimedia.org/wikipedia/commons/a/ac/Default_pfp.jpg'
        try:
            return self.image.url if self.image else default
        except (KeyError, AttributeError, TypeError):
            return default

    def __str__(self):
        return self.fullname
