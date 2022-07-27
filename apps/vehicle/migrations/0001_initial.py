

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [

        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(

            name='Type',
            fields=[
                ('type_title', models.TextField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=100, primary_key=True, serialize=False, unique=True)),
                ('type_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='type_childen', to='vehicle.type')),
            ],
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Наименование транспортного средства')),
                ('price', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='Цена')),
                ('year', models.PositiveIntegerField(verbose_name='Год выпуска')),
                ('mileage', models.PositiveIntegerField(verbose_name='Пробег')),
                ('volume', models.DecimalField(decimal_places=1, max_digits=3, verbose_name='объем двигателя')),
                ('fuel', models.CharField(choices=[('PETROL', 'бензин'), ('DIESEL', 'дизель'), ('ELECTRIC', 'электричество'), ('GAS', 'газ')], max_length=10, verbose_name='Вид топлива')),
                ('power', models.PositiveIntegerField(verbose_name='Мощность')),
                ('drive', models.CharField(choices=[('rear-wheel', 'задний привод'), ('front-wheel', 'передний привод'), ('all-wheel', 'полный привод')], max_length=20, verbose_name='Привод')),
                ('transmission', models.CharField(choices=[('manual', 'механическая'), ('automatic', 'автоматическая'), ('variable', 'вариативная/бесступенчатая')], max_length=20, verbose_name='КПП')),
                ('steering', models.CharField(choices=[('left', 'левый'), ('right', 'правый'), ('other', 'другое')], max_length=20, verbose_name='Руль')),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicles', to=settings.AUTH_USER_MODEL)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicles', to='vehicle.type', verbose_name='Тип кузова')),
            ],
            options={
                'verbose_name': 'Транспортное средство',
                'verbose_name_plural': 'Транстпортные средства',
                'db_table': 'vehicle',
            },
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='vehicles')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='vehicle.vehicle')),
            ],
        ),
    ]
