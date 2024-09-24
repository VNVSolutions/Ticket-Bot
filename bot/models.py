from django.db import models


class Conditions(models.Model):
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.text}"

    class Meta:
        db_table = "conditions"


class UserProfile(models.Model):
    telegram_id = models.BigIntegerField(null=True)
    username = models.CharField(max_length=256, null=True)
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.username}, {self.telegram_id}"

    class Meta:
        db_table = "userprofile"


class ConditionsText(models.Model):
    text = models.TextField(blank=True, null=True)
    link = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.text}"

    class Meta:
        db_table = "conditions_text"