# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Device', fields ['site', 'name', 'building', 'floor', 'room']
        db.delete_unique(u'core_device', ['site_id', 'name', 'building', 'floor', 'room'])

        # Removing unique constraint on 'PresenceSensor', fields ['device', 'metric']
        #db.delete_unique(u'core_presencesensor', ['device_id', 'metric_id'])

        # Removing unique constraint on 'ScalarSensor', fields ['device', 'metric']
        db.delete_unique(u'core_scalarsensor', ['device_id', 'metric_id'])

        # Deleting model 'Person'
        db.delete_table(u'core_person')

        # Deleting model 'ScalarData'
        db.delete_table(u'core_scalardata')

        # Removing index on 'ScalarData', fields ['sensor', 'timestamp']
        #db.delete_index(u'core_scalardata', ['sensor_id', 'timestamp'])

        # Deleting model 'StatusUpdate'
        db.delete_table(u'core_statusupdate')

        # Deleting model 'Site'
        db.delete_table(u'core_site')

        # Deleting model 'PresenceData'
        db.delete_table(u'core_presencedata')

        # Deleting model 'ScalarSensor'
        db.delete_table(u'core_scalarsensor')

        # Deleting model 'PresenceSensor'
        db.delete_table(u'core_presencesensor')

        # Adding model 'Contact'
        db.create_table(u'core_contact', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('last_name', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='contacts', null=True, to=orm['core.Organization'])),
        ))
        db.send_create_signal(u'core', ['Contact'])

        # Adding M2M table for field deployments on 'Contact'
        m2m_table_name = db.shorten_name(u'core_contact_deployments')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contact', models.ForeignKey(orm[u'core.contact'], null=False)),
            ('deployment', models.ForeignKey(orm[u'core.deployment'], null=False))
        ))
        db.create_unique(m2m_table_name, ['contact_id', 'deployment_id'])

        # Adding M2M table for field sites on 'Contact'
        m2m_table_name = db.shorten_name(u'core_contact_sites')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contact', models.ForeignKey(orm[u'core.contact'], null=False)),
            ('fixedsite', models.ForeignKey(orm[u'core.fixedsite'], null=False))
        ))
        db.create_unique(m2m_table_name, ['contact_id', 'fixedsite_id'])

        # Adding M2M table for field devices on 'Contact'
        m2m_table_name = db.shorten_name(u'core_contact_devices')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contact', models.ForeignKey(orm[u'core.contact'], null=False)),
            ('device', models.ForeignKey(orm[u'core.device'], null=False))
        ))
        db.create_unique(m2m_table_name, ['contact_id', 'device_id'])

        # Adding model 'SensorType'
        db.create_table(u'core_sensortype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('manufacturer', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('model', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('datasheet_url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('retail_cost', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('learn_priority', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('service_interval_days', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('sensor_topology', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['SensorType'])

        # Adding model 'Deployment'
        db.create_table(u'core_deployment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(related_name='deployments', to=orm['core.Organization'])),
            ('geo_location', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.GeoLocation'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Deployment'])

        # Adding model 'Organization'
        db.create_table(u'core_organization', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('url', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('raw_zmq_stream', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
        ))
        db.send_create_signal(u'core', ['Organization'])

        # Adding model 'APIType'
        db.create_table(u'core_apitype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('api_name', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('api_base_address', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['APIType'])

        # Adding model 'SensorData'
        db.create_table(u'core_sensordata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sensor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sensor_data', to=orm['core.Sensor'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, db_index=True, blank=True)),
            ('duration_sec', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'core', ['SensorData'])

        # Adding index on 'SensorData', fields ['sensor', 'timestamp']
        db.create_index(u'core_sensordata', ['sensor_id', 'timestamp'])

        # Adding model 'FixedSite'
        db.create_table(u'core_fixedsite', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=255)),
            ('deployment', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sites', to=orm['core.Deployment'])),
            ('url', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('geo_location', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.GeoLocation'], unique=True, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['FixedSite'])

        # Adding model 'CalibrationData'
        db.create_table(u'core_calibrationdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('calibration_datastore', self.gf('django.db.models.fields.related.ForeignKey')(related_name='calibration_data', to=orm['core.CalibrationDataStore'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, db_index=True, blank=True)),
            ('value', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='calibration_data', null=True, to=orm['core.Contact'])),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['CalibrationData'])

        # Adding index on 'CalibrationData', fields ['calibration_datastore', 'timestamp']
        db.create_index(u'core_calibrationdata', ['calibration_datastore_id', 'timestamp'])

        # Adding model 'DeviceType'
        db.create_table(u'core_devicetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('manufacturer', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('model', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('datasheet_url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['DeviceType'])

        # Adding model 'LocationData'
        db.create_table(u'core_locationdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='location_data', null=True, to=orm['core.Device'])),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, db_index=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('elevation', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['LocationData'])

        # Adding index on 'LocationData', fields ['device', 'timestamp']
        db.create_index(u'core_locationdata', ['device_id', 'timestamp'])

        # Adding model 'APIData'
        db.create_table(u'core_apidata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('api_datastore', self.gf('django.db.models.fields.related.ForeignKey')(related_name='api_scalar_data', to=orm['core.APIDataStore'])),
            ('api_call', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('api_access_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, db_index=True, blank=True)),
            ('duration_sec', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'core', ['APIData'])

        # Adding index on 'APIData', fields ['api_datastore', 'timestamp']
        db.create_index(u'core_apidata', ['api_datastore_id', 'timestamp'])

        # Adding model 'Sensor'
        db.create_table(u'core_sensor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sensors', to=orm['core.Device'])),
            ('sensor_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sensors', to=orm['core.SensorType'])),
            ('metric', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sensors', to=orm['core.Metric'])),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sensors', to=orm['core.Unit'])),
            ('data_status', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('manufacture_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('deploy_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('metadata', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Sensor'])

        # Adding model 'CalibrationDataStore'
        db.create_table(u'core_calibrationdatastore', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sensor', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='calibration_datastore', null=True, to=orm['core.Sensor'])),
            ('fixed_site', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='calibration_datastore', null=True, to=orm['core.FixedSite'])),
            ('metric', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='calibration_datastore', null=True, to=orm['core.Metric'])),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='calibration_datastore', null=True, to=orm['core.Unit'])),
            ('metadata', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'core', ['CalibrationDataStore'])

        # Adding model 'APIDataStore'
        db.create_table(u'core_apidatastore', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='api_datastore', null=True, to=orm['core.Device'])),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='api_datastore', null=True, to=orm['core.FixedSite'])),
            ('api', self.gf('django.db.models.fields.related.ForeignKey')(related_name='api_datastore', to=orm['core.APIType'])),
            ('metric', self.gf('django.db.models.fields.related.ForeignKey')(related_name='api_datastore', to=orm['core.Metric'])),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='api_datastore', to=orm['core.Unit'])),
            ('metadata', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['APIDataStore'])

        # Deleting field 'Device.building'
        db.delete_column(u'core_device', 'building')

        # Deleting field 'Device.room'
        db.delete_column(u'core_device', 'room')

        # Deleting field 'Device.floor'
        db.delete_column(u'core_device', 'floor')

        # Deleting field 'Device.geo_location'
        db.delete_column(u'core_device', 'geo_location_id')

        # Deleting field 'Device.name'
        db.delete_column(u'core_device', 'name')

        # Adding field 'Device.unique_name'
        db.add_column(u'core_device', 'unique_name',
                      self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=255),
                      keep_default=False)

        # Adding field 'Device.device_type'
        db.add_column(u'core_device', 'device_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='devices', to=orm['core.DeviceType']),
                      keep_default=False)

        # Adding field 'Device.deployment'
        db.add_column(u'core_device', 'deployment',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='devices', null=True, to=orm['core.Deployment']),
                      keep_default=False)

        # Adding field 'Device.manufacture_date'
        db.add_column(u'core_device', 'manufacture_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Device.deploy_date'
        db.add_column(u'core_device', 'deploy_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Device.serial_no'
        db.add_column(u'core_device', 'serial_no',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)


        # Changing field 'Device.description'
        db.alter_column(u'core_device', 'description', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Device.site'
        db.alter_column(u'core_device', 'site_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['core.FixedSite']))

    def backwards(self, orm):
        # Removing index on 'APIData', fields ['api_datastore', 'timestamp']
        db.delete_index(u'core_apidata', ['api_datastore_id', 'timestamp'])

        # Removing index on 'LocationData', fields ['device', 'timestamp']
        db.delete_index(u'core_locationdata', ['device_id', 'timestamp'])

        # Removing index on 'CalibrationData', fields ['calibration_datastore', 'timestamp']
        db.delete_index(u'core_calibrationdata', ['calibration_datastore_id', 'timestamp'])

        # Removing index on 'SensorData', fields ['sensor', 'timestamp']
        db.delete_index(u'core_sensordata', ['sensor_id', 'timestamp'])

        # Adding index on 'ScalarData', fields ['sensor', 'timestamp']
        db.create_index(u'core_scalardata', ['sensor_id', 'timestamp'])

        # Adding model 'Person'
        db.create_table(u'core_person', (
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('twitter_handle', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('geo_location', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.GeoLocation'], unique=True, null=True, blank=True)),
            ('picture_url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rfid', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(related_name='people', to=orm['core.Site'])),
        ))
        db.send_create_signal(u'core', ['Person'])

        # Adding model 'ScalarData'
        db.create_table(u'core_scalardata', (
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True, db_index=True)),
            ('sensor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='scalar_data', to=orm['core.ScalarSensor'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'core', ['ScalarData'])

        # Adding model 'StatusUpdate'
        db.create_table(u'core_statusupdate', (
            ('status', self.gf('django.db.models.fields.TextField')()),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='status_updates', to=orm['core.Person'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal(u'core', ['StatusUpdate'])

        # Adding model 'Site'
        db.create_table(u'core_site', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('raw_zmq_stream', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('geo_location', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.GeoLocation'], unique=True, null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'core', ['Site'])

        # Adding model 'PresenceData'
        db.create_table(u'core_presencedata', (
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(related_name='presense_data', to=orm['core.Person'])),
            ('sensor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='presence_data', to=orm['core.PresenceSensor'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('present', self.gf('django.db.models.fields.BooleanField')()),
        ))
        db.send_create_signal(u'core', ['PresenceData'])

        # Adding model 'ScalarSensor'
        db.create_table(u'core_scalarsensor', (
            ('metric', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sensors', to=orm['core.Metric'])),
            ('geo_location', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.GeoLocation'], unique=True, null=True, blank=True)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sensors', to=orm['core.Device'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sensors', to=orm['core.Unit'])),
            ('metadata', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'core', ['ScalarSensor'])

        # Adding unique constraint on 'ScalarSensor', fields ['device', 'metric']
        db.create_unique(u'core_scalarsensor', ['device_id', 'metric_id'])

        # Adding model 'PresenceSensor'
        db.create_table(u'core_presencesensor', (
            ('metric', self.gf('django.db.models.fields.related.ForeignKey')(related_name='presence_sensors', to=orm['core.Metric'])),
            ('geo_location', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.GeoLocation'], unique=True, null=True, blank=True)),
            ('device', self.gf('django.db.models.fields.related.ForeignKey')(related_name='presence_sensors', to=orm['core.Device'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('metadata', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'core', ['PresenceSensor'])

        # Adding unique constraint on 'PresenceSensor', fields ['device', 'metric']
        db.create_unique(u'core_presencesensor', ['device_id', 'metric_id'])

        # Deleting model 'Contact'
        db.delete_table(u'core_contact')

        # Removing M2M table for field deployments on 'Contact'
        db.delete_table(db.shorten_name(u'core_contact_deployments'))

        # Removing M2M table for field sites on 'Contact'
        db.delete_table(db.shorten_name(u'core_contact_sites'))

        # Removing M2M table for field devices on 'Contact'
        db.delete_table(db.shorten_name(u'core_contact_devices'))

        # Deleting model 'SensorType'
        db.delete_table(u'core_sensortype')

        # Deleting model 'Deployment'
        db.delete_table(u'core_deployment')

        # Deleting model 'Organization'
        db.delete_table(u'core_organization')

        # Deleting model 'APIType'
        db.delete_table(u'core_apitype')

        # Deleting model 'SensorData'
        db.delete_table(u'core_sensordata')

        # Deleting model 'FixedSite'
        db.delete_table(u'core_fixedsite')

        # Deleting model 'CalibrationData'
        db.delete_table(u'core_calibrationdata')

        # Deleting model 'DeviceType'
        db.delete_table(u'core_devicetype')

        # Deleting model 'LocationData'
        db.delete_table(u'core_locationdata')

        # Deleting model 'APIData'
        db.delete_table(u'core_apidata')

        # Deleting model 'Sensor'
        db.delete_table(u'core_sensor')

        # Deleting model 'CalibrationDataStore'
        db.delete_table(u'core_calibrationdatastore')

        # Deleting model 'APIDataStore'
        db.delete_table(u'core_apidatastore')

        # Adding field 'Device.building'
        db.add_column(u'core_device', 'building',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'Device.room'
        db.add_column(u'core_device', 'room',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'Device.floor'
        db.add_column(u'core_device', 'floor',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=10, blank=True),
                      keep_default=False)

        # Adding field 'Device.geo_location'
        db.add_column(u'core_device', 'geo_location',
                      self.gf('django.db.models.fields.related.OneToOneField')(to=orm['core.GeoLocation'], unique=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Device.name'
        db.add_column(u'core_device', 'name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255),
                      keep_default=False)

        # Deleting field 'Device.unique_name'
        db.delete_column(u'core_device', 'unique_name')

        # Deleting field 'Device.device_type'
        db.delete_column(u'core_device', 'device_type_id')

        # Deleting field 'Device.deployment'
        db.delete_column(u'core_device', 'deployment_id')

        # Deleting field 'Device.manufacture_date'
        db.delete_column(u'core_device', 'manufacture_date')

        # Deleting field 'Device.deploy_date'
        db.delete_column(u'core_device', 'deploy_date')

        # Deleting field 'Device.serial_no'
        db.delete_column(u'core_device', 'serial_no')


        # Changing field 'Device.description'
        db.alter_column(u'core_device', 'description', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Device.site'
        db.alter_column(u'core_device', 'site_id', self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['core.Site']))
        # Adding unique constraint on 'Device', fields ['site', 'name', 'building', 'floor', 'room']
        db.create_unique(u'core_device', ['site_id', 'name', 'building', 'floor', 'room'])


    models = {
        u'core.apidata': {
            'Meta': {'object_name': 'APIData', 'index_together': "[['api_datastore', 'timestamp']]"},
            'api_access_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'api_call': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'api_datastore': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'api_scalar_data'", 'to': u"orm['core.APIDataStore']"}),
            'duration_sec': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        u'core.apidatastore': {
            'Meta': {'object_name': 'APIDataStore'},
            'api': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'api_datastore'", 'to': u"orm['core.APIType']"}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'api_datastore'", 'null': 'True', 'to': u"orm['core.Device']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'api_datastore'", 'to': u"orm['core.Metric']"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'api_datastore'", 'null': 'True', 'to': u"orm['core.FixedSite']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'api_datastore'", 'to': u"orm['core.Unit']"})
        },
        u'core.apitype': {
            'Meta': {'object_name': 'APIType'},
            'api_base_address': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'api_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'core.calibrationdata': {
            'Meta': {'object_name': 'CalibrationData', 'index_together': "[['calibration_datastore', 'timestamp']]"},
            'calibration_datastore': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'calibration_data'", 'to': u"orm['core.CalibrationDataStore']"}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'calibration_data'", 'null': 'True', 'to': u"orm['core.Contact']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'core.calibrationdatastore': {
            'Meta': {'object_name': 'CalibrationDataStore'},
            'fixed_site': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'calibration_datastore'", 'null': 'True', 'to': u"orm['core.FixedSite']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'calibration_datastore'", 'null': 'True', 'to': u"orm['core.Metric']"}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'calibration_datastore'", 'null': 'True', 'to': u"orm['core.Sensor']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'calibration_datastore'", 'null': 'True', 'to': u"orm['core.Unit']"})
        },
        u'core.contact': {
            'Meta': {'ordering': "['last_name']", 'object_name': 'Contact'},
            'deployments': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'contacts'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['core.Deployment']"}),
            'devices': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'contacts'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['core.Device']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'contacts'", 'null': 'True', 'to': u"orm['core.Organization']"}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'sites': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'contacts'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['core.FixedSite']"})
        },
        u'core.deployment': {
            'Meta': {'object_name': 'Deployment'},
            'geo_location': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.GeoLocation']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'deployments'", 'to': u"orm['core.Organization']"})
        },
        u'core.device': {
            'Meta': {'ordering': "['unique_name']", 'object_name': 'Device'},
            'deploy_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deployment': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'devices'", 'null': 'True', 'to': u"orm['core.Deployment']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'device_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'devices'", 'to': u"orm['core.DeviceType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacture_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'serial_no': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'devices'", 'null': 'True', 'to': u"orm['core.FixedSite']"}),
            'unique_name': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '255'})
        },
        u'core.devicetype': {
            'Meta': {'object_name': 'DeviceType'},
            'datasheet_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'core.fixedsite': {
            'Meta': {'object_name': 'FixedSite'},
            'deployment': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sites'", 'to': u"orm['core.Deployment']"}),
            'geo_location': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['core.GeoLocation']", 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '255'}),
            'url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        u'core.geolocation': {
            'Meta': {'object_name': 'GeoLocation'},
            'elevation': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {})
        },
        u'core.locationdata': {
            'Meta': {'object_name': 'LocationData', 'index_together': "[['device', 'timestamp']]"},
            'device': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'location_data'", 'null': 'True', 'to': u"orm['core.Device']"}),
            'elevation': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True', 'blank': 'True'})
        },
        u'core.metric': {
            'Meta': {'object_name': 'Metric'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '255'})
        },
        u'core.organization': {
            'Meta': {'object_name': 'Organization'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'raw_zmq_stream': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'})
        },
        u'core.sensor': {
            'Meta': {'object_name': 'Sensor'},
            'data_status': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'deploy_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'device': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sensors'", 'to': u"orm['core.Device']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manufacture_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'metadata': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sensors'", 'to': u"orm['core.Metric']"}),
            'sensor_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sensors'", 'to': u"orm['core.SensorType']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sensors'", 'to': u"orm['core.Unit']"})
        },
        u'core.sensordata': {
            'Meta': {'object_name': 'SensorData', 'index_together': "[['sensor', 'timestamp']]"},
            'duration_sec': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sensor_data'", 'to': u"orm['core.Sensor']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        u'core.sensortype': {
            'Meta': {'object_name': 'SensorType'},
            'datasheet_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'learn_priority': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'manufacturer': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'retail_cost': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'sensor_topology': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'service_interval_days': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'core.unit': {
            'Meta': {'object_name': 'Unit'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['core']
