import urllib2

class Auth(object):
    
    def init(self, api):
        """Called after API __init__ method. 
        API object passes a reference to itself."""

        self._api = api
        
    def process_args(self, args):
        """Modify URL arguments before creating request object"""
        
        return args
    
    def process_request(self, request):
        """Modify urllib2 Request before sending"""
        
        return request
    
    def on_error(self, error):
        """Called on HTTP error 401"""
        
        raise error
        
class BasicAuth(Auth):
    
    def __init__(self, username, password):
        """Save username and password"""
        
        self._username = username
        self._password = password
    
    def init(self, api):
        self._setup(api._uri)

    def _setup(self, uri):        
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, uri, self._username, self._password)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(opener)

class APIKeyAuth(Auth):
    
    def __init__(self, **kwargs):
        """Save all keyword arguments"""

        self._args = kwargs
        
    def process_args(self, args):
        """Add all objects in self._args to request url"""
        
        args.update(self._args)
        return args