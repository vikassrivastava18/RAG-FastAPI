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


class TrueFalseQuiz(models.Model):
    subtopic = models.ForeignKey(SubTopic, on_delete=models.CASCADE)
    quiz = models.CharField(max_length=256)
    answer = models.BooleanField()

    def __str__(self) -> str:
        return self.quiz[:100]


class SelectOptionQuiz(models.Model):
    subtopic = models.ForeignKey(SubTopic, on_delete=models.CASCADE)
    quiz = models.CharField(max_length=256)
    options = models.JSONField(default=list, blank=True)
    anser = models.IntegerField()

    def __str__(self) -> str:
        return self.quiz[:100]


class FillBlankQuiz(models.Model):
    subtopic = models.ForeignKey(SubTopic, on_delete=models.CASCADE)
    quiz = models.CharField(max_length=256)
    answer = models.CharField(max_length=64)

    def __str__(self) -> str:
        return self.quiz[:100]
