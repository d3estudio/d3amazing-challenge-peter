from django.db import models
# to find the avg values based on receiver
from django.db.models import Avg, Count

# Create your models here.

class Base(models.Model):

    data_created=models.DateTimeField(auto_now_add=True)

    class Meta:

        abstract = True

class Role(Base):

    role = models.CharField(max_length=10)

    class Meta:

        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        ordering = ['id']


    def __str__(self):

        return self.role.title()


class Score(Base):

    sender = models.CharField(max_length=60)
    receiver = models.CharField(max_length=60)
    score_technical = models.DecimalField(max_digits=1, decimal_places=0)
    score_social = models.DecimalField(max_digits=1, decimal_places=0)
    scoresUser = models.ForeignKey('User', related_name='scoresUser', on_delete=models.CASCADE)

    class Meta:

        verbose_name = 'Score'
        verbose_name_plural = 'Scores'
        ordering = ['id']

    def __str__(self):

        return self.sender
class User(Base):

    slack_user_id = models.CharField(max_length=60)
    role = models.ForeignKey(Role, related_name='users', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    data_updated = models.DateTimeField(auto_now_add=True)
    avg_score_tech = models.ForeignKey(Score, related_name='avg_score_tech', null=True, on_delete=models.CASCADE)
    avg_score_social = models.ForeignKey(Score, related_name='avg_score_social', null=True, on_delete=models.CASCADE)

    # @property
    # def avg_score_tech(self):
    #     return selfaggregate(.score.Avg('score_technical'))


    # @property
    # def avg_score_social(self):
    #     return self.score.aggregate(Avg('score_social'))

    class Meta:

        verbose_name = 'User'
        verbose_name_plural = 'Users'
        unique_together = ['slack_user_id']
        ordering = ['id']

