from typing import List
import os
from django.core.management.base import BaseCommand
from model_bakery import baker
import json
from cargo.models import Logistic
import random
from account.models import User
from utils.base.fields import TrackingCodeField
from utils.base.progress_bar import progressBar


PASSWORD = 'password'


class Command(BaseCommand):
    help = "seed database for testing and development."
    seeders: List['Seeder'] = []

    def add_arguments(self, parser):
        parser.add_argument('--clean', type=bool,
                            help='Clean database before seeding')

    def handle(self, *args, **options):
        self.load_seeders()
        TrackingCodeField.register(baker)

        clean = options.get('clean')
        if clean:
            self.run_clean()

        self.run_seed()

    def load_seeders(self):
        seed_data = self.load_seed_data()
        self.seeders = [
            LogisticSeeder(self, seed_data),
            LogisticPriceSeeder(self, seed_data),
        ]

    def load_seed_data(self):
        seed_data = None
        DIR = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(DIR, 'seed.json')) as f:
            seed_data = json.load(f)
        if not seed_data:
            self.stderr.write(self.style.ERROR('No seed data found'))
            return
        return seed_data

    def run_seed(self):
        self.stdout.write('Running seeders...')
        for seeder in self.seeders:
            seeder.run()
        self.stdout.write(self.style.SUCCESS('Done.'))

    def run_clean(self):
        self.stdout.write('Cleaning database...')
        for seeder in self.seeders:
            seeder.clean()
        self.stdout.write(self.style.SUCCESS('Done.'))


class Seeder:
    def __init__(self, command: Command, seed_data: dict):
        self.seed_data = seed_data
        self.command = command

    @property
    def style(self):
        return self.command.style

    @property
    def stdout(self):
        return self.command.stdout

    @property
    def stderr(self):
        return self.command.stderr

    def run(self):
        self.stdout.write(f'Running {self.__class__.__name__} ...')
        created, quantity = self.seed()
        self.stdout.write(self.style.SUCCESS(
            f'Seeded {created} of {quantity} {self.__class__.__name__}'))

    def seed(self):
        raise NotImplementedError

    def clean(self):
        raise NotImplementedError

    def progress_bar(self, items):
        return progressBar(items, prefix='Progress:', suffix='Complete', length=50)


class LogisticSeeder(Seeder):
    def seed(self):
        self.stdout.write('Seeding logistics...')
        logistics = self.seed_data['logistics']
        created = 0
        quantity = 0

        def __creator(logistic):
            nonlocal created, quantity
            name = logistic['name']
            email = logistic['email']
            quantity += 1
            if not Logistic.objects.filter(name=name).exists():
                logistic_user = baker.make(
                    Logistic,
                    name=name,
                    user__email=email,
                )
                logistic_user.user.set_password(PASSWORD)
                logistic_user.user.save()
                logistic_user.user.profile.account_type = 'logistics'
                logistic_user.user.profile.approved = True
                logistic_user.user.profile.save()
                created += 1

        for logistic in self.progress_bar(logistics):
            __creator(logistic)

        return created, quantity

    def clean(self):
        self.stdout.write('Cleaning logistics...')
        logistics = self.seed_data['logistics']
        emails = [logistic['email'] for logistic in logistics]
        User.objects.filter(email__in=emails).delete()
        self.stdout.write(self.style.SUCCESS('Done.'))


class LogisticPriceSeeder(Seeder):
    def seed(self):
        self.stdout.write('Seeding logistic package prices ...')
        locations = self.seed_data['locations']
        created = 0
        quantity = 0
        logistics = Logistic.objects.all()
        items = []

        def __creator(_from, _to, _logistic):
            nonlocal created, quantity
            quantity += 1
            exists = _logistic.pricepackage_set.filter(
                from_location=_from,
                to_location=_to
            ).exists()
            if not exists:
                baker.make(
                    'cargo.PricePackage',
                    logistic=_logistic,
                    from_location=_from,
                    to_location=_to,
                    price=random.randint(100, 1000),
                    pickup_time=random.randint(1, 5),
                    delivery_date=random.randint(1, 5),
                )
                created += 1

        for logistic in logistics:
            for location in locations:
                items.append({
                    '_to': location['to'],
                    '_from': location['from'],
                    '_logistic': logistic,
                })

        for item in self.progress_bar(items):
            __creator(**item)

        return created, quantity

    def clean(self):
        return
