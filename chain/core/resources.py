from chain.core.api import Resource, ResourceField, CollectionField
from chain.core.api import full_reverse
from chain.core.api import CHAIN_CURIES
from chain.core.api import BadRequestException
from chain.core.api import register_resource
from chain.core.models import Organization, Deployment, FixedSite, Device, \
    Sensor, SensorType, SensorData, APIDataStore, APIData, APIType, \
    CalibrationDataStore, CalibrationData, LocationData, Contact, DeviceType
from django.conf.urls import include, patterns, url
from django.utils import timezone
from datetime import timedelta, datetime
import calendar
import itertools

# Edited DRAMSAY
class SensorDataResource(Resource):
    model = SensorData
    display_field = 'timestamp'
    resource_name = 'sensor_data'
    resource_type = 'sensor_data'
    model_fields = ['timestamp', 'value', 'duration_sec']
    required_fields = ['value']
    queryset = SensorData.objects
    default_timespan = timedelta(hours=6)

    def __init__(self, *args, **kwargs):
        super(SensorDataResource, self).__init__(*args, **kwargs)
        if 'queryset' in kwargs:
            # we want to default to the last page, not the first page
            pass

    def serialize_list(self, embed, cache):
        '''a "list" of SensorData resources is actually represented
        as a single resource with a list of data points'''

        if not embed:
            return super(
                SensorDataResource,
                self).serialize_list(
                embed,
                cache)

        href = self.get_list_href()

        serialized_data = {
            '_links': {
                'curies': CHAIN_CURIES,
                'createForm': {
                    'href': self.get_create_href(),
                    'title': 'Add Data'
                }
            },
            'dataType': 'float'
        }
        request_time = timezone.now()

        # if the time filters aren't given then use the most recent timespan,
        # if they are given, then we need to convert them from unix time to use
        # in the queryset filter
        if 'timestamp__gte' in self._filters:
            try:
                page_start = datetime.utcfromtimestamp(
                    float(self._filters['timestamp__gte'])).replace(
                        tzinfo=timezone.utc)
            except ValueError:
                raise BadRequestException(
                    "Invalid timestamp format for lower bound of date range.")
        else:
            page_start = request_time - self.default_timespan

        if 'timestamp__lt' in self._filters:
            try:
                page_end = datetime.utcfromtimestamp(
                    float(self._filters['timestamp__lt'])).replace(
                        tzinfo=timezone.utc)
            except ValueError:
                raise BadRequestException(
                    "Invalid timestamp format for upper bound of date range.")
        else:
            page_end = request_time

        self._filters['timestamp__gte'] = page_start
        self._filters['timestamp__lt'] = page_end

        objs = self._queryset.filter(**self._filters).order_by('timestamp')

        serialized_data = self.add_page_links(serialized_data, href,
                                              page_start, page_end)
        serialized_data['data'] = [{
            'value': obj.value,
            'timestamp': obj.timestamp.isoformat(),
            'duration_sec': obj.duration_sec}
            for obj in objs]
        return serialized_data

    def format_time(self, timestamp):
        return calendar.timegm(timestamp.timetuple())

    def add_page_links(self, data, href, page_start, page_end):
        timespan = page_end - page_start
        data['_links']['previous'] = {
            'href': self.update_href(
                href, timestamp__gte=self.format_time(page_start - timespan),
                timestamp__lt=self.format_time(page_start)),
            'title': '%s to %s' % (page_start - timespan, page_start),
        }
        data['_links']['self'] = {
            'href': self.update_href(
                href, timestamp__gte=self.format_time(page_start),
                timestamp__lt=self.format_time(page_end)),
        }
        data['_links']['next'] = {
            'href': self.update_href(
                href, timestamp__gte=self.format_time(page_end),
                timestamp__lt=self.format_time(page_end + timespan)),
            'title': '%s to %s' % (page_end, page_end + timespan),
        }
        return data

    def serialize_stream(self):
        '''Serialize this resource for a stream'''
        data = self.serialize_single(rels=False)
        data['_links'] = {
            'self': {'href': self.get_single_href()},
            'ch:sensor': {'href': full_reverse(
                'sensors-single', self._request,
                args=(self._filters['sensor_id'],))}
        }
        return data

    def get_tags(self):
        if not self._obj:
            raise ValueError(
                'Tried to called get_tags on a resource without an object')
        db_sensor = ScalarSensor.objects.select_related('device').get(
            id=self._obj.sensor_id)
        return ['sensor-%d' % db_sensor.id,
                'device-%d' % db_sensor.device_id,
                'site-%d' % db_sensor.device.site_id]


# Edited DRAMSAY
class CalibrationDataResource(Resource):
    model = CalibrationData
    display_field = 'timestamp'
    resource_name = 'calibration_data'
    resource_type = 'calibration_data'
    model_fields = ['timestamp', 'value', 'description']
    required_fields = []
    related_fields = {
        'ch:contacts': CollectionField('chain.core.resources.ContactResource',
                                            reverse_name='calibration_data'),
    }
    queryset = CalibrationData.objects
    default_timespan = timedelta(days=6)

    def __init__(self, *args, **kwargs):
        super(CalibrationDataResource, self).__init__(*args, **kwargs)
        if 'queryset' in kwargs:
            # we want to default to the last page, not the first page
            pass

    def serialize_list(self, embed, cache):
        '''a "list" of CalibrationData resources is actually represented
        as a single resource with a list of data points'''

        if not embed:
            return super(
                CalibrationDataResource,
                self).serialize_list(
                embed,
                cache)

        href = self.get_list_href()

        serialized_data = {
            '_links': {
                'curies': CHAIN_CURIES,
                'createForm': {
                    'href': self.get_create_href(),
                    'title': 'Add Data'
                }
            },
            'dataType': 'float'
        }
        request_time = timezone.now()

        # if the time filters aren't given then use the most recent timespan,
        # if they are given, then we need to convert them from unix time to use
        # in the queryset filter
        if 'timestamp__gte' in self._filters:
            try:
                page_start = datetime.utcfromtimestamp(
                    float(self._filters['timestamp__gte'])).replace(
                        tzinfo=timezone.utc)
            except ValueError:
                raise BadRequestException(
                    "Invalid timestamp format for lower bound of date range.")
        else:
            page_start = request_time - self.default_timespan

        if 'timestamp__lt' in self._filters:
            try:
                page_end = datetime.utcfromtimestamp(
                    float(self._filters['timestamp__lt'])).replace(
                        tzinfo=timezone.utc)
            except ValueError:
                raise BadRequestException(
                    "Invalid timestamp format for upper bound of date range.")
        else:
            page_end = request_time

        self._filters['timestamp__gte'] = page_start
        self._filters['timestamp__lt'] = page_end

        objs = self._queryset.filter(**self._filters).order_by('timestamp')

        serialized_data = self.add_page_links(serialized_data, href,
                                              page_start, page_end)
        serialized_data['data'] = [{
            'value': obj.value,
            'timestamp': obj.timestamp.isoformat(),
            'description': obj.description}
            for obj in objs]
        return serialized_data

    def format_time(self, timestamp):
        return calendar.timegm(timestamp.timetuple())

    def add_page_links(self, data, href, page_start, page_end):
        timespan = page_end - page_start
        data['_links']['previous'] = {
            'href': self.update_href(
                href, timestamp__gte=self.format_time(page_start - timespan),
                timestamp__lt=self.format_time(page_start)),
            'title': '%s to %s' % (page_start - timespan, page_start),
        }
        data['_links']['self'] = {
            'href': self.update_href(
                href, timestamp__gte=self.format_time(page_start),
                timestamp__lt=self.format_time(page_end)),
        }
        data['_links']['next'] = {
            'href': self.update_href(
                href, timestamp__gte=self.format_time(page_end),
                timestamp__lt=self.format_time(page_end + timespan)),
            'title': '%s to %s' % (page_end, page_end + timespan),
        }
        return data

    def serialize_stream(self):
        '''Serialize this resource for a stream'''
        data = self.serialize_single(rels=False)
        data['_links'] = {
            'self': {'href': self.get_single_href()},
            'ch:calibration_datastore': {'href': full_reverse(
                'calibration_datastore-single', self._request,
                args=(self._filters['calibration_datastore_id'],))}
        }
        return data

    def get_tags(self):
        if not self._obj:
            raise ValueError(
                'Tried to called get_tags on a resource without an object')
        db_sensor = ScalarSensor.objects.select_related('device').get(
            id=self._obj.sensor_id)
        return ['calibration_datastore-%d' % db_calibration_datastore.id]


# Edited DRAMSAY
class APIDataResource(Resource):
    model = APIData
    display_field = 'timestamp'
    resource_name = 'api_data'
    resource_type = 'api_data'
    model_fields = ['timestamp', 'value', 'duration_sec', 'api_access_time', 'api_call']
    required_fields = ['value']
    queryset = APIData.objects
    default_timespan = timedelta(hours=6)

    def __init__(self, *args, **kwargs):
        super(APIDataResource, self).__init__(*args, **kwargs)
        if 'queryset' in kwargs:
            # we want to default to the last page, not the first page
            pass

    def serialize_list(self, embed, cache):
        '''a "list" of SensorData resources is actually represented
        as a single resource with a list of data points'''

        if not embed:
            return super(
                APIDataResource,
                self).serialize_list(
                embed,
                cache)

        href = self.get_list_href()

        serialized_data = {
            '_links': {
                'curies': CHAIN_CURIES,
                'createForm': {
                    'href': self.get_create_href(),
                    'title': 'Add Data'
                }
            },
            'dataType': 'float'
        }
        request_time = timezone.now()

        # if the time filters aren't given then use the most recent timespan,
        # if they are given, then we need to convert them from unix time to use
        # in the queryset filter
        if 'timestamp__gte' in self._filters:
            try:
                page_start = datetime.utcfromtimestamp(
                    float(self._filters['timestamp__gte'])).replace(
                        tzinfo=timezone.utc)
            except ValueError:
                raise BadRequestException(
                    "Invalid timestamp format for lower bound of date range.")
        else:
            page_start = request_time - self.default_timespan

        if 'timestamp__lt' in self._filters:
            try:
                page_end = datetime.utcfromtimestamp(
                    float(self._filters['timestamp__lt'])).replace(
                        tzinfo=timezone.utc)
            except ValueError:
                raise BadRequestException(
                    "Invalid timestamp format for upper bound of date range.")
        else:
            page_end = request_time

        self._filters['timestamp__gte'] = page_start
        self._filters['timestamp__lt'] = page_end

        objs = self._queryset.filter(**self._filters).order_by('timestamp')

        serialized_data = self.add_page_links(serialized_data, href,
                                              page_start, page_end)
        serialized_data['data'] = [{
            'value': obj.value,
            'timestamp': obj.timestamp.isoformat(),
            'duration_sec': obj.duration_sec,
            'api_call': obj.api_call,
            'api_access_time': obj.api_access_time.isoformat()}
            for obj in objs]
        return serialized_data

    def format_time(self, timestamp):
        return calendar.timegm(timestamp.timetuple())

    def add_page_links(self, data, href, page_start, page_end):
        timespan = page_end - page_start
        data['_links']['previous'] = {
            'href': self.update_href(
                href, timestamp__gte=self.format_time(page_start - timespan),
                timestamp__lt=self.format_time(page_start)),
            'title': '%s to %s' % (page_start - timespan, page_start),
        }
        data['_links']['self'] = {
            'href': self.update_href(
                href, timestamp__gte=self.format_time(page_start),
                timestamp__lt=self.format_time(page_end)),
        }
        data['_links']['next'] = {
            'href': self.update_href(
                href, timestamp__gte=self.format_time(page_end),
                timestamp__lt=self.format_time(page_end + timespan)),
            'title': '%s to %s' % (page_end, page_end + timespan),
        }
        return data

    def serialize_stream(self):
        '''Serialize this resource for a stream'''
        data = self.serialize_single(rels=False)
        data['_links'] = {
            'self': {'href': self.get_single_href()},
            'ch:api_datstore': {'href': full_reverse(
                'api_datastore-single', self._request,
                args=(self._filters['api_datastore_id'],))}
        }
        return data

    def get_tags(self):
        if not self._obj:
            raise ValueError(
                'Tried to called get_tags on a resource without an object')
        db_sensor = ScalarSensor.objects.select_related('device').get(
            id=self._obj.sensor_id)
        return ['api_datastore-%d' % db_api_datastore.id]


# Edited DRAMSAY
class LocationDataResource(Resource):
    model = LocationData
    display_field = 'timestamp'
    resource_name = 'location_data'
    resource_type = 'location_data'
    model_fields = ['timestamp', 'elevation']
    required_fields = ['latitude','longitude']
    queryset = LocationData.objects
    default_timespan = timedelta(hours=6)

    def __init__(self, *args, **kwargs):
        super(LocationDataResource, self).__init__(*args, **kwargs)
        if 'queryset' in kwargs:
            # we want to default to the last page, not the first page
            pass

    def serialize_list(self, embed, cache):
        '''a "list" of SensorData resources is actually represented
        as a single resource with a list of data points'''

        if not embed:
            return super(
                LocationDataResource,
                self).serialize_list(
                embed,
                cache)

        href = self.get_list_href()

        serialized_data = {
            '_links': {
                'curies': CHAIN_CURIES,
                'createForm': {
                    'href': self.get_create_href(),
                    'title': 'Add Data'
                }
            }
        }
        request_time = timezone.now()

        # if the time filters aren't given then use the most recent timespan,
        # if they are given, then we need to convert them from unix time to use
        # in the queryset filter
        if 'timestamp__gte' in self._filters:
            try:
                page_start = datetime.utcfromtimestamp(
                    float(self._filters['timestamp__gte'])).replace(
                        tzinfo=timezone.utc)
            except ValueError:
                raise BadRequestException(
                    "Invalid timestamp format for lower bound of date range.")
        else:
            page_start = request_time - self.default_timespan

        if 'timestamp__lt' in self._filters:
            try:
                page_end = datetime.utcfromtimestamp(
                    float(self._filters['timestamp__lt'])).replace(
                        tzinfo=timezone.utc)
            except ValueError:
                raise BadRequestException(
                    "Invalid timestamp format for upper bound of date range.")
        else:
            page_end = request_time

        self._filters['timestamp__gte'] = page_start
        self._filters['timestamp__lt'] = page_end

        objs = self._queryset.filter(**self._filters).order_by('timestamp')

        serialized_data = self.add_page_links(serialized_data, href,
                                              page_start, page_end)
        serialized_data['data'] = [{
            'latitude': obj.latitude,
            'longitude': obj.longitude,
            'timestamp': obj.timestamp.isoformat(),
            'elevation': obj.elevation}
            for obj in objs]
        return serialized_data

    def format_time(self, timestamp):
        return calendar.timegm(timestamp.timetuple())

    def add_page_links(self, data, href, page_start, page_end):
        timespan = page_end - page_start
        data['_links']['previous'] = {
            'href': self.update_href(
                href, timestamp__gte=self.format_time(page_start - timespan),
                timestamp__lt=self.format_time(page_start)),
            'title': '%s to %s' % (page_start - timespan, page_start),
        }
        data['_links']['self'] = {
            'href': self.update_href(
                href, timestamp__gte=self.format_time(page_start),
                timestamp__lt=self.format_time(page_end)),
        }
        data['_links']['next'] = {
            'href': self.update_href(
                href, timestamp__gte=self.format_time(page_end),
                timestamp__lt=self.format_time(page_end + timespan)),
            'title': '%s to %s' % (page_end, page_end + timespan),
        }
        return data

    def serialize_stream(self):
        '''Serialize this resource for a stream'''
        data = self.serialize_single(rels=False)
        data['_links'] = {
            'self': {'href': self.get_single_href()},
            'ch:device': {'href': full_reverse(
                'device-single', self._request,
                args=(self._filters['device_id'],))}
        }
        return data

    def get_tags(self):
        if not self._obj:
            raise ValueError(
                'Tried to called get_tags on a resource without an object')
        return ['device-%d' % db_device.id]


class SensorTypeResource(Resource):

    model = SensorType
    display_field = 'model'
    resource_name = 'sensor_types'
    resource_type = 'sensor_type'
    required_fields = ['model']
    model_fields = ['manufacturer', 'revision', 'datasheet_url', 'description', 'learn_priority','service_interval_days', 'sensor_topology']
    related_fields = {
        'ch:sensors': CollectionField('chain.core.resources.SensorResource',
                                      reverse_name='sensor_type')
    }
    queryset = SensorType.objects


# Edited DRAMSAY
class SensorResource(Resource):

    model = Sensor
    display_field = 'metric'
    resource_name = 'sensors'
    resource_type = 'sensor'
    model_fields = ['data_status', 'manufacture_date', 'deploy_date', 'metadata']
    required_fields = ['metric', 'unit']

    # for now, name is hardcoded as the only attribute of metric and unit
    stub_fields = {'metric': 'name', 'unit': 'name'}
    queryset = Sensor.objects
    related_fields = {
        'ch:dataHistory': CollectionField(SensorDataResource,
                                          reverse_name='sensor'),
        'ch:device': ResourceField('chain.core.resources.DeviceResource',
                                   'device'),
        'ch:sensor_type': ResourceField('chain.core.resources.SensorTypeResource',
                                   'sensor_type')
    }

    def serialize_single(self, embed, cache, *args, **kwargs):
        data = super(
            SensorResource,
            self).serialize_single(
            embed,
            cache,
            *args,
            **kwargs)

        if embed:
            data['dataType'] = 'float'
            last_data = self._obj.scalar_data.order_by(
                'timestamp').reverse()[:1]
            if last_data:
                data['value'] = last_data[0].value
                data['updated'] = last_data[0].timestamp.isoformat()
        return data

    def get_tags(self):
        return ['sensor-%s' % self._obj.id,
                'device-%s' % self._obj.device_id]


# Edited DRAMSAY
class CalibrationDataStoreResource(Resource):

    model = CalibrationDataStore
    display_field = 'metric'
    resource_name = 'calibration_datastore'
    resource_type = 'calibration_datastore'
    model_fields = ['metadata']
    required_fields = ['metric', 'unit']

    # for now, name is hardcoded as the only attribute of metric and unit
    stub_fields = {'metric': 'name', 'unit': 'name'}
    queryset = CalibrationDataStore.objects
    related_fields = {
        'ch:dataHistory': CollectionField(CalibrationDataResource,
                                          reverse_name='calibration_datastore'),
        'ch:sensor': ResourceField('chain.core.resources.SensorResource',
                                   'sensor'),
        'ch:site': ResourceField('chain.core.resources.FixedSiteResource',
                                   'site')
    }

    def serialize_single(self, embed, cache, *args, **kwargs):
        data = super(
            ScalarSensorResource,
            self).serialize_single(
            embed,
            cache,
            *args,
            **kwargs)

        if embed:
            data['dataType'] = 'float'
            last_data = self._obj.scalar_data.order_by(
                'timestamp').reverse()[:1]
            if last_data:
                data['value'] = last_data[0].value
                data['updated'] = last_data[0].timestamp.isoformat()
        return data

    def get_tags(self):
        return ['calibration_datastore-%s' % self._obj.id,
                'sensor-%s' % self._obj.sensor_id,
                'site-%s' % self._obj.site_id]


class APITypeResource(Resource):

    model = APIType
    display_field = 'name'
    resource_name = 'api_types'
    resource_type = 'api_type'
    required_fields = ['name']
    model_fields = ['api_base_address','description']
    related_fields = {
        'ch:api_datastores': CollectionField('chain.core.resources.APIDataStoreResource',
                                      reverse_name='api_type')
    }
    queryset = APIType.objects


# Edited DRAMSAY
class APIDataStoreResource(Resource):

    model = APIDataStore
    display_field = 'metric'
    resource_name = 'api_datastores'
    resource_type = 'api_datastore'
    model_fields = ['metadata']
    required_fields = ['metric', 'unit']

    # for now, name is hardcoded as the only attribute of metric and unit
    stub_fields = {'metric': 'name', 'unit': 'name'}
    queryset = APIDataStore.objects
    related_fields = {
        'ch:dataHistory': CollectionField(APIDataResource,
                                          reverse_name='api_data'),
        'ch:device': ResourceField('chain.core.resources.DeviceResource',
                                   'device'),
        'ch:site': ResourceField('chain.core.resources.FixedSiteResource',
                                   'site'),
        'ch:api': ResourceField('chain.core.resources.APITypeResource',
                                   'api_type'),
        'ch:api_type': ResourceField('chain.core.resources.APITypeResource',
                                   'api_type')
    }

    def serialize_single(self, embed, cache, *args, **kwargs):
        data = super(
            APIDataStoreResource,
            self).serialize_single(
            embed,
            cache,
            *args,
            **kwargs)

        if embed:
            data['dataType'] = 'float'
            last_data = self._obj.scalar_data.order_by(
                'timestamp').reverse()[:1]
            if last_data:
                data['value'] = last_data[0].value
                data['updated'] = last_data[0].timestamp.isoformat()
        return data

    def get_tags(self):
        return ['api_datastore-%s' % self._obj.id,
                'device-%s' % self._obj.device_id,
                'site-%s' % self._obj.site_id]


# Edited DRAMSAY
class ContactResource(Resource):

    model = Contact
    display_field = 'last_name'
    resource_name = 'contacts'
    resource_type = 'contact'
    required_fields = ['first_name', 'last_name']
    model_fields = ['first_name', 'last_name', 'email', 'phone']
    ''' related_fields = {
        'ch:organization': ResourceField('chain.core.resources.OrganizationResource',
                                            'organization'),
        'ch:deployment': CollectionField('chain.core.resources.DeploymentResource',
                                            reverse_name='contact'),
        'ch:site': CollectionField('chain.core.resources.SiteResource',
                                            reverse_name='contact'),
        'ch:device': CollectionField('chain.core.resources.DeviceResource',
                                            reverse_name='contact'),
        'ch:calibration_data': CollectionField('chain.core.resources.CalibrationDataResource',
                                            reverse_name='contact')
    }
    '''
    queryset = Contact.objects

    def serialize_single(self, embed, cache, *args, **kwargs):
        data = super(
            ContactResource,
            self).serialize_single(
            embed,
            cache,
            *args,
            **kwargs)
        if embed:
            if '_embedded' not in data:
                data['_embedded'] = {}
            data['_embedded'].update(self.get_additional_embedded())
        if '_links' in data:
            data['_links'].update(self.get_additional_links())
        return data

    # TODO: implment similar helper functions for contacts, to get their
    # deployments, sites, orgs, and devices

    def get_deployments(self):
        filters = {
            'contacts': self._obj
        }
        return Deployment.objects.filter(**filters)[:1]

    def get_sites(self):
        filters = {
            'contacts': self._obj
        }
        return FixedSite.objects.filter(**filters)[:1]

    def get_devices(self):
        filters = {
            'contacts': self._obj
        }
        return Device.objects.filter(**filters)[:1]

    def get_calibration_data(self):
        filters = {
            'contact': self._obj
        }
        return CalibrationData.objects.filter(**filters).order_by('timestamp')[:1]

    def get_additional_links(self):
        links = {}
        last_data = self.get_calibration_data()
        if last_data:
            links['last-visit'] = {
                'href': self.get_calibration_data_url(
                    last_data[0]),
                'title': "at %s->%s at time %s" %
                (last_data[0].sensor.device,
                 last_data[0].sensor.metric,
                 last_data[0].timestamp.isoformat())}
        if self._obj.picture_url:
            links['picture'] = {
                'href': self._obj.picture_url,
                'title': 'Picture URL (external)'
            }
        return links
    '''
    def get_additional_embedded(self):
        embedded = {}
        last_data = self.get_calibration_data()
        user_deployments = self.get_deployments()
        user_sites = self.get_sites()
        user_devices = self.get_devices()

        if last_data:
            embedded['last-calibration'] = ContactResource(obj=last_data[0], request=self._request)\
                .serialize_single(False, {})
        if user_deployments:
            embedded['last-deployment'] = ContactResource(obj=user_deployments[0], request=self._request)\
                .serialize_single(False, {})
        if user_sites:
            embedded['last-site'] = ContactResource(obj=user_sites[0], request=self._request)\
                .serialize_single(False, {})
        if user_devices:
            embedded['last-device'] = ContactResource(obj=user_devices[0], request=self._request)\
                .serialize_single(False, {})
        return embedded
    '''
    def get_calibration_data_url(self, obj):
        if self._request is None:
            # No way to form URL, just return the person's ID
            return obj.id
        pdata_resource = CalibrationDataResource(obj=obj, request=self._request)
        return pdata_resource.get_single_href()
    '''
    def get_tags(self):
        # sometimes the site_id field is unicode? weird
        return ['person-%d' % self._obj.id,
                'organization-%s' % self._obj.organization_id]
    '''
'''
Merge two "JSON" style dictionary/list objects
  recursively.  Designed for merging schemas from
  multiple sensor objects.

If two objects are not merge-able, the version from
  obj1 is used.
'''


def json_merge(obj1, obj2):
    if isinstance(obj1, list):
        # Merge array:
        set_used = set(obj1)
        new_arr = obj1[:]
        for el in obj2:
            if el not in set_used:
                new_arr.append(el)
        return new_arr
    elif isinstance(obj1, dict):
        # Merge object:
        new_obj = {}
        for key in obj1:
            if key in obj2:
                new_obj[key] = json_merge(obj1[key], obj2[key])
            else:
                new_obj[key] = obj1[key]
        for key in obj2:
            if key not in new_obj:
                new_obj[key] = obj2[key]
        return new_obj
    else:
        # Could not merge.  Select the version from
        #   the first object:
        return obj1


class DeviceTypeResource(Resource):

    model = DeviceType
    display_field = 'model'
    resource_name = 'device_types'
    resource_type = 'device_type'
    required_fields = ['model']
    model_fields = ['manufacturer', 'revision', 'datasheet_url', 'description']
    related_fields = {
        'ch:devices': CollectionField('chain.core.resources.DeviceResource',
                                      reverse_name='device_type')
    }
    queryset = DeviceType.objects


# Edited DRAMSAY
class DeviceResource(Resource):

    model = Device
    display_field = 'unique_name'
    resource_name = 'devices'
    resource_type = 'device'
    required_fields = ['unique_name']
    model_fields = ['unique_name', 'manufacture_date', 'deploy_date', 'serial_no', 'description']
    related_fields = {
        'ch:sensors': CollectionField(SensorResource,
                                      reverse_name='device'),
        'ch:api_datastores': CollectionField(APIDataStoreResource,
                                      reverse_name='device'),
        'ch:deployment': ResourceField('chain.core.resources.DeploymentResource', 'deployment'),
        'ch:site': ResourceField('chain.core.resources.FixedSiteResource', 'site'),
        'ch:device_type': ResourceField('chain.core.resources.DeviceTypeResource',
                                   'device_type')
    }
    queryset = Device.objects

    def get_tags(self):
        # sometimes the site_id field is unicode? weird
        return ['device-%d' % self._obj.id,
                'deployment-%s' % self._obj.deployment_id,
                'site-%s' % self._obj.site_id]


# Edited DRAMSAY
class FixedSiteResource(Resource):

    model = FixedSite
    display_field = 'name'
    resource_name = 'sites'
    resource_type = 'site'
    required_fields = ['name']
    model_fields = ['name', 'url']
    related_fields = {
        'ch:devices': CollectionField(DeviceResource,
                                      reverse_name='site'),
        'ch:api_datastores': CollectionField(APIDataStoreResource,
                                      reverse_name='site'),
        'ch:calibration_datastores': CollectionField(CalibrationDataStoreResource,
                                      reverse_name='site'),
        'ch:deployment': ResourceField('chain.core.resources.DeploymentResource', 'deployment')
    }
    queryset = FixedSite.objects

    def get_tags(self):
        # sometimes the site_id field is unicode? weird
        return ['site-%d' % self._obj.id,
                'deployment-%s' % self._obj.deployment_id]


# Edited DRAMSAY
class DeploymentResource(Resource):

    model = Deployment
    display_field = 'name'
    resource_name = 'deployments'
    resource_type = 'deployment'
    required_fields = ['name']
    model_fields = ['name']
    related_fields = {
        'ch:sites': CollectionField(FixedSiteResource,
                                      reverse_name='deployment'),
        'ch:devices': CollectionField(DeviceResource,
                                      reverse_name='deployment'),
        'ch:organization': ResourceField('chain.core.resources.OrganizationResource', 'organization')
    }
    queryset = Deployment.objects

    def get_tags(self):
        # sometimes the site_id field is unicode? weird
        return ['deployment-%d' % self._obj.id,
                'organization-%s' % self._obj.organization_id]

# Edited by DRAMSAY
class OrganizationResource(Resource):

    model = Organization

    # TODO _href should be the external URL if present

    resource_name = 'organizations'
    resource_type = 'organization'
    display_field = 'name'
    model_fields = ['name']
    required_fields = ['name']
    related_fields = {
        'ch:deployments': CollectionField(DeploymentResource, reverse_name='organization'),
        'ch:contacts': CollectionField(ContactResource, reverse_name='organization')
    }
    queryset = Organization.objects

    def serialize_single(self, embed, cache):
        data = super(OrganizationResource, self).serialize_single(embed, cache)
        if embed:
            stream = self._obj.raw_zmq_stream
            if stream:
                data['_links']['rawZMQStream'] = {
                    'href': stream,
                    'title': 'Raw ZMQ Stream'}
            data['_links']['ch:organizationSummary'] = {
                'title': 'Summary',
                'href': full_reverse('organization-summary', self._request,
                                     args=(self._obj.id,))
            }
        return data

    def get_filled_schema(self):
        schema = super(OrganizationResource, self).get_filled_schema()
        schema['properties']['rawZMQStream']['default'] = \
            self._obj.raw_zmq_stream
        return schema

    def deserialize(self):
        super(OrganizationResource, self).deserialize()
        if 'rawZMQStream' in self._data:
            self._obj.raw_zmq_stream = self._data['rawZMQStream']
        return self._obj

    def update(self, data):
        super(OrganizationResource, self).update(data)
        if 'rawZMQStream' in data:
            self._obj.raw_zmq_stream = data['rawZMQStream']
        self._obj.save()

    def get_tags(self):
        return ['organization-%d' % self._obj.id]

    @classmethod
    def get_schema(cls, filters=None):
        schema = super(OrganizationResource, cls).get_schema(filters)
        schema['properties']['rawZMQStream'] = {
            'type': 'string',
            'format': 'uri',
            'title': 'rawZMQStream'
        }
        return schema

    @classmethod
    def organization_summary_view(cls, request, id):
        time_begin = timezone.now() - timedelta(hours=2)
        #filters = request.GET.dict()
        deployments = Deployment.objects.filter(organization_id=id)
        deployment_ids = deployments.values('id')
        deployment_sites = FixedSite.objects.filter(deployment_id=deployment_ids)
        site_devices = Device.objects.filter(site_id=deployment_sites).select_related(
            'sensors',
            'sensors__metric',
            'sensors__unit'
        )
        deployment_devices = Device.objects.filter(deployment_id=deployment_ids).select_related(
            'sensors',
            'sensors__metric',
            'sensors__unit'
        )
        db_sensor_data = SensorData.objects.filter(sensor__device__deployment__organization_id=id,
                                                   timestamp__gt=time_begin)
        db_sensor_site_data = SensorData.objects.filter(sensor__device__site__deployment__organization_id=id,
                                                   timestamp__gt=time_begin)
        response = {
            '_links': {
                'self': {'href': full_reverse('organization-summary', request,
                                              args=(id,))},
            },
            'deployments': []
        }
        sensor_hash = {}
        for device in itertools.chain(site_devices, deployment_devices):
            dev_resource = DeviceResource(obj=device, request=request)
            dev_data = dev_resource.serialize(rels=False)
            dev_data['href'] = dev_resource.get_single_href()
            response['devices'].append(dev_data)
            dev_data['sensors'] = []
            for sensor in device.sensors.all():
                sensor_resource = SensorResource(
                    obj=sensor,
                    request=request)
                sensor_data = sensor_resource.serialize(rels=False)
                sensor_data['href'] = sensor_resource.get_single_href()
                dev_data['sensors'].append(sensor_data)
                sensor_data['data'] = []
                sensor_hash[sensor.id] = sensor_data

        #import pdb; pdb.set_trace()
        for data in itertools.chain(db_sensor_site_data, db_sensor_data):
            data_data = SensorDataResource(
                obj=data, request=request).serialize(rels=False)
            sensor_hash[data.sensor_id]['data'].append(data_data)
        return cls.render_response(response, request)

    @classmethod
    def urls(cls):
        base_patterns = super(OrganizationResource, cls).urls()
        base_patterns.append(
            url(r'^(\d+)/summary$', cls.organization_summary_view,
                name='organization-summary'))
        return base_patterns


# Edited DRAMSAY
class ApiRootResource(Resource):

    def __init__(self, request):
        self._request = request

    def serialize(self):
        data = {
            '_links': {
                'self': {'href': full_reverse('api-root', self._request)},
                'curies': CHAIN_CURIES,
                'ch:organizations': {
                    'title': 'Organizations',
                    'href': full_reverse('organizations-list', self._request)
                }
            }
        }
        return data

    @classmethod
    def single_view(cls, request):
        resource = cls(request=request)
        response_data = resource.serialize()
        return cls.render_response(response_data, request)


# URL Setup:

urls = patterns(
    '',
    url(r'^/?$', ApiRootResource.single_view, name='api-root')
)
'''
# add additional URLS to account for the rename of sensor to scalarsensor.
# unfortunately we can't use redirects in case clients are POSTing to outdated
# URLs. If we WERE redirecting, we would use RedirectView.as_view()
#
# put these first so they are overridden by the later ones, particularly when
# doing URL reverse lookup.

urls += patterns('',
                 url("^sensordata/", include(ScalarSensorDataResource.urls())),
                 url("^sensor/", include(ScalarSensorResource.urls())),
                 )
'''
resources = [ SensorDataResource,
    CalibrationDataResource,
    APIDataResource,
    LocationDataResource,
    SensorTypeResource,
    SensorResource,
    CalibrationDataStoreResource,
    APITypeResource,
    APIDataStoreResource,
    ContactResource,
    DeviceTypeResource,
    DeviceResource,
    FixedSiteResource,
    DeploymentResource,
    OrganizationResource]

for resource in resources:
    new_url = url("^%s/" % resource.resource_name, include(resource.urls()))
    urls += patterns('', new_url)
    register_resource(resource)
