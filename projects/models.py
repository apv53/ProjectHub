from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=200)
    description = models.TextField()
    cover_image = models.FileField(upload_to="project_images/", blank=True, null=True)
    demo_video = models.FileField(upload_to="project_videos/", blank=True, null=True)
    project_file = models.FileField(upload_to="project_files/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

    @property
    def upvotes(self):
        return self.votes.filter(values=1).count()
    
    @property
    def downvotes(self):
        return self.votes.filter(values=-1).count()

class Votes(models.Model):
    vote_choices = (
        (1, "Upvote"),
        (-1, "Downvote"),
    )
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    values = models.IntegerField(choices=vote_choices)
    
    class Meta:
        unique_together = ("project", "user")
    
    def __str__(self):
        return f"{self.user.username} voted {self.get_value_display()} on {self.project.title}"

class Comments(models.Model):
    project = models.ForeignKey(Project, related_name="comments", on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comment by {self.user.username} on {self.project.title}"
