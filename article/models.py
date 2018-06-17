from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from unidecode import unidecode

from article.helper.helper import unique_slugify


def get_user_profile_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/profile/{1}'.format(instance.user.id, filename)


class BaseProfile(AbstractUser):
    """
    Extend the Base User model
    """
    mobile = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=100, blank=True)
    headshot = models.ImageField(upload_to=get_user_profile_path, blank=True, default='default_headshot.jpg')
    time_registered = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    """
    Identity that acting in the website.. And some others for research.
    """
    baseProfile = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    character = models.TextField(blank=True)


# Create 2 receivers to link the profile & the baseprofile together
@receiver(post_save, sender=BaseProfile)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(baseProfile=instance)


@receiver(post_save, sender=BaseProfile)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class ProfileFollowers(models.Model):
    """
    Store the following relationships
    """
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    follower = models.ForeignKey('Profile', on_delete=models.CASCADE, related_name='follower')


class Article(models.Model):
    """
    for main articles we created
    """

    def __str__(self):
        # For display
        return unidecode(self.title)

    class Meta:
        # Meta class.
        # descent order of articles' last modified time
        ordering = ['-last_modified_time']

    # Slug
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    # Author
    author = models.ForeignKey(BaseProfile, on_delete=models.CASCADE)

    # Titles & Body
    # TODO: How to display html? how to work with wangEditor format
    title = models.CharField('title', max_length=70)
    cover = models.ForeignKey('Images', on_delete=models.SET_NULL, null=True, blank=True)
    body = models.TextField('body')

    # Timestamps
    created_time = models.DateTimeField('time created', auto_now_add=True)
    last_modified_time = models.DateTimeField('time last modified', auto_now=True)

    # Either draft status or published.. and default to draft
    STATUS_CHOICES = (
        ('d', 'Draft'),
        ('o', 'Obsolete'),
        ('p', 'Published'),
    )
    status = models.CharField('status', max_length=1, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])

    # For display at main page
    abstract = models.CharField('abstract', max_length=100, blank=True, null=True,
                                help_text="Optional, default to first 100 characters")

    # Views
    views = models.IntegerField('views', default=0)

    # Likes
    likes = models.IntegerField('likes', default=0)

    # Topped status
    # topped = models.BooleanField('topped', default=False)
    shares = models.IntegerField('Shares', default=0)

    # Categories
    # Set null means if delete the articles, do not delete the categories
    category = models.ForeignKey('Category', verbose_name='category',
                                 null=True,
                                 on_delete=models.SET_NULL)

    def save(self, *args, **kwargs):
        # Slugify the images
        unique_slugify(self, unidecode(self.title))
        # Get abstract
        self.abstract = self.body[:100]
        super().save(*args, **kwargs)  # call Django's save()

    def clean(self):
        # Clean the format, some non-html code into html
        # Replace the &lt; and &gt;
        self.body = self.body.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'slug': self.slug})


class Category(models.Model):
    """
    Store Article Category information
    """
    name = models.CharField('name', max_length=50)
    created_time = models.DateTimeField('time created', auto_now_add=True)
    last_modified_time = models.DateTimeField('time last modified', auto_now=True)

    def __str__(self):
        return self.name


class Labels(models.Model):
    """
    Article Labels for future NLTK use
    """
    name = models.CharField('name', max_length=50)
    articles = models.ManyToManyField('Article')

    def __str__(self):
        return self.name


def get_user_image_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/images/{1}/{2}'.format(instance.profile.id, datetime.now().strftime('%Y/%m/%d'), filename)


class Images(models.Model):
    """
    For images related to the articles
    """
    image = models.ImageField(upload_to=get_user_image_path)
    profile = models.ForeignKey(BaseProfile, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=50, unique=True, allow_unicode=True)

    def __str__(self):
        return self.image.name

    def save(self, *args, **kwargs):
        # Slugify the images
        unique_slugify(self, unidecode(self.image.name))
        super().save(*args, **kwargs)  # call Django's save()

    def get_image_url(self):
        return self.image.url

    def get_absolute_url(self):
        return reverse('image', kwargs={'slug': self.slug})


class ArticleLiked(models.Model):
    """
    Store relation that user liked articles
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    profile = models.ForeignKey(BaseProfile, on_delete=models.CASCADE)


class ArticleStored(models.Model):
    """
    Store relation that user liked articles
    """
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)


class Stocks(models.Model):
    """
    Design for stocks?
    """
    pass


class StocksWatchers(models.Model):
    """
    Design for watching specific stocks
    """
    pass

