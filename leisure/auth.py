import base64

class Auth(object):
        
    def get_query(self):
        """Return query string to add to request"""
    
    def get_headers(self):
        """Return headers to add to request"""
        
    def on_error(self, error):
        """Called on HTTP error 401"""
        
        raise error
        
class BasicAuth(Auth):
    
    def __init__(self, username, password):
        """Save username and password"""
        
        self._username = username
        self._password = password
        self._encoded = None
        
    @property
    def encoded_cred(self):
        """base64 encode username:password string"""
        
        if not self._encoded:
            self._encoded = base64.b64encode('%s:%s' % (self._username,
                                                        self._password))
        return self._encoded
        
    def get_headers(self):
        """Add Basic Authorization header"""
        
        return {'Authorization': 'Basic %s' % self.encoded_cred}
    
class APIKeyAuth(Auth):
    
    def __init__(self, **kwargs):
        """Save all keyword arguments"""

        self._auth_args = kwargs
        
    def get_query(self):
        """Add all auth_args to query string"""
        
        return self._auth_args