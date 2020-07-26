# Generated by Django 3.0.7 on 2020-07-26 08:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phone_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=100, unique=True)),
                ('DOB', models.DateField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('is_Doctor', models.BooleanField(default=False)),
                ('is_Patient', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('is_hospital_staff', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='uploads/%Y/%m/%d/')),
                ('contact_no', phone_field.models.PhoneField(blank=True, help_text='Contact phone number', max_length=31, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_of', models.CharField(max_length=50)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('doctor_id', models.AutoField(primary_key=True, serialize=False)),
                ('qualification', models.CharField(choices=[('MBBS', 'MBBS'), ('BDS', 'BDS'), ('BHMS', 'BHMS'), ('DHMS', 'DHMS'), ('BAMS', 'BAMS'), ('BUMS', 'BUMS'), ('BVSc & AH', 'BVSc & AH'), ('B.Pharm.', 'B.Pharm.'), ('D.Pharm.', 'D.Pharm.'), ('BOT', 'BOT'), ('BMLT', 'BMLT'), ('BPT', 'BPT'), ('B.Sc. Nursing', 'B.Sc. Nursing'), ('BNYS', 'BNYS')], default='MBBS', max_length=50)),
                ('postgrad', models.CharField(choices=[('None', 'None'), ('MD', 'MD'), ('MS', 'MS'), ('Diploma', 'Diploma')], default=None, max_length=50, null=True)),
                ('speciality', models.CharField(choices=[('None', 'None'), ('DM', 'DM'), ('MCh', 'MCh')], default=None, max_length=50, null=True)),
                ('daily_start_time', models.TimeField(blank=True, null=True)),
                ('daily_end_time', models.TimeField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('patient_id', models.AutoField(primary_key=True, serialize=False)),
                ('conditions', models.CharField(blank=True, max_length=200, null=True)),
                ('history', models.CharField(blank=True, max_length=200, null=True)),
                ('username', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('typeof', models.CharField(max_length=50)),
                ('published_on', models.DateField()),
                ('filelocation', models.FileField(upload_to='uploads/%Y/%m/%d/')),
                ('appointment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clinic_app.Appointment')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic_app.Patient')),
            ],
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filelocation', models.FileField(blank=True, null=True, upload_to='uploads/%Y/%m/%d/')),
                ('date', models.DateField()),
                ('price', models.IntegerField()),
                ('appointment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='clinic_app.Appointment')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic_app.Doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic_app.Patient')),
            ],
        ),
        migrations.CreateModel(
            name='DailyDoctorQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.IntegerField()),
                ('present', models.BooleanField(default=False)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic_app.Appointment')),
            ],
        ),
        migrations.AddField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doc', to='clinic_app.Doctor'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinic_app.Patient'),
        ),
    ]