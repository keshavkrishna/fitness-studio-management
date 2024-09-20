from django.http import JsonResponse
from rest_framework.views import APIView
from .services import UserService, StudioService, ClassService, BookingService
from .utils import handle_request_result, paginate_data
from rest_framework import status

class UserView(APIView):
    def get(self, request, user_id=None):
        data = request.GET.dict()
        result, status_code = UserService.get_user(user_id)
        if user_id is None and status_code < status.HTTP_400_BAD_REQUEST:
            page = data.get('page', 1)
            result = paginate_data(result, page) 
        response, status_code = handle_request_result(result, status_code)
        return JsonResponse(response, status=status_code)

    def post(self, request):
        data = request.data
        result, status = UserService.create_user(data)
        response, status = handle_request_result(result, status)
        return JsonResponse(response, status=status)

    def put(self, request, user_id):
        data = request.data
        data['user_id'] = user_id
        result, status = UserService.update_user(data)
        response, status = handle_request_result(result, status)
        return JsonResponse(response, status=status)
    
    def patch(self, request, user_id):
        data = request.data
        data['user_id'] = user_id
        result, status = UserService.update_user(data, partial=True)
        response, status = handle_request_result(result, status)
        return JsonResponse(response, status=status)

    def delete(self, request, user_id):
        result, status = UserService.delete_user(user_id)
        response, status = handle_request_result(result, status)
        return JsonResponse(response, status=status)

class StudioView(APIView):
    def get(self, request, studio_id=None):
        data = request.GET.dict()
        result, status_code = StudioService.get_studio(studio_id)
        if studio_id is None and status_code < status.HTTP_400_BAD_REQUEST:
            page = data.get('page', 1)
            result = paginate_data(result, page) 
        response, status_code = handle_request_result(result, status_code)
        return JsonResponse(response, status=status_code)
    def post(self, request):
        data = request.data
        result, status = StudioService.create_studio(data)
        response, status = handle_request_result(result, status)
        return JsonResponse(response, status=status)

    def put(self, request, studio_id):
        data = request.data
        result, status = StudioService.update_studio(studio_id, data)
        response, status = handle_request_result(result, status)
        return JsonResponse(response, status=status)
    
    def patch(self, request, studio_id):
        data = request.data
        result, status = StudioService.update_studio(studio_id, data, partial=True)
        response, status = handle_request_result(result, status)
        return JsonResponse(response, status=status)

    def delete(self, request, studio_id):
        result, status = StudioService.delete_studio(studio_id)
        response, status = handle_request_result(result, status)
        return JsonResponse(response, status=status)

class ClassView(APIView):
    def get(self, request, class_id=None):
        data = request.GET.dict()
        data['class_id'] = class_id
        result, status_code = ClassService.get_class(data)
        if class_id is None and status_code < status.HTTP_400_BAD_REQUEST:
            page = data.get('page', 1)
            result = paginate_data(result, page) 
        response, status_code = handle_request_result(result, status_code)
        return JsonResponse(response, status=status_code)

    def post(self, request):
        data = request.data
        result, status = ClassService.create_class(data)
        response, status = handle_request_result(result, status)
        return JsonResponse(response, status=status)

    def put(self, request, class_id):
        data = request.data
        data['class_id'] = class_id
        result, status = ClassService.update_class(data)
        response, status = handle_request_result(result, status)
        return JsonResponse(response, status=status)

    def patch(self, request, class_id):
        data = request.data
        data['class_id'] = class_id
        result, status = ClassService.update_class(data, partial=True)
        response, status = handle_request_result(result, status)
        return JsonResponse(response, status=status)


    def delete(self, request, class_id):
        result, status = ClassService.delete_class(class_id)
        response, status = handle_request_result(result, status)
        return JsonResponse(response, status=status)

class BookingView(APIView):
    def get(self, request, booking_id=None):
        data = request.GET.dict()
        data['booking_id'] = booking_id
        result, status_code = BookingService.get_bookings(data)
        if booking_id is None and status_code < status.HTTP_400_BAD_REQUEST:
            page = data.get('page', 1)
            result = paginate_data(result, page) 
        response, status_code = handle_request_result(result, status_code)
        return JsonResponse(response, status=status_code)

    def post(self, request):
        data = request.data
        result, status = BookingService.create_booking(data)
        response, status = handle_request_result(result, status)
        return JsonResponse(response, status=status)
    
    def put(self, request, booking_id):
        data = request.data
        result, status = BookingService.update_booking(booking_id, data, partial=False)
        response, status = handle_request_result(result, status)
        return JsonResponse(response, status=status)

    def patch(self, request, booking_id):
        data = request.data
        result, status = BookingService.update_booking(booking_id, data, partial=True)
        response, status = handle_request_result(result, status)
        return JsonResponse(response, status=status)
    
    def delete(self, request, booking_id):
        result, status = BookingService.delete_booking(booking_id)
        response, status = handle_request_result(result, status)
        return JsonResponse(response, status=status)

class ClassAvailabilityView(APIView):
    def get(self, request, class_id):
        data = request.GET.dict()
        result, status_code = ClassService.get_class_availability(class_id)
        page = data.get('page', 1)
        if status_code < status.HTTP_400_BAD_REQUEST:
            result['availability'] = paginate_data(result['availability'], page) 
        response, status_code = handle_request_result(result, status_code)
        return JsonResponse(response, status=status_code)


class MemberDashboardView(APIView):
    def get(self, request, user_id):
        data = request.GET.dict()
        only_upcoming = data.get('upcoming', 0) 
        result, status_code = UserService.get_member_dashboard(user_id, only_upcoming)
        page = data.get('page', 1)
        if status_code < status.HTTP_400_BAD_REQUEST:
            bookings = result['bookings']
            paginated_bookings = paginate_data(bookings, page)
            result['bookings'] = paginated_bookings 
        response, status_code = handle_request_result(result, status_code)
        return JsonResponse(response, status=status_code)