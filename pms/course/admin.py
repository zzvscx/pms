from django.contrib import admin

# Register your models here.
from .models import Academy, Department, Grade, Course
@admin.register(Academy)
class AcademyAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin')
    search_fields = ('name', 'admin')
    raw_id_fields = ('admin',)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin', 'academy')
    search_fields = ('name', 'admin', 'academy')
    raw_id_fields = ('admin', 'academy')


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('name', 'department')
    search_fields = ('name', 'department')
    raw_id_fields = ('department',)


# @admin.register(Course)
# class CourseAdmin(admin.ModelAdmin):
#     list_display = ('name', 'total_points', 'rate')
#     search_fields = ('name',)
#     raw_id_fields = ('admin',)
