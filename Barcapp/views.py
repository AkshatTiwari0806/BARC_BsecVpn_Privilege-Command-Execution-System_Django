import os
import json
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

commands_file_path = os.path.join(settings.BASE_DIR, 'Barcapp', 'commands.json')
with open(commands_file_path) as json_file:
    data = json.load(json_file)


def token_required(view_func):
    def wrapper(request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION')
        if token == settings.ACCESS_TOKEN:
            return view_func(request, *args, **kwargs)
        else:
            return JsonResponse({"success": "FALSE", "message": "Incorrect token", "status_code": 401})
    return wrapper

@csrf_exempt
@token_required
def add_user(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            if username is None:
                return JsonResponse({"success": "FALSE", "message": "Missing 'username' parameter", "status_code": 400})
            for command in data[0]:
                if command['name'] == request.path and len(username) <= command['parameters'][0]['length'] and isinstance(username, str) == True:
                    output = execute_command(command['mapped_command'])
                    print(output)
                    if output['status_code'] == 0:
                        return JsonResponse({"success": "TRUE", "message": output['output'], "status_code": 200})
                    else:
                        return JsonResponse({"success": "FALSE", "message": output['error'], "status_code": 500})
            return JsonResponse({"success": "FALSE", "message": "Invalid command", "status_code": 400})
        else:
            return JsonResponse({"success": "FALSE", "message": "Invalid request method", "status_code": 400})
    except:
        return JsonResponse({"Message": "Something went wrong"})

@csrf_exempt
@token_required
def add_email(request):
    if request.method == 'POST':
        useremail = request.POST.get('useremail')
        if useremail is None:
            return JsonResponse({"success": "FALSE", "message": "Missing 'user-email' parameter", "status_code": 400})
        for command in data[1]:
            if command['name'] == request.path and len(useremail) <= command['parameters'][0]['length'] and isinstance(useremail, str) == True:
                output = execute_command(command['mapped_command'])
                print(output)
                if output['status_code'] == 0:
                    return JsonResponse({"success": "TRUE", "message": output['output'], "status_code": 200})
                else:
                    return JsonResponse({"success": "FALSE", "message": output['error'], "status_code": 500})
            return JsonResponse({"success": "FALSE", "message": "Invalid command", "status_code": 400})
    else:
        return JsonResponse({"success": "FALSE", "message": "Invalid request method", "status_code": 400})

    

@csrf_exempt
@token_required
def add_password(request):
    try:
        if request.method == 'POST':
            userpassword = request.POST.get('userpassword')
            if userpassword is None:
                return JsonResponse({"success": "FALSE", "message": "Missing 'password' parameter", "status_code": 400})
            for command in data[2]:
                if command['name'] == request.path and len(userpassword) <= command['parameters'][0]['length'] and isinstance(userpassword, str) == True:
                    output = execute_command(command['mapped_command'])
                    print(output)
                    if output['status_code'] == 0:
                        return JsonResponse({"success": "TRUE", "message": output['output'], "status_code": 200})
                    else:
                        return JsonResponse({"success": "FALSE", "message": output['error'], "status_code": 500})
            return JsonResponse({"success": "FALSE", "message": "Invalid command", "status_code": 400})
        else:
            return JsonResponse({"success": "FALSE", "message": "Invalid request method", "status_code": 400})
    except:
        return JsonResponse({"Message": "Something went wrong"})
    

def execute_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return {
        'output': output.decode('utf-8'),
        'error': error.decode('utf-8'),
        'status_code': process.returncode
    }


