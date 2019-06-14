# Generated by Django 2.2 on 2019-06-12 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Club', '0002_auto_20190610_1613'),
        ('Image', '0002_remove_imagemodel_club'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagemodel',
            name='club',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='image_club', to='Club.Club'),
        ),
    ]
