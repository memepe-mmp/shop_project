from django.core.cache import cache
from django.db.models import Count

from .models import Category

CATEGORIES_KEY = "categories_with_counts"

def get_categories_with_counts():
    return cache.get_or_set(
        CATEGORIES_KEY,
        lambda: list(
            Category.objects.annotate(products_count=Count("products")).order_by("name")
        ),
        timeout=600,
    )