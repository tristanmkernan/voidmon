import factory

from .models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("email")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    @factory.post_generation
    def set_password(obj, create, extracted, **kwargs):
        password = extracted if extracted else "password123"
        obj.set_password(password)
        if create:
            obj.save()
