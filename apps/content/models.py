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
    likes = ManyToManyField('content.Like', related_name='posts')
    comments = ManyToManyField('content.CommentPost', related_name='posts')

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
    media = FileField(upload_to='reels/', validators=[CustomFileExtensionValidator(['mp4', 'avi', 'mkv'])])
    location = CharField(max_length=255, null=True, blank=True)
    likes = ManyToManyField('content.Like', related_name='reels')
    comments = ManyToManyField('content.CommentReel', related_name='reels')

    @property
    def get_number_of_likes(self):
        return self.likes.count()

    @property
    def get_number_of_comments(self):
        return self.comments.count()


class Media(Model):
    file = FileField(upload_to='posts/', validators=(file_ext_validator,))


class CommentReel(Model):
    user = ForeignKey('users.UserProfile', CASCADE)
    comment = CharField(max_length=255)
    posted_on = DateTimeField(auto_now_add=True)
    reel = ForeignKey('content.Reel', on_delete=CASCADE)

    def __str__(self):
        return self.comment


class CommentPost(CommentReel):
    reel = None
    post = ForeignKey('content.Post', on_delete=CASCADE)

    def __str__(self):
        return self.comment


class Like(Model):
    user = ForeignKey('users.UserProfile', CASCADE)

    def __str__(self):
        return 'Like: ' + self.user.username
