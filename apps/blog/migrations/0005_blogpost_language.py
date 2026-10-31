import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_blogpost_image_alter_sociallink_blog_post'),
        ('language', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogpost',
            options={'ordering': ['-published_date'], 'verbose_name': 'Blog Post', 'verbose_name_plural': 'Blog Posts'},
        ),
        migrations.AddField(
            model_name='blogpost',
            name='language',
            field=models.ForeignKey(
                blank=True,
                help_text='Select language for this blog post',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='blog_posts',
                to='language.language'
            ),
        ),
    ]
