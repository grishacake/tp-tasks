from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)

    page_number = request.GET.get("page")

    try:
        page = paginator.get_page(page_number)
    except PageNotAnInteger:
        page = paginator.get_page(1)
    except EmptyPage:
        page = paginator.get_page(paginator.num_pages)

    return page
