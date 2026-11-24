import random

from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from faker import Faker
from catalog.models import Category, Characteristic, Product


class Command(BaseCommand):
    help = "Заполняет базу тестовыми товарами"

    def add_arguments(self, parser):
        parser.add_argument("--products", type=int, default=100_000)

    @transaction.atomic
    def handle(self, *args, **options):
        fake = Faker("ru_RU")
        User = get_user_model()

        users = [
            User.objects.get_or_create(username=f"shop_user_{i}")[0]
            for i in range(20)
        ]

        Category.objects.bulk_create(
            [Category(name=f"Категория {i}") for i in range(50)],
            ignore_conflicts=True,
        )
        Characteristic.objects.bulk_create(
            [Characteristic(name=f"Характеристика {i}") for i in range(200)],
            ignore_conflicts=True,
        )

        categories = list(Category.objects.all())
        characteristics = list(Characteristic.objects.all())
        statuses = [choice[0] for choice in Product.Status.choices]

        total = options["products"]
        batch = 5000
        Through = Product.characteristics.through

        for start in range(0, total, batch):
            size = min(batch, total - start)
            products = Product.objects.bulk_create([
                Product(
                    title=fake.sentence(nb_words=3).rstrip(".")[:200],
                    description=fake.text(max_nb_chars=350),
                    price=Decimal(str(round(random.uniform(50.0, 150000.0), 2))),
                    status=random.choice(statuses),
                    category=random.choice(categories),
                    author=random.choice(users),
                )
                for _ in range(size)
            ])

            Through.objects.bulk_create([
                Through(product_id=prod.pk, characteristic_id=char.pk)
                for prod in products
                for char in random.sample(characteristics, k=random.randint(2, 5))
            ])

            self.stdout.write(f"Создано {start + size} из {total}")
