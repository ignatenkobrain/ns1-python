#
# Copyright (c) 2014 NSONE, Inc.
#
# License under The MIT License (MIT). See LICENSE in project root.
#

from . import resource


class Zones(resource.BaseResource):

    ROOT = 'zones'
    SEARCH_ROOT = 'search'

    INT_FIELDS = ['ttl', 'retry', 'refresh', 'expiry', 'nx_ttl']
    PASSTHRU_FIELDS = ['primary', 'secondary', 'hostmaster', 'meta', 'networks', 'link']
    BOOL_FIELDS = ['dnssec']

    def _buildBody(self, zone, **kwargs):
        body = {}
        body['zone'] = zone
        self._buildStdBody(body, kwargs)
        return body

    def import_file(self, zone, zoneFile, callback=None, errback=None,
                    **kwargs):
        files = [('zonefile', (zoneFile, open(zoneFile, 'rb'), 'text/plain'))]
        return self._make_request('PUT',
                                  'import/zonefile/%s' % (zone),
                                  files=files,
                                  callback=callback,
                                  errback=errback)

    def create(self, zone, callback=None, errback=None, **kwargs):
        body = self._buildBody(zone, **kwargs)
        return self._make_request('PUT',
                                  '%s/%s' % (self.ROOT, zone),
                                  body=body,
                                  callback=callback,
                                  errback=errback)

    def update(self, zone, callback=None, errback=None, **kwargs):
        body = self._buildBody(zone, **kwargs)
        return self._make_request('POST',
                                  '%s/%s' % (self.ROOT, zone),
                                  body=body,
                                  callback=callback,
                                  errback=errback)

    def delete(self, zone, callback=None, errback=None):
        return self._make_request('DELETE', '%s/%s' % (self.ROOT, zone),
                                  callback=callback,
                                  errback=errback)

    def list(self, callback=None, errback=None):
        return self._make_request('GET', '%s' % self.ROOT,
                                  callback=callback,
                                  errback=errback)

    def retrieve(self, zone, callback=None, errback=None):
        return self._make_request('GET', '%s/%s' % (self.ROOT, zone),
                                  callback=callback,
                                  errback=errback)

    def search(self, zone, q=None, has_geo=False, callback=None, errback=None):
        params = {}
        if q is not None:
            params['q'] = q
        if has_geo:
            params['geo'] = has_geo
        return self._make_request('GET', '%s/zone/%s' % (self.SEARCH_ROOT, zone),
                                  params=params,
                                  callback=callback,
                                  errback=errback)
