from itertools import cycle

import pytest
from factory import DictFactory, LazyAttribute
from factory.fuzzy import FuzzyChoice
from faker import Faker
from model_bakery import baker

from users.models import UserProfile

faker = Faker()


class UserProfileFactory(DictFactory):
    _first = LazyAttribute(
        lambda obj: faker.unique.first_name_male() if obj._gender == "M" else faker.first_name_female())
    _last = LazyAttribute(
        lambda obj: faker.unique.last_name_male() if obj._gender == "M" else faker.unique.last_name_female())
    _gender = FuzzyChoice(("M", "F"))

    fullname = LazyAttribute(lambda obj: f"{obj._first} {obj._last}")
    image = LazyAttribute(lambda obj: faker.file_name(category='image'))
    is_public = LazyAttribute(lambda obj: faker.random.choice((True, False)))

    class Meta:
        exclude = ("_gender", '_first', '_last')
        rename = {'fullname': 'fullname', 'last': 'last_name', 'email': 'email', 'age': 'age'}


@pytest.mark.django_db
class TestUsers:

    @pytest.fixture
    def test_user_model(self):
        count = UserProfile.objects.count()
        baker.make(
            'users.UserProfile',
            fullname=cycle(UserProfileFactory()['fullname'] for _ in range(10)),
            is_public=cycle(UserProfileFactory()['is_public'] for _ in range(10)),
            password=1,
            _quantity=10,
        )
        count_last = UserProfile.objects.count()

        assert count + 10 == count_last
        return UserProfile.objects.all()

    def test_user_follow_system(self, test_user_model):
        users = test_user_model
        first_five = users[:5]
        last_five = users[5:]
        for i in range(5):
            first_five[i].following.add(last_five[i])
            last_five[i].followers.add(first_five[i])
            last_five[i].following.add(first_five[i])
            first_five[i].followers.add(last_five[i])
        for i in range(5):
            assert first_five[i].following.filter(pk=last_five[i].pk).exists() == last_five[i].following.filter(
                pk=first_five[i].pk).exists()

        for i in range(5):
            assert first_five[i].followers.first().following.get(pk=first_five[i].pk)
