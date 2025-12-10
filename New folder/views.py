from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.db.models import Sum, Count
from .models import Student, Comment, ClassTeacher, WeeklyLeader
from .forms import CommentForm # Hali yaratilmagan, keyin yaratamiz

# Bosh sahifa
def home_view(request):
    # Sinf Rahbari ismi
    try:
        class_teacher = ClassTeacher.objects.get()
        teacher_name = class_teacher.name
    except ClassTeacher.DoesNotExist:
        teacher_name = settings.CLASS_TEACHER_NAME # Default name
        
    # Haftalik Sinf Lideri
    weekly_leader = WeeklyLeader.objects.order_by('-start_date').first()
    
    # So'nggi 3 ta sharh
    latest_comments = Comment.objects.all().order_by('-created_at')[:3]
    
    # O'quvchilar ro'yxatiga link uchun Student modelini import qilish
    student_count = Student.objects.count()
    
    context = {
        'teacher_name': teacher_name,
        'weekly_leader': weekly_leader,
        'latest_comments': latest_comments,
        'student_count': student_count,
    }
    return render(request, 'main/home.html', context)

# O'quvchilar ro'yxati
def student_list_view(request):
    students = Student.objects.all().order_by('full_name')
    context = {
        'students': students,
    }
    return render(request, 'main/student_list.html', context)

# O'quvchi profili (biografiya sahifasi)
def student_detail_view(request, pk):
    student = get_object_or_404(Student, pk=pk)
    comments = student.comments.all()
    
    # CommentForm ni ishlatish uchun try-except bloki
    try:
        from .forms import CommentForm
    except ImportError:
        CommentForm = None # Agar forma hali yaratilmagan bo'lsa
        
    if CommentForm and request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.student = student
            comment.save()
            # Comment modelining save() metodi Student reytingini yangilaydi
            return redirect('student_detail', pk=student.pk)
    else:
        form = CommentForm() if CommentForm else None
        
    context = {
        'student': student,
        'comments': comments,
        'form': form,
    }
    return render(request, 'main/student_detail.html', context)

# Haftalik Lider sahifasi
def weekly_leader_view(request):
    leader = WeeklyLeader.objects.order_by('-start_date').first()
    
    context = {
        'leader': leader,
    }
    return render(request, 'main/weekly_leader.html', context)

# Haftalik liderni avtomatik aniqlash funksiyasi (cron job uchun)
def calculate_weekly_leader():
    # Barcha o'quvchilarning jami yulduzlarini hisoblash
    students_with_rating = Student.objects.annotate(
        total_stars_sum=Sum('total_stars')
    ).order_by('-total_stars_sum')
    
    if students_with_rating:
        top_student = students_with_rating.first()
        
        # Agar oldingi lider shu o'quvchi bo'lmasa, yangi yozuv yaratish
        latest_leader = WeeklyLeader.objects.order_by('-start_date').first()
        
        if not latest_leader or latest_leader.student != top_student:
            WeeklyLeader.objects.create(student=top_student)
            print(f"Yangi haftalik lider aniqlandi: {top_student.full_name}")
        else:
            print(f"Haftalik lider o'zgarmadi: {top_student.full_name}")
    else:
        print("O'quvchilar topilmadi, haftalik lider aniqlanmadi.")
