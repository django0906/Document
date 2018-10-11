from django.db import models
from django.utils import timezone


__all__ = (
    'TwitterUser',
    'Relation',
)


class TwitterUser(models.Model):
    """
    특정 유저가 다른 유저를 (인스턴스 메서드)
        follow  (팔로우하기)
        block   (차단하기)

    중간모델이 저장하는 정보
        from_user
            어떤 유저가 '만든' 관계인지
        to_user
            관계의 '대상'이 되는 유저
        relation_type
            follow또는 block (팔로우 또는 차단)

    용어 정리
        자신을 follow하는 다른 사람목록
            followers (팔로워 목록)
        자신이 다른사람을 follow한 목록
            following (팔로우 목록)
        자신이 다른사람을 block한 목록
            block_list
        A가 B를 follow한 경우
            A는 B의 follower (팔로워)
            B는 A의 followee (팔로우)
    """
    name = models.CharField(max_length=50)
    relation_users = models.ManyToManyField(
        'self',
        through='Relation',
        symmetrical=False,
    )

    def __str__(self):
        return self.name

    @property
    def followers(self):
        """
        :return: 나를 follow하는 다른 TwitterUser QuerySet
        """
        return TwitterUser.objects.filter(
            from_user_relations__to_user=self,
            from_user_relations__relation_type='f',
        )

    @property
    def following(self):
        """
        :return: 내가 follow하는 다른 TwitterUser QuerySet
        """
        return TwitterUser.objects.filter(
            to_user_relations__from_user=self,
            to_user_relations__relation_type='f',
        )

    @property
    def block_list(self):
        """
        :return: 내가 block하는 다른 TwitterUser QuerySet
        """
        return TwitterUser.objects.filter(
            to_user_relations__from_user=self,
            to_user_relations__relation_type='b',
        )

    def follow(self, user):
        """
        user 를 follow 하는 Relation 을 생성
            1. 이미 존재한다면 만들지 않는다
            2. user 가 block_list 에 속한다면 만들지 않는다 (필요없음)
        :param user: TwitterUser
        :return: tuple(Relation instance, created(생성여부 True/False))
        """
        # 관계가 없다면 새 relations을 걸어줌
        created = False

        if not self.from_user_relations.filter(to_user=user).exists():
            self.from_user_relations.create(
                to_user=user,
                relation_type='f',
            )
            created = True

        return self.from_user_relations.get(to_user=user), created

    def block(self, user):
        """
        user 를 block 하는 Relation 을 생성
            1. 이미 존재한다면 만들지 않는다
            2. user 가 following 에 속한다면 해제시키고 만든다
        :param user: TwitterUser
        :return: tuple(Relation instance, created(생성여부 True/False))
        """

        try:
            # 기존의 관계를 먼저 읽어온다.
            relation = self.from_user_relations.get(to_user=user)
            if relation.relation_type == 'f':
                relation.relation_type = 'b'
                relation.created_at = timezone.now()
                relation.save()

        # 기존에 follow 가 안되어있으면?
        except Relation.DoesNotExist:
            relation = self.from_user_relations.create(
                to_user=user,
                relation_type='b'
            )

        else:
            return relation

    @property
    def follower_relations(self):
        """

        :return: 나를 follow하는 Relation QuerySet
        """
        return self.to_user_relations

    @property
    def followee_relations(self):
        """

        :return: 내가 follow하는 Relation QuerySet
        """
        return self.from_user_relations


class Relation(models.Model):
    CHOICES_RELATION_TYPE = (
        ('f', 'Follow'),
        ('b', 'Block'),
    )
    from_user = models.ForeignKey(
        TwitterUser,
        on_delete=models.CASCADE,
        related_name='from_user_relations',
        # related_query_name 의 기본값
        #  기본값:
        #    이 모델 클래스명의 소문자화
        #  related_name 이 지정되어 있을 경우:
        #    related_name 의 값
        related_query_name='from_user_relation',
    )
    to_user = models.ForeignKey(
        TwitterUser,
        on_delete=models.CASCADE,
        related_name='to_user_relations',
        related_query_name='to_user_relation',
    )
    relation_type = models.CharField(
        choices=CHOICES_RELATION_TYPE,
        max_length=1,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            ('from_user', 'to_user'),
        )