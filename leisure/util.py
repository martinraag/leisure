import urllib2

HTTP_METHODS = ('OPTIONS', 'GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE',
                'CONNECT')

class RequestWithMethod(urllib2.Request):
    """Allow more then GET and POST methods with urllib2"""
    
    def __init__(self, *args, **kwargs):
        self._method = kwargs.pop('method', None)
        assert self._method in HTTP_METHODS
        urllib2.Request.__init__(self, *args, **kwargs)

    def get_method(self):
        if self._method:
            return self._method
        else:
            return urllib2.Request.get_method(self)