from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from product.models import Product

def index(request):
    products = Product.objects.select_related(
    'category'
).prefetch_related(
    'images',
    'variants'
)

    return render(request,"product/index.html",{products:products})


def productDetails(request, id):

    product = get_object_or_404(
    Product.objects.prefetch_related('images', 'variants')
    .select_related(
        'category',
        'category__parent',
        'category__parent__parent',
        'category__parent__parent__parent',
    ),
    id=id
    )

    breadcrumb = product.category.get_breadcrumb()

    return render(
        request,
        "product/product_details.html",
        {
            "product": product,
            "categories" : breadcrumb
        }
    )

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

    if minPrice_query:
        products = products.filter(base_price__gte=minPrice_query)

    if maxPrice_query:
        products = products.filter(base_price__lte=maxPrice_query)

    if category_query:
        products = products.filter(category__slug=category_query)

    context = {
        "products": products,
        "search_query": search_query,
        "min_price": minPrice_query,
        "max_price": maxPrice_query,
        "category_query": category_query,
    }


    return render(request, "product/search.html", context)