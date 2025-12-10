from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from .models import Student, Comment, ClassTeacher, WeeklyLeader

# 1. Sinf Rahbari (Class Teacher) Admin
class ClassTeacherAdmin(admin.ModelAdmin):
    list_display = ('name',)
    
    # Faqat bitta yozuv bo'lishini ta'minlash
    def has_add_permission(self, request):
        try:
            # Agar yozuv mavjud bo'lsa, qo'shishga ruxsat bermaymiz
            if ClassTeacher.objects.exists():
                return False
            return True
        except ObjectDoesNotExist:
            return True

    def has_delete_permission(self, request, obj=None):
        # O'chirishga ruxsat berish, lekin yangisini qo'shishga yo'q
        return True

admin.site.register(ClassTeacher, ClassTeacherAdmin)

# 2. O'quvchi (Student) Admin
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'average_rating', 'total_stars', 'rating_count')
    search_fields = ('full_name',)
    readonly_fields = ('total_stars', 'rating_count')
    
    # average_rating ni admin panelda ko'rsatish uchun
    def average_rating(self, obj):
        return obj.average_rating
    average_rating.short_description = "O'rtacha Reyting"

admin.site.register(Student, StudentAdmin)

# 3. Sharh (Comment) Admin
class CommentAdmin(admin.ModelAdmin):
    list_display = ('student', 'author_name', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('student__full_name', 'author_name', 'text')
    
    # Sharh o'chirilganda yoki qo'shilganda Student reytingini yangilash
    # Bu yerda reytingni yangilash uchun override qilamiz
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Agar yangi sharh bo'lsa yoki rating o'zgargan bo'lsa, Student reytingini yangilash
        # Lekin Comment modelining save() metodida bu ishni qilish yaxshiroq
        # Hozircha admin panelda o'zgartirishlar kiritilganda avtomatik yangilanishni ta'minlash uchun
        # Comment modelining save() metodini ishlatamiz.
        pass

    def delete_model(self, request, obj):
        # O'chirishdan oldin reytingni qayta hisoblash
        student = obj.student
        super().delete_model(request, obj)
        
        # O'quvchi reytingini qayta hisoblash
        student.total_stars = sum(c.rating for c in student.comments.all())
        student.rating_count = student.comments.count()
        student.save()

admin.site.register(Comment, CommentAdmin)

# 4. Haftalik Lider (Weekly Leader) Admin
class WeeklyLeaderAdmin(admin.ModelAdmin):
    list_display = ('student', 'start_date')
    list_filter = ('start_date',)
    
    # Haftalik liderni qo'lda o'zgartirish imkoniyati mavjud
    # Yangi yozuv qo'shish orqali liderni o'zgartirish mumkin
    
admin.site.register(WeeklyLeader, WeeklyLeaderAdmin)
