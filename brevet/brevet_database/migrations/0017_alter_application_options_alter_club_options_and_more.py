# Generated by Django 4.0 on 2022-11-04 11:27

import brevet_database.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_email_confirmed_delete_profile'),
        ('brevet_database', '0016_club_country'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='application',
            options={'verbose_name': 'Заявка', 'verbose_name_plural': 'Заявки'},
        ),
        migrations.AlterModelOptions(
            name='club',
            options={'verbose_name': 'Клуб', 'verbose_name_plural': 'Клубы'},
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'ordering': ['-date'], 'verbose_name': 'Бревет', 'verbose_name_plural': 'Бреветы'},
        ),
        migrations.AlterModelOptions(
            name='paymentinfo',
            options={'verbose_name': 'Платёжная информация', 'verbose_name_plural': 'Платёжная информация'},
        ),
        migrations.AlterModelOptions(
            name='randonneur',
            options={'ordering': ['russian_surname'], 'verbose_name': 'Рандоннёр', 'verbose_name_plural': 'Рандоннёры'},
        ),
        migrations.AlterModelOptions(
            name='result',
            options={'ordering': ['-event__date'], 'verbose_name': 'Результат', 'verbose_name_plural': 'Результаты'},
        ),
        migrations.AlterModelOptions(
            name='route',
            options={'ordering': ['-active', 'distance'], 'verbose_name': 'Мартшрут', 'verbose_name_plural': 'Маршруты'},
        ),
        migrations.AlterField(
            model_name='application',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Активна'),
        ),
        migrations.AlterField(
            model_name='application',
            name='date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата подачи'),
        ),
        migrations.AlterField(
            model_name='application',
            name='dnf',
            field=models.BooleanField(default=False, verbose_name='DNF'),
        ),
        migrations.AlterField(
            model_name='application',
            name='dns',
            field=models.BooleanField(default=False, verbose_name='DNS'),
        ),
        migrations.AlterField(
            model_name='application',
            name='dsq',
            field=models.BooleanField(default=False, verbose_name='DSQ'),
        ),
        migrations.AlterField(
            model_name='application',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brevet_database.event', verbose_name='Бревет'),
        ),
        migrations.AlterField(
            model_name='application',
            name='otl',
            field=models.BooleanField(default=False, verbose_name='OTL'),
        ),
        migrations.AlterField(
            model_name='application',
            name='payment',
            field=models.BooleanField(default=False, verbose_name='Оплачена'),
        ),
        migrations.AlterField(
            model_name='application',
            name='result',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='brevet_database.result', verbose_name='Результат'),
        ),
        migrations.AlterField(
            model_name='application',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user', verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='club',
            name='ACP_code',
            field=models.IntegerField(unique=True, verbose_name='Код АСР'),
        ),
        migrations.AlterField(
            model_name='club',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Город'),
        ),
        migrations.AlterField(
            model_name='club',
            name='country',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Страна'),
        ),
        migrations.AlterField(
            model_name='club',
            name='foreign',
            field=models.BooleanField(default=False, verbose_name='Иностранный'),
        ),
        migrations.AlterField(
            model_name='club',
            name='french_name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Название на французском'),
        ),
        migrations.AlterField(
            model_name='club',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='event',
            name='club',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='brevet_database.club', verbose_name='Клуб'),
        ),
        migrations.AlterField(
            model_name='event',
            name='date',
            field=models.DateField(verbose_name='Дата'),
        ),
        migrations.AlterField(
            model_name='event',
            name='external_xref',
            field=models.URLField(blank=True, verbose_name='Внешний ресурс'),
        ),
        migrations.AlterField(
            model_name='event',
            name='finished',
            field=models.BooleanField(default=False, verbose_name='Завершен'),
        ),
        migrations.AlterField(
            model_name='event',
            name='fleche_distance',
            field=models.IntegerField(blank=True, null=True, verbose_name='Факт. дистанция (Только для флеша, на англ.)'),
        ),
        migrations.AlterField(
            model_name='event',
            name='fleche_finish',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Факт. место финиша (Только для флеша, на англ.)'),
        ),
        migrations.AlterField(
            model_name='event',
            name='fleche_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Название (Только для флеша, на англ.)'),
        ),
        migrations.AlterField(
            model_name='event',
            name='fleche_start',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Место старта (Только для флеша, на англ.)'),
        ),
        migrations.AlterField(
            model_name='event',
            name='fleche_team',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Имя команды (Только для флеша, на англ.)'),
        ),
        migrations.AlterField(
            model_name='event',
            name='lights_required',
            field=models.BooleanField(default=False, verbose_name='Свет обязателен'),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(blank=True, max_length=50, verbose_name='Название (не обязательно)'),
        ),
        migrations.AlterField(
            model_name='event',
            name='omskvelo_xref',
            field=models.URLField(blank=True, verbose_name='Ссылка на форум'),
        ),
        migrations.AlterField(
            model_name='event',
            name='payment_info',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='brevet_database.paymentinfo', verbose_name='Информация об оплате'),
        ),
        migrations.AlterField(
            model_name='event',
            name='responsible',
            field=models.CharField(blank=True, max_length=50, verbose_name='Ответственный'),
        ),
        migrations.AlterField(
            model_name='event',
            name='route',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='brevet_database.route', verbose_name='Маршрут'),
        ),
        migrations.AlterField(
            model_name='event',
            name='text',
            field=models.TextField(blank=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='event',
            name='text_intro',
            field=models.TextField(blank=True, verbose_name='Введение'),
        ),
        migrations.AlterField(
            model_name='event',
            name='time',
            field=models.TimeField(default=datetime.time(7, 0), verbose_name='Время старта'),
        ),
        migrations.AlterField(
            model_name='event',
            name='vk_xref',
            field=models.URLField(blank=True, verbose_name='Ссылка вк'),
        ),
        migrations.AlterField(
            model_name='event',
            name='warning_text',
            field=models.TextField(blank=True, verbose_name='Предупреждение'),
        ),
        migrations.AlterField(
            model_name='randonneur',
            name='club',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='brevet_database.club', verbose_name='Клуб'),
        ),
        migrations.AlterField(
            model_name='randonneur',
            name='female',
            field=models.BooleanField(default=False, verbose_name='Женского пола'),
        ),
        migrations.AlterField(
            model_name='randonneur',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Имя (латиница)'),
        ),
        migrations.AlterField(
            model_name='randonneur',
            name='russian_name',
            field=models.CharField(max_length=50, verbose_name='Имя (кириллица)'),
        ),
        migrations.AlterField(
            model_name='randonneur',
            name='russian_surname',
            field=models.CharField(max_length=50, verbose_name='Фамилия (кириллица)'),
        ),
        migrations.AlterField(
            model_name='randonneur',
            name='sr',
            field=models.JSONField(blank=True, default=dict, null=True, verbose_name='Суперрандоннёр'),
        ),
        migrations.AlterField(
            model_name='randonneur',
            name='surname',
            field=models.CharField(max_length=50, verbose_name='Фамилия (латиница)'),
        ),
        migrations.AlterField(
            model_name='randonneur',
            name='total_brevets',
            field=models.IntegerField(default=0, verbose_name='Всего бреветов'),
        ),
        migrations.AlterField(
            model_name='randonneur',
            name='total_distance',
            field=models.IntegerField(default=0, verbose_name='Общая дистанция'),
        ),
        migrations.AlterField(
            model_name='result',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brevet_database.event', verbose_name='Бревет'),
        ),
        migrations.AlterField(
            model_name='result',
            name='homologation',
            field=models.CharField(blank=True, max_length=50, verbose_name='№ омологации'),
        ),
        migrations.AlterField(
            model_name='result',
            name='medal',
            field=models.BooleanField(default=False, verbose_name='Медаль'),
        ),
        migrations.AlterField(
            model_name='result',
            name='randonneur',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='brevet_database.randonneur', verbose_name='Рандоннёр'),
        ),
        migrations.AlterField(
            model_name='result',
            name='time',
            field=models.DurationField(blank=True, verbose_name='Время'),
        ),
        migrations.AlterField(
            model_name='route',
            name='active',
            field=models.BooleanField(default=False, verbose_name='Активный'),
        ),
        migrations.AlterField(
            model_name='route',
            name='bad_roads',
            field=models.BooleanField(default=False, verbose_name='Плохие дороги'),
        ),
        migrations.AlterField(
            model_name='route',
            name='brm',
            field=models.BooleanField(default=True, verbose_name='BRM'),
        ),
        migrations.AlterField(
            model_name='route',
            name='club',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.PROTECT, to='brevet_database.club', verbose_name='Клуб'),
        ),
        migrations.AlterField(
            model_name='route',
            name='controls',
            field=models.TextField(blank=True, verbose_name='КП'),
        ),
        migrations.AlterField(
            model_name='route',
            name='distance',
            field=models.IntegerField(verbose_name='Дистанция'),
        ),
        migrations.AlterField(
            model_name='route',
            name='external_xref',
            field=models.URLField(blank=True, verbose_name='Внешний ресурс'),
        ),
        migrations.AlterField(
            model_name='route',
            name='fleche',
            field=models.BooleanField(default=False, verbose_name='Flèche'),
        ),
        migrations.AlterField(
            model_name='route',
            name='gpx',
            field=models.FileField(blank=True, upload_to=brevet_database.models.gpx_path, verbose_name='*.gpx'),
        ),
        migrations.AlterField(
            model_name='route',
            name='image',
            field=models.ImageField(blank=True, upload_to=brevet_database.models.img_path, verbose_name='Картинка'),
        ),
        migrations.AlterField(
            model_name='route',
            name='lrm',
            field=models.BooleanField(default=False, verbose_name='LRM'),
        ),
        migrations.AlterField(
            model_name='route',
            name='map_embed_src',
            field=models.CharField(blank=True, max_length=500, verbose_name='Ссылка на карту'),
        ),
        migrations.AlterField(
            model_name='route',
            name='name',
            field=models.CharField(blank=True, max_length=200, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='route',
            name='orvm',
            field=models.FileField(blank=True, upload_to=brevet_database.models.pdf_path, verbose_name='Документ ОРВМ'),
        ),
        migrations.AlterField(
            model_name='route',
            name='pdf',
            field=models.FileField(blank=True, upload_to=brevet_database.models.pdf_path, verbose_name='*.pdf'),
        ),
        migrations.AlterField(
            model_name='route',
            name='sr600',
            field=models.BooleanField(default=False, verbose_name='SR600'),
        ),
        migrations.AlterField(
            model_name='route',
            name='text',
            field=models.TextField(blank=True, verbose_name='Описание полное'),
        ),
        migrations.AlterField(
            model_name='route',
            name='text_brief',
            field=models.TextField(blank=True, max_length=120, verbose_name='Описание краткое'),
        ),
    ]