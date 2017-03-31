# Knesset data dataservice objects

Provides interfaces to fetch from the knesset dataservice API

## How to add a new collection dataservice

* You will need to add a class that extends the [BaseKnessetDataServiceCollectionObject](https://github.com/hasadna/knesset-data-python/blob/master/knesset_data/dataservice/base.py#L207)
* this class should define:
  * `SERVICE_NAME` - a string which maps to the [dataservice constants](https://github.com/hasadna/knesset-data-python/blob/master/knesset_data/dataservice/constants.py) service urls
  * `METHOD_NAME` - a string which is appended to the service url and should be an access point to ODATA collection
  * `ORDERED_FIELDS` - an OrderedDict with:
    * key = the field name (which will be available as attribute for each object)
    * value = a DataserviceField based object which includes the source field name, type, description etc.

This minimal setup should allow you to call the object's get_all function which will return a generator yielding dataservice objects
