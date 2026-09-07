from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=56)

    def __str__(self) -> str:
        return self.name


# class Topic
class Topic(models.Model):
    title = models.CharField(max_length=128)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    summary = models.TextField()

    def __str__(self) -> str:
        return (f"({self.course.name})-{self.summary}")[:50]


class SubTopic(models.Model):
     topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
     title = models.CharField(max_length=128)
     summary = models.TextField()
     quizzes = models.JSONField(null=True, blank=True)
     codes = models.JSONField(null=True, blank=True)

     def __str__(self) -> str:
        return (f"{self.title}")[:100]


class CodeSnippet(models.Model):
    sub_topic = models.ForeignKey(SubTopic, on_delete=models.CASCADE)
    is_example = models.BooleanField(default=True)
    question = models.TextField()
    snippet = models.TextField()
    expected_answer = models.CharField(max_length=256)

    def __str__(self) -> str:
        return (f"{self.question}")[:100]


