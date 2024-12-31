import factory

from .models import NotificationSubscription, Scan, ScanIssue


class NotificationSubscriptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = NotificationSubscription

    url = factory.Faker("url")
    email = factory.Faker("email")


class ScanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Scan

    url = factory.Faker("url")


class ScanIssueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ScanIssue

    scan = factory.SubFactory(ScanFactory)
    type = factory.Faker("random_element", elements=ScanIssue.ScanIssueType.values)
    message = factory.Faker("sentence")
