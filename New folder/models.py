from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

# 1. Sinf Rahbari (Class Teacher) modeli
class ClassTeacher(models.Model):
    """Sinf rahbari ismini saqlash uchun model."""
    name = models.CharField(max_length=100, verbose_name="Sinf Rahbari Ismi")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Sinf Rahbari"
        verbose_name_plural = "Sinf Rahbari"

# 2. O'quvchi (Student) modeli
class Student(models.Model):
    """O'quvchilar ro'yxati va profili uchun model."""
    full_name = models.CharField(max_length=150, verbose_name="To'liq Ismi")
    photo = models.ImageField(upload_to='students/', blank=True, null=True, verbose_name="Rasmi")
    biography = models.TextField(verbose_name="Biografiya")
    achievements = models.TextField(blank=True, verbose_name="Yutuqlar")
    
    # Reyting tizimi uchun
    total_stars = models.IntegerField(default=0, verbose_name="Jami Yulduzlar Soni")
    rating_count = models.IntegerField(default=0, verbose_name="Reytinglar Soni")

    @property
    def average_rating(self):
        """O'rtacha reytingni hisoblash."""
        if self.rating_count == 0:
            return 0
        # O'rtacha reytingni 1 o'nlik kasr aniqligida qaytarish
        return round(self.total_stars / self.rating_count, 1)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "O'quvchi"
        verbose_name_plural = "O'quvchilar"
        ordering = ['full_name']

# 3. Sharh (Comment) modeli
class Comment(models.Model):
    """O'quvchi profili uchun sharhlar va reytinglar modeli."""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='comments', verbose_name="O'quvchi")
    author_name = models.CharField(max_length=100, verbose_name="Sharh Qoldiruvchi Ismi")
    text = models.TextField(verbose_name="Sharh Matni")
    
    # 1 dan 5 gacha yulduzcha
    rating = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Bahosi (Yulduzcha)"
    )
    
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Yaratilgan Vaqti")

    def save(self, *args, **kwargs):
        # Agar yangi sharh bo'lsa (yoki rating o'zgargan bo'lsa, lekin bu yerda faqat yangi sharhni hisoblaymiz)
        is_new = self.pk is None
        
        super().save(*args, **kwargs)
        
        # O'quvchi reytingini yangilash
        student = self.student
        student.total_stars = sum(c.rating for c in student.comments.all())
        student.rating_count = student.comments.count()
        student.save()

    def __str__(self):
        return f"Sharh: {self.author_name} - {self.student.full_name}"

    class Meta:
        verbose_name = "Sharh"
        verbose_name_plural = "Sharhlar"
        ordering = ['-created_at']

# 4. Haftalik Lider (Weekly Leader) modeli
class WeeklyLeader(models.Model):
    """Haftalik liderni saqlash uchun model."""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Haftalik Lider")
    start_date = models.DateField(default=timezone.now, verbose_name="Boshlanish Sanasi")
    
    def __str__(self):
        return f"Haftalik Lider: {self.student.full_name} ({self.start_date})"

    class Meta:
        verbose_name = "Haftalik Lider"
        verbose_name_plural = "Haftalik Liderlar"
        get_latest_by = 'start_date'
