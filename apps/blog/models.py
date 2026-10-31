from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from apps.language.models import Language


class BlogPost(models.Model):
    language = models.ForeignKey(
        Language,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='blog_posts',
        help_text="Select language for this blog post"
    )
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    short_description = models.CharField(max_length=500, blank=True, null=True)
    content = RichTextUploadingField(config_name='default')
    published_date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-published_date']
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def __str__(self):
        lang_str = f" [{self.language.code}]" if self.language else ""
        return f"{self.title}{lang_str}"

class SocialLink(models.Model):
    blog_post = models.ForeignKey(BlogPost, related_name='social_links', on_delete=models.CASCADE)
    platform_name = models.CharField(max_length=50)
    link = models.URLField()
    def __str__(self):
        return f"{self.platform_name} - {self.blog_post.title}"