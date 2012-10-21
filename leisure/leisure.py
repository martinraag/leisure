import urllib
import urllib2

from util import HTTP_METHODS, RequestWithMethod

class Resource(object):
    """Single REST API resource"""
    
    def __init__(self, resource, auth=None):
        self._resource = resource
        self._auth = auth
            
    def _prep_query(self, query):
        """Prepare request query string"""
        
        query = {} if not query else query
        if self._auth:
            auth_query = self._auth.get_query()
            if auth_query:
                query.update(auth_query)
        return urllib.urlencode(query)
    
    def _prep_headers(self, headers):
        """Prepare request headers"""
        
        headers = {} if not headers else headers
        if self._auth:
            auth_headers = self._auth.get_headers()
            if auth_headers:
                headers.update(auth_headers)
        return headers
    
    def _prep_data(self, data):
        """Prepare request body"""
        
        return data
            
    def _request(self, method, query=None, data=None, headers=None):
        assert method in HTTP_METHODS
        
        query = self._prep_query(query)
        headers = self._prep_headers(headers)
        data = self._prep_data(data)
        
        request = RequestWithMethod(self._resource + '?' + query, data, 
                                    headers, method=method)
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
        # If uri ends with '/' then add trailing '/'to all resources
        self._trail = '/' if uri[-1] == '/' else ''
        
    def __getattr__(self, name):
        try:
            return self.__getattribute__(name)
        except AttributeError:
            return self._resource(self._uri + '/' + name + self._trail, self._auth)