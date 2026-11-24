from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Product
from .services import CATEGORIES_KEY

@receiver([post_save, post_delete], sender=Product)
def reset_category_counts(sender, **kwargs):
    cache.delete(CATEGORIES_KEY)