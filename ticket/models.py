from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Multi_User(models.Model):
    file_name = models.CharField(max_length = 100)

    def __str__(self):
        return "Multi_User(s) added!"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sid = models.IntegerField(default = 1234567, max_length = 7)

@receiver(post_save, sender=User)
def create_student(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(user=instance).save()

@receiver(post_save, sender=User)
def save_student(sender, instance, **kwargs):
    instance.student.save()

class Ticket_Request(models.Model):
    tickets_ordered = models.IntegerField(default = 0)
    extra_tickets = models.IntegerField(default = 0)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    studentID = models.IntegerField(unique=True)

#Create a string function for displaying models values
    def __str__(self):
        return f"Ticket_Ordered: {self.tickets_ordered}, First_Name: {self.first_name}, StudentID: {self.studentID} Last_Name: {self.last_name}, Extra_Tickets: {self.extra_tickets}"