# models.py

from django.db import models
from .enums import UserType
from django.db.models import UniqueConstraint

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices(),
        default=UserType.MEMBER.value
    )

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

class Studio(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='owned_studios')

    def __str__(self):
        return self.name

class Class(models.Model):
    id = models.AutoField(primary_key=True)
    studio = models.ForeignKey(Studio, on_delete=models.CASCADE, related_name='classes')
    class_title = models.CharField(max_length=100)
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)
    slots_per_day = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.class_title} at {self.studio.name} ({self.start_date} to {self.end_date})"

class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='bookings')
    member = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='bookings')
    date = models.DateField()

    class Meta:
        constraints = [
            UniqueConstraint(fields=['class_instance', 'member', 'date'], name='unique_booking')
        ]

    def __str__(self):
        return f"{self.member.username} - {self.class_instance.class_title} on {self.date}"