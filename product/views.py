from itertools import groupby

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

from product.models import Product, ProductVariant, Category


CATEGORY_LABELS = {
    'men-watches': "Men's Watches",
    'women-watches': "Women's Watches",
    'smart-watches': 'Smart Watches',
    'luxury-watches': 'Luxury Watches',
    'sports-watches': 'Sports Watches',
}


from django.db.models import Count

CATEGORY_META = {
    'men-watches': {'icon': 'watch', 'desc': 'Engineered timepieces built for everyday performance.'},
    'women-watches': {'icon': 'watch_later', 'desc': 'Elegant designs crafted to complement any style.'},
    'smart-watches': {'icon': 'smartphone', 'desc': 'Connected wearables with health and fitness tracking.'},
    'luxury-watches': {'icon': 'diamond', 'desc': 'Haute horology with premium materials and finishing.'},
    'sports-watches': {'icon': 'fitness_center', 'desc': 'Rugged, feature-rich watches built for the active life.'},
}


def index(request):
    categories = (
        Category.objects
        .filter(slug__in=['men-watches', 'women-watches', 'smart-watches', 'luxury-watches', 'sports-watches'])
        .annotate(product_count=Count('products'))
        .order_by('name')
    )

    featured_products = Product.objects.select_related('category').prefetch_related('images', 'variants')

    main_featured = featured_products.filter(category__slug='luxury-watches').order_by('-base_price').first()
    secondary_featured = list(featured_products.exclude(id=main_featured.id if main_featured else None).order_by('-base_price')[:2])

    return render(request, "product/index.html", {
        "categories": categories,
        "category_meta": CATEGORY_META,
        "main_featured": main_featured,
        "secondary_featured": secondary_featured,
    })


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
    variants = product.variants.all().order_by('type')
    variant_groups = {
    k: list(v) for k, v in groupby(variants, key=lambda x: x.type)
        }
    
    context_variant_groups = {
    'groups': [
        {'label': k, 'variants': v}
        for k, v in variant_groups.items()
    ]
}
    return render(request, 'product/product_details.html', {
    'product': product,
    'variant_groups': context_variant_groups['groups'],
    'breadcrum' : breadcrumb
})


def searchProduct(request):
    search_query = request.GET.get("s", "").strip()
    minPrice_query = request.GET.get("min-price", "").strip()
    maxPrice_query = request.GET.get("max-price", "").strip()
    category_query = request.GET.get("c", "").strip()
    sort_query = request.GET.get("sort", "").strip()
    variant_filters = request.GET.getlist("v")

    products = Product.objects.select_related('category').prefetch_related('images', 'variants').order_by('id')

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

    if variant_filters:
        products = products.filter(variants__id__in=variant_filters).distinct()

    if sort_query == 'price_asc':
        products = products.order_by('base_price')
    elif sort_query == 'price_desc':
        products = products.order_by('-base_price')
    elif sort_query == 'name':
        products = products.order_by('name')

    paginator = Paginator(products, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    category_label = CATEGORY_LABELS.get(category_query, '') if category_query else ''

    filter_options = []
    if category_query:
        excluded_types = {'color'}
        variant_types = (
            ProductVariant.objects
            .filter(product__category__slug=category_query)
            .exclude(type__in=excluded_types)
            .values_list('type', flat=True)
            .distinct()
        )
        for vtype in variant_types:
            seen = set()
            values = []
            for v in ProductVariant.objects.filter(
                product__category__slug=category_query, type=vtype
            ).order_by('value'):
                if v.value not in seen:
                    seen.add(v.value)
                    values.append({'value': v.value, 'min_id': str(v.id)})
            filter_options.append({'type': vtype, 'values': values})

    all_categories = Category.objects.filter(slug__in=['men-watches', 'women-watches', 'smart-watches', 'luxury-watches', 'sports-watches']).order_by('name')

    context = {
        "products": page_obj,
        "page_obj": page_obj,
        "search_query": search_query,
        "min_price": minPrice_query,
        "max_price": maxPrice_query,
        "category_query": category_query,
        "category_label": category_label,
        "sort_query": sort_query,
        "variant_filters": [str(v) for v in variant_filters],
        "filter_options": filter_options,
        "all_categories": all_categories,
        "total_results": paginator.count,
    }

    return render(request, "product/search.html", context)