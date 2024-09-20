from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from .models import Users, Studio, Class, Booking
from .serializers import UserSerializer, StudioSerializer, ClassSerializer, BookingSerializer
from django.utils import timezone
from django.db.models import Count
from datetime import date
from .utils import date_range


class UserService:
    @staticmethod
    def get_user(user_id=None):
        try:
            if user_id:
                user = Users.objects.get(id=user_id)
                serializer = UserSerializer(user)
            else:
                users = Users.objects.all()
                serializer = UserSerializer(users, many=True)
            return serializer.data, status.HTTP_200_OK
        except ObjectDoesNotExist:
            return "User not found",  status.HTTP_404_NOT_FOUND
        except Exception as e:
            return str(e),  status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def create_user(data):
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            try:
                user = Users.objects.create(**serializer.validated_data)
                user_data = UserSerializer(user).data
                return user_data, status.HTTP_201_CREATED
            except Exception as e:
                return  e, status.HTTP_400_BAD_REQUEST
        return serializer.errors, status.HTTP_400_BAD_REQUEST

    @staticmethod
    def update_user(data, partial=False):
        try:
            user_id = data.pop('user_id', None)
            user = Users.objects.get(id=user_id)
            serializer = UserSerializer(data=data, partial=partial)
            if serializer.is_valid():
                for attr, value in serializer.validated_data.items():
                    setattr(user, attr, value)
                user.save()
                user_data = UserSerializer(user).data
                return user_data, status.HTTP_200_OK
            return serializer.errors, status.HTTP_400_BAD_REQUEST
        except ObjectDoesNotExist:
            return "User not found", status.HTTP_404_NOT_FOUND
        except Exception as e:
            return e, status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def delete_user(user_id):
        try:
            user = Users.objects.get(id=user_id)
            user.delete()
            return "User deleted", status.HTTP_204_NO_CONTENT
        except ObjectDoesNotExist:
            return "User not found", status.HTTP_404_NOT_FOUND
        except Exception as e:
            return e, status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def get_member_dashboard(user_id, only_upcoming=0):
        try:
            user = Users.objects.get(id=user_id)
            bookings = Booking.objects.filter(member=user)
            if only_upcoming:
                bookings = bookings.filter(date__gte=timezone.now())
            bookings_data = BookingSerializer(bookings, many=True).data
            bookings_count = len(bookings_data)

            data = {
                "bookings_count": bookings_count,
                "bookings": bookings_data
            }

            return data, status.HTTP_200_OK
        except ObjectDoesNotExist:
            return "User not found", status.HTTP_404_NOT_FOUND
        except Exception as e:
            return e, status.HTTP_500_INTERNAL_SERVER_ERROR

class StudioService:
    @staticmethod
    def get_studio(studio_id=None):
        try:
            if studio_id:
                studio = Studio.objects.get(id=studio_id)
                serializer = StudioSerializer(studio)
            else:
                studios = Studio.objects.all()
                serializer = StudioSerializer(studios, many=True)
            return serializer.data, status.HTTP_201_CREATED
        except ObjectDoesNotExist:
            return "Studio not found", status.HTTP_404_NOT_FOUND
        except Exception as e:
            return e, status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def create_studio(data):
        try:
            serializer = StudioSerializer(data=data)
            if serializer.is_valid():
                try:
                    studio = Studio.objects.create(**serializer.validated_data)
                    studio_data = StudioSerializer(studio).data
                    return studio_data, status.HTTP_201_CREATED
                except Exception as e:
                    return  e, status.HTTP_400_BAD_REQUEST
            return serializer.errors, status.HTTP_400_BAD_REQUEST
        except ObjectDoesNotExist:
            return "Studio not found", status.HTTP_404_NOT_FOUND
        except Exception as e:
            return e, status.HTTP_500_INTERNAL_SERVER_ERROR


    @staticmethod
    def update_studio(studio_id, data, partial=False):
        try:
            studio = Studio.objects.get(id=studio_id)
            serializer = StudioSerializer(studio, data=data, partial=partial)
            if serializer.is_valid():
                for attr, value in serializer.validated_data.items():
                    setattr(studio, attr, value)
                studio.save()
                return StudioSerializer(studio).data, status.HTTP_200_OK
            return serializer.errors, status.HTTP_400_BAD_REQUEST
        except ObjectDoesNotExist:
            return "Studio not found", status.HTTP_404_NOT_FOUND
        except Exception as e:
            return e, status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def delete_studio(studio_id):
        try:
            studio = Studio.objects.get(id=studio_id)
            studio.delete()
            return None, status.HTTP_204_NO_CONTENT
        except ObjectDoesNotExist:
            return "Studio not found", status.HTTP_404_NOT_FOUND
        except Exception as e:
            return e, status.HTTP_500_INTERNAL_SERVER_ERROR

class ClassService:
    @staticmethod
    def get_class(data):
        try:
            class_id = data.get('class_id', None)
            studio_id = data.get('studio_id', None)
            if class_id:
                class_obj = Class.objects.get(id=class_id)
                serializer = ClassSerializer(class_obj)
            elif studio_id:
                classes = Class.objects.filter(studio_id=studio_id)
                serializer = ClassSerializer(classes, many=True)
            else:
                classes = Class.objects.all()
                serializer = ClassSerializer(classes, many=True)
            return serializer.data, status.HTTP_200_OK
        except ObjectDoesNotExist:
            return "Class not found", status.HTTP_404_NOT_FOUND
        except Exception as e:
            return e, status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def create_class(data):
        try:
            studio_id = data.get('studio', None)
            studio = Studio.objects.get(id=studio_id)
            if studio:
                serializer = ClassSerializer(data=data)
                if serializer.is_valid():
                    class_obj = Class.objects.create(**serializer.validated_data)
                    class_data = ClassSerializer(class_obj).data
                    return class_data, status.HTTP_201_CREATED
                return serializer.errors, status.HTTP_400_BAD_REQUEST
        except ObjectDoesNotExist:
            return "Studio not found", status.HTTP_404_NOT_FOUND
        except Exception as e:
            return e, status.HTTP_400_BAD_REQUEST

    @staticmethod
    def update_class(data, partial=False):
        try:
            class_id = data.pop('class_id', None)
            class_obj = Class.objects.get(id=class_id)

            max_bookings = class_obj.bookings.values('date').annotate(
                booking_count=Count('id')
            ).order_by('-booking_count').first()
            max_bookings_count = max_bookings['booking_count'] if max_bookings else 0
            if 'slots_per_day' in data and data['slots_per_day'] < max_bookings_count:
                return f"Cannot reduce slots_per_day below {max_bookings_count}", status.HTTP_400_BAD_REQUEST
            
            serializer = ClassSerializer(data=data, partial=partial)
            if serializer.is_valid():
                for attr, value in serializer.validated_data.items():
                    setattr(class_obj, attr, value)
                class_obj.save()
                return ClassSerializer(class_obj).data, status.HTTP_200_OK
            return serializer.errors, status.HTTP_400_BAD_REQUEST
        except ObjectDoesNotExist:
            return "Class not found", status.HTTP_404_NOT_FOUND
        except Exception as e:
            return e, status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def delete_class(class_id):
        try:
            class_obj = Class.objects.get(id=class_id)
            class_obj.delete()
            return None, status.HTTP_204_NO_CONTENT
        except ObjectDoesNotExist:
            return "Class not found", status.HTTP_404_NOT_FOUND
        except Exception as e:
            return e, status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def get_class_availability(class_id):
        try:
            class_obj = Class.objects.get(id=class_id)
            total_slots = class_obj.slots_per_day

            # Determine the start date as the later of the class's start date or today
            start_date = max(class_obj.start_date, date.today())
            end_date = class_obj.end_date

            # Calculate availability for each date from the calculated start date to the end date
            availability = []
            for single_date in date_range(start_date, end_date):
                booked_slots = Booking.objects.filter(class_instance=class_obj, date=single_date).count()
                available_slots = total_slots - booked_slots
                availability.append({
                    "date": single_date,
                    "total_slots": total_slots,
                    "booked_slots": booked_slots,
                    "available_slots": available_slots
                })

            data = {
                "class_title": class_obj.class_title,
                "availability": availability
            }

            return data, status.HTTP_200_OK

        except ObjectDoesNotExist:
            return {"error": "Class not found"}, status.HTTP_404_NOT_FOUND
        except Exception as e:
            return {"error": str(e)}, status.HTTP_500_INTERNAL_SERVER_ERROR

class BookingService:
    @staticmethod
    def get_bookings(data):
        try:
            studio_id = data.get('studio_id', None)
            class_id = data.get('class_id', None)
            booking_id = data.get('booking_id', None)

            if booking_id:
                bookings = Booking.objects.filter(id=booking_id)
            elif class_id:
                bookings = Booking.objects.filter(class_instance__id=class_id)
            elif studio_id:
                bookings = Booking.objects.filter(class_instance__studio_id=studio_id)
            else:
                 bookings = Booking.objects.all()

            if bookings.count() ==0:
                return "No booking found", status.HTTP_200_OK
            serializer = BookingSerializer(bookings, many=True)
            return serializer.data, status.HTTP_200_OK
        except Exception as e:
            return str(e), status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def create_booking(data):
        try:
            class_instance = Class.objects.get(id=data.get('class_instance'))
            member = Users.objects.get(id=data.get('member'))
            booking = Booking.objects.filter(class_instance=class_instance, date=data.get('date'), member=member)
            if booking.count():
                return "A booking with the same date, class instance, and member already exists.", status.HTTP_404_NOT_FOUND
            serializer = BookingSerializer(data=data)
            if serializer.is_valid():
                booking = Booking.objects.create( **serializer.validated_data)
                booking_data = BookingSerializer(booking).data
                return booking_data, status.HTTP_201_CREATED
            return serializer.errors, status.HTTP_400_BAD_REQUEST
        except Users.DoesNotExist:
            return "User not found", status.HTTP_404_NOT_FOUND
        except Class.DoesNotExist:
            return "Class not found", status.HTTP_404_NOT_FOUND
        except Exception as e:
            return e, status.HTTP_400_BAD_REQUEST

    @staticmethod
    def update_booking(booking_id, data, partial=False):
        try:
            booking = Booking.objects.get(id=booking_id)
            old_class = booking.class_instance
            old_date = booking.date

            serializer = BookingSerializer(booking, data=data, partial=partial)
            if serializer.is_valid():
                new_class = serializer.validated_data.get('class_instance', old_class)
                new_date = serializer.validated_data.get('date', old_date)

                if new_class != old_class or new_date != old_date:
                    availability, _ = BookingService.check_booking_availability(new_class.id, new_date)
                    if availability['available_slots'] <= 0:
                        return f"No available slots for the class on {new_date}", status.HTTP_400_BAD_REQUEST

                updated_booking = serializer.save()
                return BookingSerializer(updated_booking).data, status.HTTP_200_OK
            return serializer.errors, status.HTTP_400_BAD_REQUEST
        except ObjectDoesNotExist:
            return "Booking not found", status.HTTP_404_NOT_FOUND
        except Exception as e:
            return str(e), status.HTTP_500_INTERNAL_SERVER_ERROR


    @staticmethod
    def delete_booking(booking_id):
        try:
            booking = Booking.objects.get(id=booking_id)
            booking.delete()
            return None, status.HTTP_204_NO_CONTENT
        except ObjectDoesNotExist:
            return "Booking not found", status.HTTP_404_NOT_FOUND
        except Exception as e:
            return e, status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def check_booking_availability(class_id, date):
        try:
            class_obj = Class.objects.get(id=class_id)
            total_slots = class_obj.slots_per_day
            booked_slots = Booking.objects.filter(class_instance=class_obj, date=date).count()
            available_slots = total_slots - booked_slots
            data = {
                "class_id": class_id,
                "date": date,
                "total_slots": total_slots,
                "booked_slots": booked_slots,
                "available_slots": available_slots
            }
            return data, status.HTTP_200_OK
        except ObjectDoesNotExist:
            return "Class not found", status.HTTP_404_NOT_FOUND
        except Exception as e:
            return e, status.HTTP_500_INTERNAL_SERVER_ERROR