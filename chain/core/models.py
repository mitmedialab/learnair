from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

class GeoLocation(models.Model):
    '''For Fixed Locations.  For mobile device location data, see below.'''
    latitude = models.FloatField()
    longitude = models.FloatField()
    elevation = models.FloatField(null=True, blank=True)


class Organization(models.Model):
    '''An organization that owns one or more deployments within the air
    quailty chain system. '''
    name = models.CharField(max_length=255, default="")
    url = models.CharField(max_length=255, default='', blank=True)
    raw_zmq_stream = models.CharField(max_length=255, default='', blank=True)


class Deployment(models.Model):
    '''A deployment of Chain API, usually on the scale of several to hundreds
    of devices/sites. Organizations/Deployments may host their CHAIN servers on
    remote servers, in which case the URL field will point to that resource
    on their server.  If the site is hosted locally the URL can be left blank'''
    name = models.CharField(max_length=255, default="")
    organization = models.ForeignKey(Organization, related_name='deployments')
    geo_location = models.OneToOneField(GeoLocation, null=True, blank=True)

    def __repr__(self):
        return 'Deployment(name=%r, org=%r)' % (self.name, self.organization)

    def __str__(self):
        return self.name


class FixedSite(models.Model):
    '''a stationary site with a collection of devices'''
    name = models.CharField(max_length=255, unique=True, default="")
    deployment = models.ForeignKey(Deployment, related_name='sites')
    url = models.CharField(max_length=255, default='', blank=True)
    geo_location = models.OneToOneField(GeoLocation, null=True, blank=True)


class DeviceType(models.Model):
    '''Device Information useful for multiple instances of one device type'''
    manufacturer = models.CharField(max_length=255, null=True, blank=True)
    model = models.CharField(max_length=255, default="")
    revision = models.CharField(max_length=255, null=True, blank=True)
    datasheet_url = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class Device(models.Model):
    '''A set of co-located sensors, often sharing a PCB and/or enclosure.'''
    unique_name = models.CharField(max_length=255, unique=True, default="") #unique- suggested form of 'Org-Deployment-DeviceID', aka 'ML.LA.0001' for MediaLab's LearnAir Deployment device 1
    device_type = models.ForeignKey(DeviceType, related_name='devices')
    deployment = models.ForeignKey(Deployment, related_name='devices', null=True, blank=True) #should have either this or fixed site
    site = models.ForeignKey(FixedSite, related_name='devices', null=True, blank=True) #should have either this or deployment
    manufacture_date = models.DateTimeField(null=True, blank=True)
    deploy_date = models.DateTimeField(null=True, blank=True)

    serial_no = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["unique_name"]

    def __repr__(self):
        return ('Device(site=%r, deployment=%r, name=%r, type=%r, description=%r') % (
                self.site, self.deployment, self.unique_name,
                self.device_type,  self.description)

    def __str__(self):
        return self.unique_name


class Contact(models.Model):
    '''Contact info for owners of orgs, deployments, sites, devices,
    and who run regular site maintenance and/or calibration'''
    first_name = models.CharField(max_length=50, default="")
    last_name = models.CharField(max_length=50, default="")
    email = models.EmailField(max_length=254, null=True, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(max_length=16, validators=[phone_regex], null=True, blank=True)

    organization = models.ForeignKey(Organization, related_name='contacts', null=True, blank=True)
    deployments = models.ManyToManyField(Deployment, related_name='contacts', null=True, blank=True)
    sites = models.ManyToManyField(FixedSite, related_name='contacts', null=True, blank=True)
    devices = models.ManyToManyField(Device, related_name='contacts', null=True, blank=True)

    class Meta:
        verbose_name_plural = "contacts"
        ordering = ["last_name"]


class Unit(models.Model):
    '''A unit used on a data point, such as "ug/m3", or "kWh"'''
    name = models.CharField(max_length=30, unique=True)

    def __repr__(self):
        return 'Unit(name=%r)' % self.name

    def __str__(self):
        return self.name


class Metric(models.Model):
    '''A metric that might be measured, such as "temperature", "humidity",
    or a pollutant like 'Ozone' or 'CO' or 'NO2'.  This should come from
    a finite, agreed upon list.  This is used to tie together a set of
    ScalarData points that are all measuring the same thing.'''
    name = models.CharField(max_length=255, unique=True, default="")

    def __repr__(self):
        return 'Metric(name=%r)' % self.name

    def __str__(self):
        return self.name


class SensorType(models.Model):
    '''Sensor Information useful for multiple instances of one sensor type'''
    manufacturer = models.CharField(max_length=255, null=True, blank=True)
    model = models.CharField(max_length=255, default="")
    revision = models.CharField(max_length=255, null=True, blank=True)
    datasheet_url = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    retail_cost = models.FloatField(null=True, blank=True)
    learn_priority = models.IntegerField(null=True, blank=True)
    # TODO: should be this, django upgrade to 1.8
    # service_interval = models.DurationField(null=True, blank=True)
    service_interval_days = models.FloatField(null=True, blank=True)
    sensor_topology = models.CharField(max_length=255, null=True, blank=True) #ie BAM, laser, electrochemical


class Sensor(models.Model):
    '''An individual sensor or a virtual one. There may be multiple sensors on
    a single device.  Sensors can store raw data, corrected/calibrated data, or
    virtual data that has been curated using external algorithmic models.
    The metadata field is used to store information that might be necessary to
    tie the Sensor data to the physical Sensor in the real world, such as a MAC
    address, serial number, etc.'''
    device = models.ForeignKey(Device, related_name='sensors')
    sensor_type = models.ForeignKey(SensorType, related_name='sensors')
    metric = models.ForeignKey(Metric, related_name='sensors')
    unit = models.ForeignKey(Unit, related_name='sensors')
    data_status = models.IntegerField(null=True, blank=True) #data status, i.e. 1=raw/uncalibrated, 2=calibrated, 3=algorithmicly processed
    manufacture_date = models.DateTimeField(null=True, blank=True)
    deploy_date = models.DateTimeField(null=True, blank=True)
    metadata = models.CharField(max_length=255, null=True,  blank=True)

    def __repr__(self):
        return 'Sensor(device=%r, metric=%r, unit=%r)' % (
            self.device, self.metric, self.unit)

    def __str__(self):
        return self.metric.name


class SensorData(models.Model):
    '''A data point representing scalar sensor data, such as temperature,
    humidity, etc.  Timestamp represents start of measurement, if there
    is a duration it is represented in the duration field.'''
    # Django automatically creates indices on foreign keys
    sensor = models.ForeignKey(Sensor, related_name='sensor_data')
    timestamp = models.DateTimeField(default=timezone.now, blank=True,
                                     db_index=True)
    # TODO: should be this, upgrade to django 1.8
    # duration = models.DurationField(null=True, blank=True)
    duration_sec = models.IntegerField(null=True, blank=True)
    value = models.FloatField()

    class Meta:
        verbose_name_plural = "sensor data"
        index_together = [['sensor', 'timestamp']]

    def __repr__(self):
        return 'SensorData(timestamp=%r, duration=%r, value=%r, sensor=%r)' % (
            self.timestamp, self.duration_sec, self.value, self.sensor)

    def __str__(self):
        return '%.3f %s' % (self.value, self.sensor.unit)


class APIType(models.Model):
    '''Basic info for APIs accessed to supplement data in Chain'''
    api_name = models.CharField(max_length=255, default="")
    api_base_address = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class APIDataStore(models.Model):
    '''A data store representing API data, such as weather,
    wind, etc.  This data is at the locations of the associated
    device/site and its sensors, in order to provide context.'''
    # Django automatically creates indices on foreign keys
    device = models.ForeignKey(Device, related_name='api_datastore', null=True, blank=True) #should have either this or fixed site
    site = models.ForeignKey(FixedSite, related_name='api_datastore', null=True, blank=True) #should have either this or deployment
    api = models.ForeignKey(APIType, related_name='api_datastore')
    metric = models.ForeignKey(Metric, related_name='api_datastore')
    unit = models.ForeignKey(Unit, related_name='api_datastore')
    metadata = models.CharField(max_length=255, null=True, blank=True)

    def __repr__(self):
        return 'API(metric=%r, unit=%r)' % (
            self.metric, self.unit)

    def __str__(self):
        return self.metric.name


class APIData(models.Model):
    '''API Data value'''
    api_datastore = models.ForeignKey(APIDataStore, related_name='api_scalar_data')
    api_call = models.CharField(max_length=255, null=True, blank=True)
    api_access_time = models.DateTimeField(default=timezone.now, blank=True)
    timestamp = models.DateTimeField(default=timezone.now, blank=True,
                                     db_index=True)
    #this should work, upgrade to django 1.8
    #duration = models.DurationField(null=True, blank=True)
    duration_sec = models.IntegerField(null=True, blank=True)
    value = models.FloatField()

    class Meta:
        verbose_name_plural = "api scalar data"
        index_together = [['api_datastore', 'timestamp']]

    def __repr__(self):
        return 'APIScalarData(timestamp=%r, duration=%r, value=%r, datastore=%r)' % (
            self.timestamp, self.duration_sec, self.value, self.api_datastore)

    def __str__(self):
        return '%.3f %s' % (self.value, self.api_datastore.unit)


class CalibrationDataStore(models.Model):
    '''A data store representing calibration data or site service visits.'''
    # Django automatically creates indices on foreign keys
    sensor = models.ForeignKey(Sensor, related_name='calibration_datastore', null=True, blank=True) #should have either this or fixed site
    fixed_site = models.ForeignKey(FixedSite, related_name='calibration_datastore', null=True, blank=True) #should have either this or deployment
    metric = models.ForeignKey(Metric, related_name='calibration_datastore', null=True, blank=True)
    unit = models.ForeignKey(Unit, related_name='calibration_datastore', null=True, blank=True)
    metadata = models.CharField(max_length=255, blank=True)

    def __repr__(self):
        return 'CalibrationStore(metric=%r, unit=%r)' % (
            self.metric, self.unit)

    def __str__(self):
        return self.metric.name


class CalibrationData(models.Model):
    '''API Data value'''
    calibration_datastore = models.ForeignKey(CalibrationDataStore, related_name='calibration_data')
    timestamp = models.DateTimeField(default=timezone.now, blank=True,
                                     db_index=True)
    value = models.FloatField(blank=True, null=True)
    contact = models.ForeignKey(Contact, related_name='calibration_data', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name_plural = "calibration data"
        index_together = [['calibration_datastore', 'timestamp']]

    def __repr__(self):
        return 'CalibrationData(timestamp=%r, value=%r, datastore=%r)' % (
            self.timestamp, self.value, self.calibration_datastore)

    def __str__(self):
        return '%.3f %s' % (self.value, self.calibration_datastore.unit)


'''
class LocationDataStore(models.Model):
    #A data store representing location data for mobile devices.
    device = models.ForeignKey(Device, related_name='location_datastore', null=True, blank=True) #should have either this or fixed site
    metadata = models.CharField(max_length=255, blank=True)

    def __repr__(self):
        return 'API(metric=%r, unit=%r)' % (
            self.metric, self.unit)

    def __str__(self):
        return self.metric.name
'''


class LocationData(models.Model):
    '''Mobile, timestamped Location Data for Portable Devices'''
    device = models.ForeignKey(Device, related_name='location_data', null=True, blank=True) #should have either this or fixed site
    #location_store = models.ForeignKey(LocationDataStore, related_name='location_data')
    timestamp = models.DateTimeField(default=timezone.now, blank=True,
                                     db_index=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    elevation = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "location data"
        index_together = [['device', 'timestamp']]

    def __repr__(self):
        return 'LocationData(timestamp=%r, lat=%r, lon=%r, device=%r)' % (
            self.timestamp, self.latitude, self.longitude, self.device)

