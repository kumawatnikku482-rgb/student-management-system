

from django import forms
from .models import Student


class StudentForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['name', 'city', 'course']

        error_messages = {
            'name': {
                'required': 'Name cannot be empty.',
            },
            'city': {
                'required': 'City cannot be empty.',
            },
            'course': {
                'required': 'Course cannot be empty.',
            },
        }

    def clean_name(self):
        name = self.cleaned_data.get('name', '')

        if not name.strip():
            raise forms.ValidationError("Name cannot be empty.")

        return name.strip()

    def clean_city(self):
        city = self.cleaned_data.get('city', '')

        if not city.strip():
            raise forms.ValidationError("City cannot be empty.")

        return city.strip()

    def clean_course(self):
        course = self.cleaned_data.get('course', '')

        if not course.strip():
            raise forms.ValidationError("Course cannot be empty.")

        return course.strip()
