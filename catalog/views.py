from django.shortcuts import render, redirect
from .forms import ProductForm
from .models import Category, Product
from django.shortcuts import get_object_or_404
from decimal import Decimal, InvalidOperation
from django.db.models import Count, Q

def _parse_decimal(value):
    if not value:
        return None
    try:
        return Decimal(value)
    except InvalidOperation:
        return None

def index(request):
    products = Product.objects.all()

    q = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "").strip()
    status = request.GET.get("status", "").strip()
    min_price = _parse_decimal(request.GET.get("min_price", "").strip())
    max_price = _parse_decimal(request.GET.get("max_price", "").strip())
    sort = request.GET.get("sort", "newest").strip()

    if q:
        products = products.filter(title__icontains=q)
    if category_id.isdigit():
        products = products.filter(category_id=int(category_id))
    if status in dict(Product.Status.choices):
        products = products.filter(status=status)
    if min_price is not None:
        products = products.filter(price__gte=min_price)
    if max_price is not None:
        products = products.filter(price__lte=max_price)

    sort_map = {
        "newest": ["-created_at", "-id"],
        "oldest": ["created_at", "id"],
        "price_asc": ["price", "-id"],
        "price_desc": ["-price", "-id"],
    }
    products = products.order_by(*sort_map.get(sort, sort_map["newest"]))

    total = len(products)
    products = products[:300]
    categories = Category.objects.all()

    return render(request, "catalog/product_list.html", {
        "products": products,
        "total": total,
        "categories": categories,
        "statuses": Product.Status.choices,
        "current_sort": sort,
    })

def product_detail(request, pk):
    product = get_object_or_404(
        Product.objects.select_related("category", "author").prefetch_related("characteristics"),
        pk=pk,
    )
    feature_ids = list(product.characteristics.values_list("pk", flat=True))

    similar_products = Product.objects.none()
    if feature_ids:
        similar_products = (
            Product.objects.filter(category=product.category)
            .exclude(pk=product.pk)
            .filter(characteristics__in=feature_ids)
            .annotate(
                common_features=Count(
                    "characteristics",
                    filter=Q(characteristics__in=feature_ids),
                )
            )
            .select_related("category", "author")
            .prefetch_related("characteristics")
            .order_by("-common_features", "-created_at", "-id")[:4]
        )

    return render(request, "catalog/product_detail.html", {"product": product, "similar_products": similar_products,},)

def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("catalog:index")
    else:
            form = ProductForm()
    return render(request, "catalog/product_form.html", {"form": form, "title": "Новый товар"})

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect("catalog:detail", pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, "catalog/product_form.html", {"form": form, "title": "Редактирование товара"},)

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect("catalog:index")
    return render(request, "catalog/product_confirm_delete.html", {"product": product})
