
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Student
from .forms import StudentForm


def hello(request):
    return HttpResponse("Hello, I am learning Django!")


@login_required
def dashboard(request):
    total_students = Student.objects.count()
    total_courses = (
        Student.objects.values("course").distinct().count()
    )
    total_cities = (
        Student.objects.values("city").distinct().count()
    )

    return render(
        request,
        "students/dashboard.html",
        {
            "total_students": total_students,
            "total_courses": total_courses,
            "total_cities": total_cities,
        }
    )


@login_required
def student_list(request):
    query = request.GET.get("q", "")
    student_data = Student.objects.all()
    total_students = Student.objects.count()

    if query:
        student_data = student_data.filter(name__icontains=query)

    paginator = Paginator(student_data, 2)
    page_number = request.GET.get("page")
    students = paginator.get_page(page_number)

    return render(
        request,
        "students/student_list.html",
        {
            "students": students,
            "query": query,
            "total_students": total_students,
        }
    )


@login_required
def add_student(request):
    if request.method == "POST":
        form = StudentForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Student added successfully!")
            return redirect("student_list")
    else:
        form = StudentForm()

    return render(
        request,
        "students/add_student.html",
        {"form": form}
    )


@login_required
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)

        if form.is_valid():
            form.save()
            messages.success(request, "Student updated successfully!")
            return redirect("student_list")
    else:
        form = StudentForm(instance=student)

    return render(
        request,
        "students/edit_student.html",
        {"form": form, "student": student}
    )


@login_required
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.delete()
        messages.success(request, "Student deleted successfully!")
        return redirect("student_list")

    return render(
        request,
        "students/delete_student.html",
        {"student": student}
    )
