from django.db import models

__all__ = (
    "RelatedUser",
    "PostBase",
    "PhotoPost",
    "TextPost",
)


class RelatedUser(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class PostBase(models.Model):
    '''
    Be careful with related_name and related_query_name 구문 읽기!
    https://lhy.kr/django-introduction-to-models
    '''
    author = models.ForeignKey(
        RelatedUser,
        on_delete=models.CASCADE,
        # Person 과 PostBase 를 이어주는 역할.
        # User(Person) 의 입장에서...
        # 자신이 특정 Post 의 Author 인 경우에 해당하는
        # 모든 PostBase 객체를 참조하는 역방향 매니저 이름
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class PhotoPost(PostBase):
    photo_url = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'Post: (Author: {self.author.name})'


class TextPost(PostBase):
    text = models.TextField(blank=True)

    def __str__(self):
        return f'Post: (Author: {self.author.name})'
