from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Notes'
        verbose_name_plural = 'Notes'
        
    
class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignment'
        
        
class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'todo'
        verbose_name_plural = 'todo'
    
        
    
    
        

