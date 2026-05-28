from django.shortcuts import get_object_or_404, render

def index(request):
    return render(request,"product/index.html")


def productDetails(request, id):
    return render(request,"product/product_details.html", {"id": id})


def searchProduct(request):
    package_query = request.GET.get("t", "").strip()
    
    # packages = (
    #     TravelPackage.objects.prefetch_related('images').filter(name__istartswith=package_query)
    #     if package_query
    #     else TravelPackage.objects.prefetch_related('images').all()
    # )

    # paginator = Paginator(packages, 9)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    return render(request, 'product/search.html', {
        # 'page_obj': page_obj,
        'query': package_query,
    })