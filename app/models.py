from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum, Count


# Create your models here.0

class QuestionManager(models.Manager):

    def all_user_questions(self, user_id):
        return self.filter(user__id=user_id).all()

    def likes_user_question(self, user_id):

        likes = Question.question_items.aggregate(Sum('count_like')).get('count_like__sum')
        dislikes = Question.question_items.aggregate(Sum('count_dislike')).get('count_dislike__sum')
        if likes and dislikes:
            return likes - dislikes
        elif likes and not dislikes:
            return likes
        elif not likes and dislikes:
            return -dislikes
        else:
            return 0

    def new(self):

        return self.order_by('-id').all()

    def best(self):

        return self.order_by('-count').all()

    def filter_by_tag(self, tag_name):

        return self.filter(tags__tag=tag_name).all()

    def single(self, q_id):

        return self.all().filter(id=q_id).all()


class LikeAnswerManager(models.Manager):
    def count_like(self, a_id):
        likes = self.filter(answer_id=a_id).filter(val__gt=0).aggregate(Sum('val')).get('val__sum')
        if likes:
            return likes
        return 0

    def count_dislike(self, a_id):
        dislikes = self.filter(answer_id=a_id).filter(val__lt=0).aggregate(Sum('val')).get('val__sum')
        if dislikes:
            return dislikes * (-1)
        return 0


class LikeQuestionManager(models.Manager):
    def count_like(self, q_id):
        likes = self.filter(question_id=q_id).filter(val__gt=0).aggregate(Sum('val')).get('val__sum')
        if likes:
            return likes
        return 0

    def count_dislike(self, q_id):
        dislikes = self.filter(question_id=q_id).filter(val__lt=0).aggregate(Sum('val')).get('val__sum')
        if dislikes:
            return dislikes * (-1)
        return 0


class TagManager(models.Manager):

    def popular_tags(self, num):
        return self.annotate(num_questions=Count('questions')).order_by('-num_questions')[:num]


class AnswerManager(models.Manager):

    def get_answers(self, q_id):

        answers = self.filter(question__id=q_id).all()
        return answers

    def answer_count(self, q_id):
        return self.select_related('question').filter(question__id=q_id).count()

    def all_user_answers(self, user_id):

        return self.filter(user__id=user_id).all()

    def likes_user_answers(self, user_id):
        answers_user = Answer.answer_items.all_user_answers(user_id)
        likes = answers_user.aggregate(Sum('likes')).get('likes__sum')
        dislikes = answers_user.aggregate(Sum('dislikes')).get('dislikes__sum')
        if likes and dislikes:
            return likes - dislikes
        elif likes and not dislikes:
            return likes
        elif not likes and dislikes:
            return -dislikes
        else:
            return 0


def best_users(num):
    dict = []
    users = User.objects.all()
    for user in users:
        result = Question.question_items.likes_user_question(user.id) + Answer.answer_items.likes_user_answers(user.id)
        user_item = {
            'id_user': user.id,
            'username': user.username,
            'likes': result
        }
        dict.append(user_item)
    dict.sort(key=lambda dictionary: dictionary['likes'])
    dict.reverse()
    return dict[:num]


class Question(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    tags = models.ManyToManyField('Tag', related_name='questions')
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    count_like = models.IntegerField(default=0)
    count_dislike = models.IntegerField(default=0)
    question_items = QuestionManager()
    count_answer = models.IntegerField(default=0)
    count = models.IntegerField(default=0)


class Answer(models.Model):
    question = models.ForeignKey('Question', models.PROTECT)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    is_correct = models.BooleanField()
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    answer_items = AnswerManager()


class Tag(models.Model):
    tag = models.CharField(max_length=32)
    tag_items = TagManager()

    def __str__(self):
        return f'{self.tag}'


class Profile(models.Model):
    avatar = models.ImageField(upload_to='../static/img/')
    user = models.OneToOneField(User, on_delete=models.PROTECT)


class LikeQuestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    question = models.ForeignKey('Question', on_delete=models.PROTECT)
    val = models.IntegerField(default=0)
    like_items = LikeQuestionManager()

    class Meta:
        unique_together = [['user', 'question']]


class LikeAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    answer = models.ForeignKey('Answer', on_delete=models.PROTECT)
    val = models.IntegerField(default=0)
    like_items = LikeAnswerManager()

    class Meta:
        unique_together = [['user', 'answer']]
