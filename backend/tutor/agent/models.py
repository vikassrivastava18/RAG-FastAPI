from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=56)

    def __str__(self) -> str:
        return self.name

# class Topic
class Topic(models.Model):
    title = models.CharField(max_length=128)
    course = models.ForeignKey(Course, on_delete=models.RESTRICT)
    summary = models.TextField()

    def __str__(self) -> str:
        return (f"({self.course.name})-{self.summary}")[:50]

class SubTopic(models.Model):
     topic = models.ForeignKey(Topic, on_delete=models.RESTRICT)
     title = models.CharField(max_length=128)
     summary = models.TextField()
     content = models.JSONField(null=True, blank=True)

     def __str__(self) -> str:
        return (f"{self.title}")[:100]
     


