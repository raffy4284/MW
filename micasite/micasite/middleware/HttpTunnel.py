from django.http import QueryDict
 
class HttpPostTunnelingMiddleware(object):
    def process_request(self, request):
        if request.method.lower() == 'put':
            request.PUT = QueryDict(request.body)
        if request.method.lower() == 'delete':
            request.DELETE = QueryDict(request.body)
        return None
