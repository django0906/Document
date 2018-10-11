# 1. AbstractBaseClass
#   자식 테이블만 존재
# 2. Multi-table inheritance
#   부모, 자식테이블이 모두 존재
# 3. Proxy Model
#   부모 테이블만 존재
from django.db import models


class CommonInfo(models.Model):
    # 순서를 미리 걸어놓는 Index를 생성
    name = models.CharField(max_length=100, db_index=True)
    age = models.PositiveIntegerField()

    class Meta:
        abstract = True
        ordering = ['name']


class Student(CommonInfo):
    home_group = models.CharField(max_length=5)

    # 상속의 상속이 이어질 때는 명시할 필요가 있다.
    class Meta(CommonInfo.Meta):
        # abstract = True
        verbose_name = '학생'
        verbose_name_plural = '학생 목록'
