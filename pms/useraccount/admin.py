#-*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from .models import User, Academy, Department, Grade, Course, UserScore
from django import forms
from django.contrib.auth.forms import UserChangeForm

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)
    

    class Meta:
        model = User
        fields = ('username', 'email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(UserChangeForm):
    username = forms.CharField(max_length=36)

    class Meta:
        model = User
        fields = '__all__'

    def clean_username(self):
        return self.cleaned_data.get('username')


@admin.register(User)
class UserAdmin(UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = [
        (None, {'fields': ('stuId', 'username', 'password', 'grade', 'intake')}),
        (u'权限', {'fields': ('is_active', 'is_staff', 'is_superuser',
                            'groups', 'user_permissions')}),
        (u'重要日期', {'fields': ('last_login', 'date_joined')}),
    ]

    list_display = ('stuId', 'username', 'grade',
                    'intake', 'is_active', 'is_staff')
    search_fields = ('grade', 'stuId', 'username')
    list_filter = ('is_staff', 'is_active')
    raw_id_fields = ('grade',)


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


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_points', 'rate')
    search_fields = ('name',)
    raw_id_fields = ('admin',)
