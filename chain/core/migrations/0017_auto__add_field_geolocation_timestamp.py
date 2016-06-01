# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'GeoLocation.timestamp'
        db.add_column(u'core_geolocation', 'timestamp',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, null=True, db_index=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'GeoLocation.timestamp'
        db.delete_column(u'core_geolocation', 'timestamp')


    models = {
        u'core.apidata': {
            'Meta': {'object_name': 'APIData', 'index_together': "[['api_datastore', 'timestamp']]"},
            'api_access_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'api_call': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'api_datastore': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'api_data'", 'to': u"orm['core.APIDataStore']"}),
            'duration_sec': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.FloatField', [], {})
        },
        u'core.apidatastore': {
            'Meta': {'object_name': 'APIDataStore'},
            'api_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'api_datastore'", 'null': 'True', 'to': u"orm['core.APIType']"}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'metric': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'calibration_datastore'", 'to': u"orm['core.Metric']"}),
            'sensor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'calibration_datastore'", 'null': 'True', 'to': u"orm['core.Sensor']"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'calibration_datastore'", 'null': 'True', 'to': u"orm['core.FixedSite']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'calibration_datastore'", 'to': u"orm['core.Unit']"})
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
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'null': 'True', 'db_index': 'True', 'blank': 'True'})
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