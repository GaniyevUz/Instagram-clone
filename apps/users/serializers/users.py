from rest_framework.fields import IntegerField, HiddenField, CurrentUserDefault, DateTimeField
from rest_framework.fields import IntegerField, HiddenField, CurrentUserDefault, DateTimeField
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import ModelSerializer

from users.models import UserProfile


class UserProfileSerializer(ModelSerializer):
    following_count = IntegerField(read_only=True)
    followers_count = IntegerField(read_only=True)
    date_joined = DateTimeField(read_only=True)

    class Meta:
        model = UserProfile
        fields = "id", "fullname", "username", "email", "image", "bio", "is_public", "following_count", "followers_count", "date_joined"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # data['followers'] = instance.followers_count
        # data['following'] = instance.following_count
        return data


class UserViewProfileModelSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'fullname', 'username', 'image')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context['request']
        data['is_followed'] = False
        if request and (user := getattr(request, 'user')) and user.is_authenticated:
            data['is_followed'] = user.following.filter(id=instance.id).exists()
        return data


class UserFollowModelSerializer(ModelSerializer):
    followers = UserViewProfileModelSerializer(many=True)
    following = UserViewProfileModelSerializer(many=True)

    class Meta:
        model = UserProfile
        fields = ('following', 'followers')

    def create(self, validated_data):
        return super().create(validated_data)


class UserFollowingModelSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    username = SlugRelatedField(queryset=UserProfile.objects.all(), slug_field='username')

    class Meta:
        model = UserProfile
        fields = ('username', 'user')

    def create(self, validated_data):
        user: UserProfile = validated_data['user']
        follow_user = validated_data['username']
        # if user.following.filter(id=follow_user.id).first():
        #     user.following.remove(follow_user)
        #     follow_user.followers.remove(user)
        #     follow_user.save()
        #     user.save()
        # else:
        user.following.add(follow_user)
        user.save()
        follow_user.followers.add(user)
        follow_user.save()
        return user


def to_representation(self, instance):
    return {'message': "you've followed successfully"}
