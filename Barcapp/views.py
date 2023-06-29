import os
import json
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

@csrf_exempt
def add_user(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            print(request.path)
            if username is None:
                return JsonResponse({"status": "failure", "message": "Missing 'username' parameter", "status_code": 400})
            commands_file_path = os.path.join(settings.BASE_DIR, 'Barcapp', 'commands.json')
            with open(commands_file_path) as json_file:
                data = json.load(json_file)
                for command in data[0]:
                    if command['name'] == request.path and len(username) <= command['parameters'][0]['length'] and isinstance(username, str) == True:
                        output = execute_command(command['mapped_command'])
                        print(output)
                        if output['status_code'] == 0:
                            return JsonResponse({"status": "success", "message": output['output'], "status_code": 200})
                        else:
                            return JsonResponse({"status": "failure", "message": output['error'], "status_code": 500})
            return JsonResponse({"status": "failure", "message": "Invalid command", "status_code": 400})
        else:
            return JsonResponse({"status": "failure", "message": "Invalid request method", "status_code": 400})
    except:
        return JsonResponse({"Message": "Something went wrong"})

@csrf_exempt
def add_email(request):
    try:
        if request.method == 'POST':
            useremail = request.POST.get('useremail')
            print(request.path)
            if useremail is None:
                return JsonResponse({"status": "failure", "message": "Missing 'user-email' parameter", "status_code": 400})
            commands_file_path = os.path.join(settings.BASE_DIR, 'Barcapp', 'commands.json')
            with open(commands_file_path) as json_file:
                data = json.load(json_file)
                for command in data[1]:
                    if command['name'] == request.path and len(useremail) <= command['parameters'][0]['length'] and isinstance(useremail, str) == True:
                        output = execute_command(command['mapped_command'])
                        print(output)
                        if output['status_code'] == 0:
                            return JsonResponse({"status": "success", "message": output['output'], "status_code": 200})
                        else:
                            return JsonResponse({"status": "failure", "message": output['error'], "status_code": 500})
            return JsonResponse({"status": "failure", "message": "Invalid command", "status_code": 400})
        else:
            return JsonResponse({"status": "failure", "message": "Invalid request method", "status_code": 400})
    except:
        return JsonResponse({"Message": "Something went wrong"})
    

@csrf_exempt
def add_password(request):
    try:
        if request.method == 'POST':
            userpassword = request.POST.get('userpassword')
            print(request.path)
            if userpassword is None:
                return JsonResponse({"status": "failure", "message": "Missing 'password' parameter", "status_code": 400})
            commands_file_path = os.path.join(settings.BASE_DIR, 'Barcapp', 'commands.json')
            with open(commands_file_path) as json_file:
                data = json.load(json_file)
                for command in data[2]:
                    if command['name'] == request.path and len(userpassword) <= command['parameters'][0]['length'] and isinstance(userpassword, str) == True:
                        output = execute_command(command['mapped_command'])
                        print(output)
                        if output['status_code'] == 0:
                            return JsonResponse({"status": "success", "message": output['output'], "status_code": 200})
                        else:
                            return JsonResponse({"status": "failure", "message": output['error'], "status_code": 500})
            return JsonResponse({"status": "failure", "message": "Invalid command", "status_code": 400})
        else:
            return JsonResponse({"status": "failure", "message": "Invalid request method", "status_code": 400})
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


