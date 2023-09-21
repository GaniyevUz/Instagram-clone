from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db.models import Model, TextField, ForeignKey, CASCADE, ManyToManyField, FileField, CharField, \
    DateTimeField

from shared.models import BaseModel, unique_id, CustomFileExtensionValidator

file_ext_validator = CustomFileExtensionValidator(('mp4', 'mkv', 'avi', 'webm', '3gp', 'jpg', 'jpeg', 'png', 'webp'))


class Post(BaseModel):
    id = CharField(primary_key=True, default=unique_id, max_length=36)
    caption = TextField(null=True, blank=True)
    author = ForeignKey('users.UserProfile', on_delete=CASCADE)
    media = ManyToManyField('content.Media', related_name='medias')
    location = CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.caption

    @property
    def get_number_of_likes(self):
        return self.likes.count()

    @property
    def get_number_of_comments(self):
        return self.comments.count()


class Reel(BaseModel):
    id = CharField(primary_key=True, default=unique_id, max_length=36)
    caption = TextField(null=True, blank=True)
    author = ForeignKey('users.UserProfile', on_delete=CASCADE)
    media = FileField(upload_to='reels/', validators=[FileExtensionValidator(['mp4', 'avi', 'mkv'])])
    location = CharField(max_length=255, null=True, blank=True)

    @property
    def get_number_of_likes(self):
        return self.likes.count()

    @property
    def get_number_of_comments(self):
        return self.comments.count()


class Media(Model):
    file = FileField(upload_to='posts/', validators=(file_ext_validator,))


class Comment(Model):
    parent = ForeignKey('self', CASCADE, null=True, related_name='reply_comments')
    user = ForeignKey('users.UserProfile', CASCADE)
    comment = CharField(max_length=255)
    posted_on = DateTimeField(auto_now_add=True)
    post = ForeignKey('content.Post', on_delete=CASCADE, related_name='comments', null=True)
    reel = ForeignKey('content.Reel', on_delete=CASCADE, related_name='comments', null=True)

    def __str__(self):
        return self.comment

    class Meta:
        unique_together = ('post', 'reel')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not (self.post or self.reel):
            raise ValidationError('You must specify one of the following fields to save comments, fields: "post, reel"')
        super().save(force_insert, force_update, using, update_fields)


class LikePost(Model):
    post = ForeignKey('content.Post', CASCADE, related_name='likes')
    user = ForeignKey('users.UserProfile', CASCADE, related_name='liked_posts')

    def __str__(self):
        return 'Like: ' + self.user.username


class LikeReel(Model):
    reel = ForeignKey('content.Reel', CASCADE, related_name='likes')
    user = ForeignKey('users.UserProfile', CASCADE, related_name='liked_reels')

    def __str__(self):
        return 'Like: ' + self.user.username


class LikeComment(Model):
    comment = ForeignKey('content.Comment', CASCADE, related_name='likes')
    user = ForeignKey('users.UserProfile', CASCADE, related_name='liked_comments')

    def __str__(self):
        return 'Like: ' + self.user.username
