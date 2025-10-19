import os
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from .models import Project

# Delete files from disk when a Project is deleted
@receiver(post_delete, sender=Project)
def delete_project_files(sender, instance, **kwargs):
    if instance.cover_image and os.path.isfile(instance.cover_image.path):
        os.remove(instance.cover_image.path)
    if instance.demo_video and os.path.isfile(instance.demo_video.path):
        os.remove(instance.demo_video.path)
    if instance.project_file and os.path.isfile(instance.project_file.path):
        os.remove(instance.project_file.path)


# Optional: Delete old files when a Project file is updated
@receiver(pre_save, sender=Project)
def delete_old_project_files(sender, instance, **kwargs):
    if not instance.pk:
        return  # Skip if new instance
    
    try:
        old_instance = Project.objects.get(pk=instance.pk)
    except Project.DoesNotExist:
        return

    if old_instance.cover_image and old_instance.cover_image != instance.cover_image:
        if os.path.isfile(old_instance.cover_image.path):
            os.remove(old_instance.cover_image.path)
            
    # Demo video
    if old_instance.demo_video and old_instance.demo_video != instance.demo_video:
        if os.path.isfile(old_instance.demo_video.path):
            os.remove(old_instance.demo_video.path)
    
    # Project file
    if old_instance.project_file and old_instance.project_file != instance.project_file:
        if os.path.isfile(old_instance.project_file.path):
            os.remove(old_instance.project_file.path)
