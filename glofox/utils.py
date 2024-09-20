from rest_framework import status
from datetime import timedelta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .enums import PAGE_SIZE

def handle_response(data, status_code=status.HTTP_200_OK):
    if status_code == status.HTTP_204_NO_CONTENT:
        return {}, 204  
    return {"data": data}, status_code

def handle_error(error_message, status_code):
    if isinstance(error_message, dict):
        return {"errors": error_message}, status_code
    return {"error": str(error_message)}, status_code

def handle_request_result(result, status_code):
    if isinstance(result, dict) and "errors" in result:  
        return handle_error(result["errors"], status_code)

    if status_code < 400:  
        return handle_response(result, status_code)
    else:  
        return handle_error(result, status_code)

def date_range(start_date, end_date):
        for n in range((end_date - start_date).days + 1):
            yield start_date + timedelta(n)

def paginate_data(data, page_number):
    page_size = PAGE_SIZE
    paginator = Paginator(data, page_size)
    
    try:
        paginated_data = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_data = paginator.page(1)
    except EmptyPage:
        paginated_data = paginator.page(paginator.num_pages)
    
    return {
        'total_pages': paginator.num_pages,
        'total_items': paginator.count,
        'current_page': page_number,
        'page_size': page_size,
        'data': paginated_data.object_list
    }