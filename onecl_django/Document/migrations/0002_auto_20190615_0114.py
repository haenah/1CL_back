# Generated by Django 2.2 on 2019-06-14 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Club', '0005_merge_20190614_2248'),
        ('Document', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='types', to='Club.Club')),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='documents', to='Document.DocumentType'),
        ),
    ]
