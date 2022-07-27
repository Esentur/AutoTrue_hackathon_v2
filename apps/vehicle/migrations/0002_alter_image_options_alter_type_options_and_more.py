# Generated by Django 4.0.6 on 2022-07-27 10:39
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vehicle', '0001_initial'),
    ]
    operations = [
        migrations.AlterModelOptions(
            name='image',
            options={'verbose_name': 'Изображение', 'verbose_name_plural': 'Изображения'},
        ),
        migrations.AlterModelOptions(
            name='type',
            options={'verbose_name': 'Тип транспорта', 'verbose_name_plural': 'Типы транспорта'},
        ),
        migrations.AlterModelOptions(
            name='vehicle',
            options={'ordering': ['title'], 'verbose_name': 'Транспортное средство', 'verbose_name_plural': 'Транстпортные средства'},
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='vehicles', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='image',
            name='vehicle',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='vehicle.vehicle', verbose_name='Транспорт'),
        ),
        migrations.AlterField(
            model_name='type',
            name='slug',
            field=models.SlugField(blank=True, max_length=100, primary_key=True, serialize=False, unique=True, verbose_name='Кузов'),
        ),
        migrations.AlterField(
            model_name='type',
            name='type_parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='type_childen', to='vehicle.type', verbose_name='Родительская категория'),
        ),
        migrations.AlterField(
            model_name='type',
            name='type_title',
            field=models.TextField(max_length=100, verbose_name='Тип кузова'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicles', to=settings.AUTH_USER_MODEL, verbose_name='Продавец'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=500, verbose_name='Текст')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='vehicle.vehicle', verbose_name='Транспорт')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'db_table': 'review',
            },
        ),
    ]