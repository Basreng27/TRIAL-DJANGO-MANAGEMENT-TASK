def response_json(status:bool, code, message:str=None, data:any=None, title=None, url=None):
    if not message:
        message = "Successfully"
    
    if not status:
        message = f"Failed : {message}"
    
    return {
        'status': status,
        'code': code,
        'title': title,
        'message': message,
        'redirect': url,
        'data': data if data else None
    }