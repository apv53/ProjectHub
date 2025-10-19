from django import forms
from .models import Project, Comments

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "description","cover_image", "demo_video", "project_file"]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']  # Only the comment text is entered by user
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Write your comment here...'
            }),
        }
        labels = {
            'comment': '',
        }