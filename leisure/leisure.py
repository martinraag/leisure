import urllib
import urllib2

from util import RequestWithMethod

class Resource(object):
    """Single REST API resource"""
    
    def __init__(self, resource, auth=None):
        self._resource = resource
        self._auth = auth
            
    def _request(self, method, args=None, data=None):
        assert method in ('GET', 'POST', 'PUT', 'DELETE')
        args = {} if not args else args
        if self._auth:
            args = self._auth.process_args(args)
            data = self._auth.process_data(data)
        request = RequestWithMethod(self._resource + '?' + urllib.urlencode(args),
                                    data, method=method)
        try:
            pagehandle = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            if self._auth and e.code == 401:
                self._auth.on_error(e)
            else:
                raise
        code, data = pagehandle.getcode(), pagehandle.read()
        return (code, data)
    
    def get(self, **kwargs):
        return self._request('GET', kwargs)
        
    def post(self, **kwargs):
        data = kwargs.pop('data', None)
        return self._request('POST', kwargs, data)
    
    def put(self, **kwargs):
        data = kwargs.pop('data', None)
        return self._request('PUT', kwargs, data)
    
    def delete(self, **kwargs):
        data = kwargs.pop('data', None)
        return self._request('DELETE', kwargs, data)
        
    def __getattr__(self, name):
        try:
            return self.__getattribute__(name)
        except AttributeError:
            self._resource += '/%s' % name
            return self

class API(object):
    
    _resource = Resource
    
    def __init__(self, uri, auth=None):
        self._uri = uri
        self._auth = auth
        self._trail = '/' if uri[:1] == '/' else ''
        
    def __getattr__(self, name):
        try:
            return self.__getattribute__(name)
        except AttributeError:
            return self._resource(self._uri + '/' + name + self._trail, self._auth)