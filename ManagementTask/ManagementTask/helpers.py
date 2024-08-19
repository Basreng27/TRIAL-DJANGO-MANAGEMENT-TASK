# from django.http import JsonResponse

def response_json(status:bool, code, message:str=None, data:any=None):
    if not message:
        message = "Successfully"
    
    if not status:
        message = f"Failed : {message}"
    
    return {
        'status': status,
        'code': code,
        'message': message,
        'data': data if data else None
    }