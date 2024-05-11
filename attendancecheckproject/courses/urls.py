from django.urls import path
from .views import CreateCourse, CreateGroup, CreateLesson, GetCourses, GetGroups, GetLessons, GetUsersOfGroup, \
    LessonAttendanceList, GetCoursesOfTeacher, GetGroupsOfCourse, GetLessonOfGroup, GetLessonAttendanceInfo, \
    GetAttendanceOfLesson, ChangeAttendanceTypeToAttended, ChangeAttendanceTypeToManual, \
    ChangeAttendanceTypeToPermitted, ChangeAttendanceTypeToAbsent, GetMyLessonsWithAttendanceType, \
    SendReferenceToLesson, GetMyReferencesToApproveAPIView, ApproveReference, DownloadReferenceFileAPIView,get_course_by_id,AttendanceTypeList,NotificationListView,NotificationCreateView,NotificationDetailView

urlpatterns = [
    path('create/course/', CreateCourse.as_view(), name='create_course'),
    path('create/group/', CreateGroup.as_view(), name='create_group'),
    path('get/courses/', GetCourses.as_view(), name='get_courses'),
    path('get/courses/<str:course_id>/', get_course_by_id, name='get_course_by_id'),
    path('get/groups/', GetGroups.as_view(), name='get_groups'),
    # path('get/lessons/', GetLessons.as_view(), name='get_lessons'),
    path('get/group/users/<int:group_id>/', GetUsersOfGroup.as_view(), name='get_users_of_group'),
    path('get/lesson/attendance/<int:lesson_id>/', LessonAttendanceList.as_view(), name='lesson_attendance_list'),
    path('get/attendancytype/', AttendanceTypeList.as_view()),

    # для получения курсов тичера
    path('get/teacher/courses/', GetCoursesOfTeacher.as_view(), name='get_teacher_courses'),
    path('get/course/groups/<int:course_id>/', GetGroupsOfCourse.as_view(), name='get_groups_of_course'),
    path('get/group/lesson/<int:group_id>/', GetLessonOfGroup.as_view(), name='get_lesson_of_group'),

    path('create/lesson/', CreateLesson.as_view(), name='create_lesson'),

    path('get/lesson/attendance/<int:lesson_id>/', GetLessonAttendanceInfo.as_view(),
         name='get_lesson_attendance_info'),

    path('get/lesson/attendance/<int:lesson_id>/', GetAttendanceOfLesson.as_view(), name='get_attendance_of_lesson'),

    # изменение статусов
    path('change/attendance/<int:lesson_attendance_id>/to_attended/', ChangeAttendanceTypeToAttended.as_view(),
         name='change_attendance_to_attended'),
    path('change/attendance/<int:lesson_attendance_id>/to_manual/', ChangeAttendanceTypeToManual.as_view(),
         name='change_attendance_to_manual'),
    path('change/attendance/<int:lesson_attendance_id>/to_permitted/', ChangeAttendanceTypeToPermitted.as_view(),
         name='change_attendance_to_permitted'),
    path('change/attendance/<int:lesson_attendance_id>/to_absent/', ChangeAttendanceTypeToAbsent.as_view(),
         name='change_attendance_to_absent'),

    path('get/my_lessons/<int:group_id>/', GetMyLessonsWithAttendanceType.as_view(),
         name='get_my_lessons_with_attendance_type'),

    path('send_reference_to_lesson/<int:lesson_id>/', SendReferenceToLesson.as_view(), name='send_reference_to_lesson'),

    path('my_references_to_approve/', GetMyReferencesToApproveAPIView.as_view(), name='my_references_to_approve'),

    path('approve_reference/<int:reference_id>/', ApproveReference.as_view(), name='approve_reference'),

    path('download_reference_file/<int:reference_id>/', DownloadReferenceFileAPIView.as_view(),
         name='download_reference_file'),

     path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/create/', NotificationCreateView.as_view(), name='notification-create'),
    path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification-detail'),


]
