from product.models import Category

NAVBAR_SLUGS = ['cpus', 'gpus', 'storage', 'ram', 'motherboards']


def navbar_categories(request):
    return {
        'navbar_categories': Category.objects.filter(slug__in=NAVBAR_SLUGS).order_by('name'),
    }
