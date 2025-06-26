from django.db import models
from django.contrib.auth.models import User


class Equipment(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    details = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class ChecklistItem(models.Model):
    category = models.CharField(max_length=50)
    question = models.CharField(max_length=255)
    order = models.IntegerField()

    def __str__(self):
        return self.question


class CheckLog(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    item = models.ForeignKey(ChecklistItem, on_delete=models.CASCADE)
    inspector = models.ForeignKey(User, on_delete=models.CASCADE)
    checked_at = models.DateTimeField(auto_now_add=True)
    result = models.CharField(max_length=10, choices=[('양호', '양호'), ('불량', '불량'), ('해당없음', '해당없음')])
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.equipment.name} - {self.item.question} ({self.result})"