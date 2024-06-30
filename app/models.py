from django.db import models

class User(models.Model):
    userid = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.username

class Friend(models.Model):
    user = models.ForeignKey(User, related_name='user_friends', on_delete=models.CASCADE)
    friend = models.ForeignKey(User, related_name='friend_set', on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'friend'], name='unique_user_friend'),
            models.CheckConstraint(check=~models.Q(user=models.F('friend')), name='prevent_self_friendship')
        ]

    def __str__(self):
        return f'{self.user.username} is friends with {self.friend.username}'