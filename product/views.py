from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from product.models import Product

def index(request):
    products = Product.objects.all()

    return render(request,"product/index.html",{products:products})


def productDetails(request, id):
    return render(request,"product/product_details.html", {"id": id})


def searchProduct(request):
    search_query = request.GET.get("s", "").strip()
    minPrice_query = request.GET.get("min-price", "").strip()
    maxPrice_query = request.GET.get("max-price", "").strip()
    category_query = request.GET.get("c", "").strip()

    products = Product.objects.all()

    # Search by name or description
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # Filter by minimum price
    if minPrice_query:
        products = products.filter(price__gte=minPrice_query)

    # Filter by maximum price
    if maxPrice_query:
        products = products.filter(price__lte=maxPrice_query)

    # Filter by category slug
    if category_query:
        products = products.filter(category__slug=category_query)

    context = {
        "products": products,
        "search_query": search_query,
        "min_price": minPrice_query,
        "max_price": maxPrice_query,
        "category_query": category_query,
    }
    print(context)

    return render(request, "product/search.html", context)