from django.db import models

# Create your models here.

class Base(models.Model):

    data_created=models.DateField(auto_now_add=True)

    class Meta:

        abstract = True

    def __str__(self):

        return self.slack_user_id

class Role(Base):

    role = models.CharField(max_length=10)

    class Meta:

        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        ordering = ['id']


    def __str__(self):

        return self.role.title()

class User(Base):

    slack_user_id = models.CharField(max_length=60)
    role = models.ForeignKey(Role, related_name='users', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    data_updated = models.DateTimeField(auto_now_add=True)

    class Meta:

        verbose_name = 'User'
        verbose_name_plural = 'Users'
        unique_together = ['slack_user_id']
        ordering = ['id']

class Score(Base):

    sender = models.CharField(max_length=60)
    receiver = models.CharField(max_length=60)
    score_technical = models.DecimalField(max_digits=1, decimal_places=0)
    score_social = models.DecimalField(max_digits=1, decimal_places=0)
    scoresUser = models.ForeignKey(User, related_name='scoresUser', on_delete=models.CASCADE)

    class Meta:

        verbose_name = 'Score'
        verbose_name_plural = 'Scores'
        ordering = ['id']

    def __str__(self):

        return self.sender