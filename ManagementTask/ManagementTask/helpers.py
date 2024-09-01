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