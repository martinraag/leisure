import urllib2

class RequestWithMethod(urllib2.Request):
    """Use DELETE and PUT with urllib2"""
    
    def __init__(self, *args, **kwargs):
        self._method = kwargs.pop('method', None)
        urllib2.Request.__init__(self, *args, **kwargs)

    def get_method(self):
        if self._method:
            return self._method
        else:
            return urllib2.Request.get_method(self)