from rest_framework import serializers
from .models import Course, Group, Lesson, Reference
from .models import LessonAttendance,AttendanceType,Notification


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class AttendancyTypeSer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceType
        fields = '__all__'

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class LessonAttendanceSerializer(serializers.ModelSerializer):
    user_full_name = serializers.SerializerMethodField()
    attendance_type_title = serializers.SerializerMethodField()

    class Meta:
        model = LessonAttendance
        fields = '__all__'

    def get_user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    def get_attendance_type_title(self, obj):
        return obj.attendance_type.title if obj.attendance_type else ""


class ReferenceSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=False)

    class Meta:
        model = Reference
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
