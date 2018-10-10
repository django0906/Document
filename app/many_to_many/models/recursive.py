from django.db import models

__all__ = (
    'FacebookUser',
)


class FacebookUser(models.Model):
    name = models.CharField(max_length=50)
    friends = models.ManyToManyField(
        'self',
    )

    def __str__(self):
        # 이한영 (친구: a, b, c)
        #  QuerySet순회 및 문자열 포매팅
        friend_list = self.friends.all()
        friend_list_str = ', '.join([friend.name for friend in friend_list])
        return f'{self.name} (친구: {friend_list_str})'

        # return '{name} (친구: {friend_list})'.format(
        #     name=self.name,
        #     friend_list=', '.join(self.friends.values_list('name', flat=True))
        # )
