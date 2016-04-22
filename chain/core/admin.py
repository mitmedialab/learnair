from django.contrib import admin
from chain.core.models import (Organization, Deployment, FixedSite,
                                Device, DeviceType, Unit, Metric,
                                Sensor, SensorType, SensorData,
                                APIDataStore, APIType, APIData,
                                CalibrationDataStore, CalibrationData,
                                LocationData, GeoLocation, Contact)

admin.site.register(GeoLocation)
admin.site.register(Organization)
admin.site.register(Deployment)
admin.site.register(FixedSite)
admin.site.register(DeviceType)
admin.site.register(Device)
admin.site.register(Contact)
admin.site.register(Unit)
admin.site.register(Metric)
admin.site.register(SensorType)
admin.site.register(Sensor)
admin.site.register(SensorData)
admin.site.register(APIType)
admin.site.register(APIDataStore)
admin.site.register(APIData)
admin.site.register(CalibrationDataStore)
admin.site.register(CalibrationData)
admin.site.register(LocationData)

