from django.http import JsonResponse

def response_json(status:bool, code, message:str=None, data:any=None, title=None, url=None):
    if not message:
        message = "Successfully"

    if not status:
        message = f"Failed : {message if message != 'Successfully' else 'Failed'}"
    
    return {
        'status': status,
        'code': code,
        'title': title,
        'message': message,
        'redirect': url,
        'data': data if data else None
    }
    
def response_frontend(status:bool, code, message:str=None, data:any=None, title=None, url=None):
    if not message:
        message = "Successfully"
    
    if not status:
        message = f"Failed : {message if message != 'Successfully' else 'Failed'}"
    
    return JsonResponse({
        'status': status,
        'code': code,
        'title': title,
        'message': message,
        'redirect': url,
        'data': data if data else None
    })
    
def get_url_name(url):
    from urllib.parse import urlparse
    
    parsed_url = urlparse(url)
    path = parsed_url.path
    path_parts = path.split('/')
    
    if len(path_parts) > 1:
        return path_parts[-1]
    
    return None