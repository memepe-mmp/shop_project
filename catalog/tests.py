
from django.test import TestCase
from django.contrib.auth import get_user_model
from unicodedata import category
from django.core.cache import cache

from .models import Category, Characteristic, Product

class IndexQueriesTest(TestCase):
    def setUp(self):
        cache.clear()
        user = get_user_model().objects.create(username="u")
        cat = Category.objects.create(name="c")
        char = Characteristic.objects.create(name="char")

        for i in range(30):
            product = Product.objects.create(
                title=f"Товар {i}",
                description="Описание",
                price="1000.00",
                status=Product.Status.IN_STOCK,
                author=user,
                category=cat,
            )
            product.characteristics.add(char)

    def test_query_count_does_not_grow(self):
        with self.assertNumQueries(4):
            self.client.get("/")