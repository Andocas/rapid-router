from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session


class UserProfile (models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='static/game/image/avatars/', null=True, blank=True,
                               default='/static/game/image/avatars/default-avatar.png')

class School (models.Model):
    name = models.CharField(max_length=200)

class Teacher (models.Model):
    name = models.CharField(max_length=200)
    user = models.OneToOneField(UserProfile)

class Class (models.Model):
    name = models.CharField(max_length=200)
    school = models.ForeignKey(School, related_name='class_school')
    teacher = models.ForeignKey(Teacher, related_name='class_teacher')

    def get_logged_in_students(self):
        """This gets all the students who are logged in."""
        sessions = Session.objects.filter(expire_date__gte=datetime.now())
        uid_list = []

        # Build a list of user ids from that query
        for session in sessions:
            data = session.get_decoded()
            uid_list.append(data.get('_auth_user_id', None))

        # Query all logged in users based on id list
        return Student.objects.filter(class_field=self).filter(user__id__in=uid_list)

class Student (models.Model):
    name = models.CharField(max_length=200)
    class_field = models.ForeignKey(Class, related_name='students')
    user = models.OneToOneField(UserProfile)

class Guardian (models.Model):
    name = models.CharField(max_length=200)
    children = models.ManyToManyField(Student)
    user = models.OneToOneField(UserProfile)

class Block (models.Model):
  type = models.CharField(max_length=200)

class Level (models.Model):
  name = models.IntegerField()
  path = models.CharField(max_length=300)
  blocks = models.ManyToManyField(Block, related_name='+')


class Attempt (models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    level = models.ForeignKey(Level, related_name='attempts')
    student = models.ForeignKey(Student, related_name='attempts')
    finish_time = models.DateTimeField(auto_now=True)
    score = models.FloatField()

class Command (models.Model):
    # TODO: deal with storing the complex commands.
    STEP_CHOICES = (
        ('Right', 'right'),
        ('Left', 'left'),
        ('Forward', 'forward'),
        ('TurnAround', 'turn around'),
        ('While', 'while'),
        ('If', 'if'),
    )

    CONDITON_CHOICES = (
        ('DeadEnd', 'dead end'),
        ('Destination', 'destination'),
        ('Forward', 'exists road forward'),
        ('Left', 'exists road left'),
        ('Right', 'exists road right'),
    )

    step = models.IntegerField()
    attempt = models.ForeignKey(Attempt, related_name='commands')
    command = models.CharField(max_length=15, choices=STEP_CHOICES, default='Forward')
    next = models.IntegerField()

    # Condition in While or If statements. Optional.
    condition = models.CharField(max_length=15, choices=CONDITON_CHOICES, blank=True)
    # 'While' or 'If' block. Optional.
    executedBlock1 = models.CommaSeparatedIntegerField(blank=True, max_length=100)
    # 'Else' block. Optional.
    executedBlock2 = models.CommaSeparatedIntegerField(blank=True, max_length=100)
    # Whether or not the 'not' block was used. Optional.
    condition_boolean = models.NullBooleanField(blank=True, null=True)
