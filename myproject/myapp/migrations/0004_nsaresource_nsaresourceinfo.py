# Generated by Django 5.1.3 on 2024-11-13 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_information'),
    ]

    operations = [
        migrations.CreateModel(
            name='NsaResource',
            fields=[
                ('idx', models.BigAutoField(db_column='idx', primary_key=True, serialize=False)),
                ('id', models.CharField(db_column='id', max_length=255, null=True)),
                ('group', models.CharField(db_column='group', max_length=255, null=True)),
                ('name', models.CharField(db_column='name', max_length=255, null=True)),
                ('hostname', models.CharField(db_column='hostname', max_length=255, null=True)),
                ('ipaddress', models.CharField(db_column='ipaddress', max_length=255, null=True)),
                ('vendor', models.CharField(db_column='vendor', max_length=255, null=True)),
                ('model', models.CharField(db_column='model', max_length=255, null=True)),
                ('osversion', models.CharField(db_column='osversion', max_length=255, null=True)),
                ('crt_dtm', models.DateTimeField(auto_now_add=True, db_column='crt_dtm')),
                ('crt_uid', models.IntegerField(blank=True, db_column='crt_uid', null=True)),
                ('upd_dtm', models.DateTimeField(auto_now=True, db_column='upd_dtm', null=True)),
                ('upd_uid', models.IntegerField(blank=True, db_column='upd_uid', null=True)),
            ],
            options={
                'db_table': 't_nsa_resource',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='NsaResourceInfo',
            fields=[
                ('idx', models.BigAutoField(db_column='idx', primary_key=True, serialize=False)),
                ('port_id', models.CharField(db_column='port_id', max_length=255, null=True)),
                ('port_name', models.CharField(db_column='port_name', max_length=255, null=True)),
                ('description', models.TextField(db_column='description', null=True)),
                ('ok', models.CharField(db_column='ok', max_length=255, null=True)),
                ('oper_status', models.CharField(db_column='oper_status', max_length=255, null=True)),
                ('admin_status', models.CharField(db_column='admin_status', max_length=255, null=True)),
                ('mtu', models.CharField(db_column='mtu', max_length=255, null=True)),
                ('type', models.CharField(db_column='type', max_length=255, null=True)),
                ('speed', models.CharField(db_column='speed', max_length=255, null=True)),
                ('ipaddress', models.CharField(db_column='ipaddress', max_length=255, null=True)),
                ('system_name', models.TextField(db_column='system_name', null=True)),
                ('mac', models.CharField(db_column='mac', max_length=255, null=True)),
                ('lldp_alive', models.CharField(db_column='lldp_alive', max_length=255, null=True)),
                ('crt_dtm', models.DateTimeField(auto_now_add=True, db_column='crt_dtm')),
                ('crt_uid', models.IntegerField(blank=True, db_column='crt_uid', null=True)),
                ('upd_dtm', models.DateTimeField(auto_now=True, db_column='upd_dtm', null=True)),
                ('upd_uid', models.IntegerField(blank=True, db_column='upd_uid', null=True)),
            ],
            options={
                'db_table': 't_nsa_resource_info',
                'managed': False,
            },
        ),
    ]
