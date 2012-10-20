import urllib2

class Auth(object):
    
    def init(self):
        """Called after API __init__ method"""
    
    def process_args(self, args):
        """Modify URL arguments (query string)"""
    
    def process_data(self, data):
        """Modify request data"""
    
    def on_error(self, error):
        """Called on HTTP error 401"""
        
        raise error
        
class BasicAuth(Auth):
    
    def __init__(self, username, password):
        """Save username and password"""
        
        self._username = username
        self._password = password
    
    def init(self, api):
        self._setup(api._resource)

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