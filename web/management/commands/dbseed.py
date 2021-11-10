from faker import Faker
from django.core.management.base import BaseCommand
from organizations.utils import create_organization
from authentication.models import User
from card.models import Card, Template

class Command(BaseCommand):
    help = 'Populate DB with fake data'

    def handle(self, *args, **options):
        fake = Faker()
        templ = Template.objects.create(name='First template')
        owner = User.objects.create_user('test', email='test@test.com', password='123', first_name='Carlos', last_name='Bravo')
        Card.objects.create(user=owner, template=templ)
        org = create_organization(owner, 'CBS Logística', org_user_defaults={'is_admin': True})
        for _ in range(20):
            name = fake.name().split(' ')
            first_name = name[0]
            last_name = name[1]
            email = fake.email()
            user = User.objects.create_user(first_name+'.'+last_name, email=email, password='123', first_name=first_name, last_name=last_name)
            Card.objects.create(user=user, template=templ)
            org.add_user(user)
                