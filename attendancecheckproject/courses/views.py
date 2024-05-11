from urllib.parse import quote

from django.http import HttpResponse, FileResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from users.serializers import UserSerializer
from .models import Course, Group, Lesson, AttendanceType, Reference
from .serializers import CourseSerializer, GroupSerializer, LessonSerializer, ReferenceSerializer
from .models import LessonAttendance
from .serializers import LessonAttendanceSerializer,AttendancyTypeSer
from rest_framework.generics import ListAPIView


class CreateCourse(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateGroup(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateLesson(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            lesson = serializer.save()

            group_id = request.data.get('group')
            group_students = Group.objects.get(id=group_id).students.all()

            for student in group_students:
                LessonAttendance.objects.create(lesson=lesson, user=student)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetCourses(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)


class GetGroups(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)


class GetLessons(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        lessons = Lesson.objects.all()
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)


class GetUsersOfGroup(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        try:
            group = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            return Response({"error": "Group does not exist"}, status=status.HTTP_404_NOT_FOUND)

        users = group.students.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class LessonAttendanceList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, lesson_id):
        try:
            lesson_attendance = LessonAttendance.objects.filter(lesson_id=lesson_id)
        except LessonAttendance.DoesNotExist:
            return Response({"error": "Lesson attendance does not exist for this lesson"},
                            status=status.HTTP_404_NOT_FOUND)

        serializer = LessonAttendanceSerializer(lesson_attendance, many=True)
        return Response(serializer.data)

class AttendanceTypeList(ListAPIView):
    serializer_class = AttendancyTypeSer

    def get_queryset(self):
        return AttendanceType.objects.all()


class GetCoursesOfTeacher(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        teacher_courses = Course.objects.filter(teacher=request.user)
        serializer = CourseSerializer(teacher_courses, many=True)
        return Response(serializer.data)


class GetGroupsOfCourse(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        try:
            groups = Group.objects.filter(course_id=course_id)
        except Group.DoesNotExist:
            return Response({"error": "No groups found for this course"}, status=status.HTTP_404_NOT_FOUND)

        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)


class GetLessonOfGroup(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        try:
            lessons = Lesson.objects.filter(group=group_id)
        except Lesson.DoesNotExist:
            return Response({"error": "No lesson found for this group"}, status=status.HTTP_404_NOT_FOUND)

        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)


class GetLessonAttendanceInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, lesson_id):
        try:
            lesson_attendance = LessonAttendance.objects.filter(lesson_id=lesson_id)
        except LessonAttendance.DoesNotExist:
            return Response({"error": "No lesson attendance found for this lesson"}, status=status.HTTP_404_NOT_FOUND)

        serializer = LessonAttendanceSerializer(lesson_attendance, many=True)
        return Response(serializer.data)


class GetAttendanceOfLesson(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, lesson_id):
        try:
            attendance_records = LessonAttendance.objects.filter(lesson_id=lesson_id)
        except LessonAttendance.DoesNotExist:
            return Response({"error": "No attendance records found for this lesson"}, status=status.HTTP_404_NOT_FOUND)

        serializer = LessonAttendanceSerializer(attendance_records, many=True)
        return Response(serializer.data)


class ChangeAttendanceTypeToAttended(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, lesson_attendance_id):
        try:
            lesson_attendance = LessonAttendance.objects.get(id=lesson_attendance_id)
        except LessonAttendance.DoesNotExist:
            return Response({"error": "Lesson attendance does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_teacher:
            return Response({"error": "Only teachers can change attendance type"}, status=status.HTTP_403_FORBIDDEN)

        try:
            lesson_attendance = LessonAttendance.objects.get(id=lesson_attendance_id)
            lesson = Lesson.objects.get(id=lesson_attendance.lesson.id)
            group = Group.objects.get(id=lesson.group.id)
            course = Course.objects.get(id=group.course.id)
            if request.user != course.teacher:
                return Response({"error": "You are not the teacher of this course"}, status=status.HTTP_403_FORBIDDEN)
        except Course.DoesNotExist:
            return Response({"error": "No course found for this lesson"}, status=status.HTTP_404_NOT_FOUND)

        try:
            attended_type = AttendanceType.objects.get(pk=1)
        except AttendanceType.DoesNotExist:
            return Response({"error": "Attendance type 'Attended' does not exist"}, status=status.HTTP_404_NOT_FOUND)

        lesson_attendance.attendance_type = attended_type
        lesson_attendance.save()

        return Response({"message": "Attendance type updated to 'Attended'"}, status=status.HTTP_200_OK)


class ChangeAttendanceTypeToManual(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, lesson_attendance_id):
        try:
            lesson_attendance = LessonAttendance.objects.get(id=lesson_attendance_id)
        except LessonAttendance.DoesNotExist:
            return Response({"error": "Lesson attendance does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_teacher:
            return Response({"error": "Only teachers can change attendance type"}, status=status.HTTP_403_FORBIDDEN)

        try:
            lesson = lesson_attendance.lesson
            group = lesson.group
            course = group.course
            if request.user != course.teacher:
                return Response({"error": "You are not the teacher of this course"}, status=status.HTTP_403_FORBIDDEN)
        except (Lesson.DoesNotExist, Group.DoesNotExist, Course.DoesNotExist):
            return Response({"error": "No course found for this lesson"}, status=status.HTTP_404_NOT_FOUND)

        try:
            manual_type = AttendanceType.objects.get(pk=4)
        except AttendanceType.DoesNotExist:
            return Response({"error": "Attendance type 'Manual' does not exist"}, status=status.HTTP_404_NOT_FOUND)

        lesson_attendance.attendance_type = manual_type
        lesson_attendance.save()

        return Response({"message": "Attendance type updated to 'Manual'"}, status=status.HTTP_200_OK)


class ChangeAttendanceTypeToPermitted(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, lesson_attendance_id):
        try:
            lesson_attendance = LessonAttendance.objects.get(id=lesson_attendance_id)
        except LessonAttendance.DoesNotExist:
            return Response({"error": "Lesson attendance does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_teacher:
            return Response({"error": "Only teachers can change attendance type"}, status=status.HTTP_403_FORBIDDEN)

        try:
            lesson = lesson_attendance.lesson
            group = lesson.group
            course = group.course
            if request.user != course.teacher:
                return Response({"error": "You are not the teacher of this course"}, status=status.HTTP_403_FORBIDDEN)
        except (Lesson.DoesNotExist, Group.DoesNotExist, Course.DoesNotExist):
            return Response({"error": "No course found for this lesson"}, status=status.HTTP_404_NOT_FOUND)

        try:
            permitted_type = AttendanceType.objects.get(pk=3)
        except AttendanceType.DoesNotExist:
            return Response({"error": "Attendance type 'Permitted' does not exist"}, status=status.HTTP_404_NOT_FOUND)

        lesson_attendance.attendance_type = permitted_type
        lesson_attendance.save()

        return Response({"message": "Attendance type updated to 'Permitted'"}, status=status.HTTP_200_OK)


class ChangeAttendanceTypeToAbsent(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, lesson_attendance_id):
        try:
            lesson_attendance = LessonAttendance.objects.get(id=lesson_attendance_id)
        except LessonAttendance.DoesNotExist:
            return Response({"error": "Lesson attendance does not exist"}, status=status.HTTP_404_NOT_FOUND)

        if not request.user.is_teacher:
            return Response({"error": "Only teachers can change attendance type"}, status=status.HTTP_403_FORBIDDEN)

        try:
            lesson = lesson_attendance.lesson
            group = lesson.group
            course = group.course
            if request.user != course.teacher:
                return Response({"error": "You are not the teacher of this course"}, status=status.HTTP_403_FORBIDDEN)
        except (Lesson.DoesNotExist, Group.DoesNotExist, Course.DoesNotExist):
            return Response({"error": "No course found for this lesson"}, status=status.HTTP_404_NOT_FOUND)

        try:
            absent_type = AttendanceType.objects.get(pk=2)
        except AttendanceType.DoesNotExist:
            return Response({"error": "Attendance type 'Absent' does not exist"}, status=status.HTTP_404_NOT_FOUND)

        lesson_attendance.attendance_type = absent_type
        lesson_attendance.save()

        return Response({"message": "Attendance type updated to 'Absent'"}, status=status.HTTP_200_OK)


class GetMyLessonsWithAttendanceType(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        if request.user.is_teacher:
            return Response({"error": "Only student can see"}, status=status.HTTP_400_BAD_REQUEST)

        lessons = Lesson.objects.filter(group_id=group_id)

        lessons_with_attendance = []

        for lesson in lessons:
            try:
                attendance = LessonAttendance.objects.get(lesson=lesson, user=request.user)
                attendance_type = attendance.attendance_type.title
            except LessonAttendance.DoesNotExist:
                attendance_type = "Not Recorded"

            serialized_lesson = {
                'lesson_id': lesson.id,
                'lesson_date': lesson.lesson_date,
                'attendance_type': attendance_type
            }
            lessons_with_attendance.append(serialized_lesson)

        return Response(lessons_with_attendance, status=status.HTTP_200_OK)


class SendReferenceToLesson(APIView):
    def post(self, request, lesson_id):
        try:
            lesson_id = int(lesson_id)
        except ValueError:
            return Response({"error": "Invalid lesson ID"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            lesson = Lesson.objects.get(pk=lesson_id)
        except Lesson.DoesNotExist:
            return Response({"error": "Lesson not found"}, status=status.HTTP_404_NOT_FOUND)

        request.data['lesson'] = lesson_id
        request.data['student'] = request.user.id

        group = Group.objects.get(id=lesson.group.id)
        course = Course.objects.get(id=group.course.id)
        request.data['teacher'] = course.teacher.id

        serializer = ReferenceSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetMyReferencesToApproveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_teacher:
            return Response({"error": "Only teachers can access this endpoint"}, status=status.HTTP_403_FORBIDDEN)

        references = Reference.objects.filter(teacher=request.user)

        serializer = ReferenceSerializer(references, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ApproveReference(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, reference_id):
        try:
            reference = Reference.objects.get(id=reference_id)
        except Reference.DoesNotExist:
            return Response({"error": "Reference not found"}, status=status.HTTP_404_NOT_FOUND)

        lesson = reference.lesson
        student = reference.student

        if not request.user.is_teacher:
            return Response({"error": "Only teachers can approve references"}, status=status.HTTP_403_FORBIDDEN)
        if request.user != lesson.group.course.teacher:
            return Response({"error": "You are not the teacher of this lesson"}, status=status.HTTP_403_FORBIDDEN)

        try:
            attendance = LessonAttendance.objects.get(lesson=lesson, user=student)
        except LessonAttendance.DoesNotExist:
            return Response({"error": "Lesson attendance not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            approved_type = AttendanceType.objects.get(pk=3)
        except AttendanceType.DoesNotExist:
            return Response({"error": "Attendance type 'Approved' does not exist"}, status=status.HTTP_404_NOT_FOUND)

        attendance.attendance_type = approved_type
        attendance.save()

        reference.is_approved = True
        reference.is_done = True
        reference.save()

        return Response({"message": "Reference approved successfully"}, status=status.HTTP_200_OK)


class DownloadReferenceFileAPIView(APIView):
    def get(self, request, reference_id):
        try:
            reference = Reference.objects.get(id=reference_id)
        except Reference.DoesNotExist:
            return Response({"error": "Reference not found"}, status=status.HTTP_404_NOT_FOUND)

        if not reference.file:
            return Response({"error": "File not found for this reference"}, status=status.HTTP_404_NOT_FOUND)

        file_path = reference.file.path
        response = FileResponse(open(file_path, 'rb'), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{quote(reference.file.name.split("/")[-1])}"'
        return response
    

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Course
from .serializers import CourseSerializer
from rest_framework.decorators import api_view

@api_view(['GET'])
@csrf_exempt
def get_course_by_id(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        return JsonResponse({'error': 'Course not found'}, status=404)

    serializer = CourseSerializer(course)
    return JsonResponse(serializer.data)


from rest_framework import generics
from .models import Notification
from .serializers import NotificationSerializer

# View для получения списка уведомлений
class NotificationListView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

# View для создания нового уведомления
class NotificationCreateView(generics.CreateAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

# View для получения деталей конкретного уведомления
class NotificationDetailView(generics.RetrieveAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer