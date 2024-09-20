from rest_framework import serializers
from .models import Users, Studio, Class, Booking
from datetime import date
from .enums import UserType
from django.db import IntegrityError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'

class StudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Studio
        fields = '__all__'

    def validate(self, data):
        user = data.get('owner', None)
        if user and user.user_type != UserType.OWNER.value:
            raise serializers.ValidationError("only users registered as owners can create studio")
        
        if self.instance:
            if 'owner' in data and data['owner'] != self.instance.owner:
                raise serializers.ValidationError("Updating the owner associated with a studio is not allowed.")
            
        return data
    
class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = '__all__'

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        slots_per_day = data.get('slots_per_day')

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError("End date must be after start date.")

        if slots_per_day is not None and slots_per_day <= 0:
            raise serializers.ValidationError("Slots per day must be greater than zero.")

        if start_date and start_date <= date.today():
            raise serializers.ValidationError("Start date must be greater than today's date.")

        return data

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
    def validate(self, data):
        class_instance = data.get('class_instance')
        booking_date = data.get('date')

        if self.instance:
            if 'member' in data and data['member'] != self.instance.member:
                raise serializers.ValidationError("Updating the user associated with a booking is not allowed.")

        if booking_date and class_instance and (booking_date < class_instance.start_date or booking_date > class_instance.end_date):
            raise serializers.ValidationError("Booking date must be within the class date range.")
        
        return data
