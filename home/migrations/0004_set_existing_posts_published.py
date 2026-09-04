# Data migration: set existing blog posts to published so they still appear on site

from django.db import migrations


def set_published(apps, schema_editor):
    BlogPost = apps.get_model('home', 'BlogPost')
    BlogPost.objects.all().update(status='published')


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_add_category_slug'),
    ]

    operations = [
        migrations.RunPython(set_published, noop),
    ]
