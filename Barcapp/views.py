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
            return JsonResponse({"success": "FALSE", "message": "Incorrect Access-token", "status_code": 401})
    return wrapper



def execute_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    return {
        'output': output.decode('utf-8'),
        'error': error.decode('utf-8'),
        'status_code': process.returncode
    }


@csrf_exempt
@token_required
def add_user(request):
    try:
        if request.method == 'POST':

            commands = [item for sublist in data[0] for item in sublist]

            command = next((c for c in commands if c['name'] == request.path), None)
            if command is None:
                return JsonResponse({"success": "FALSE", "message": "Invalid command", "status_code": 400})

            parameters = []
            for param in command['parameters']:
                value = request.POST.get(param['name'])
                if value is None or len(value) > param['length'] or not isinstance(value, str):
                    return JsonResponse({"success": "FALSE", "message": f"Invalid value for parameter '{param['name']}'", "status_code": 400})
                parameters.append(value)

            mapped_command = command['mapped_command'] % tuple(parameters)
            return JsonResponse({"success": "TRUE", "message": mapped_command, "status_code": 200})

        else:
            return JsonResponse({"success": "FALSE", "message": "Invalid request method", "status_code": 400})

    except Exception as e:
        return JsonResponse({"success": "FALSE", "message": "Something went wrong: " + str(e), "status_code": 500})

@csrf_exempt
@token_required
def add_email(request):
    try:
        if request.method == 'POST':
            useremail = request.POST.get('useremail')
            if useremail is None:
                return JsonResponse({"success": "FALSE", "message": "Missing 'email' parameter", "status_code": 400})
            for command in data[8]:
                if len(useremail) <= command['parameters'][0]['length'] and isinstance(useremail, str) == True:
                    output = execute_command(command['mapped_command'])
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
def add_password(request):
    try:
        if request.method == 'POST':
            userpassword = request.POST.get('userpassword')
            if userpassword is None:
                return JsonResponse({"success": "FALSE", "message": "Missing 'password' parameter", "status_code": 400})
            for command in data[9]:
                if len(userpassword) <= command['parameters'][0]['length'] and isinstance(userpassword, str) == True:
                    output = execute_command(command['mapped_command'])
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
def add_userr(request):
    if request.method == 'POST':
        

        command = data[0]

        parameters = command['parameters']

        data = {}

        for param in parameters:
            param_name = param['name']
            param_value = request.POST.get(param_name)

            if param_value is None:
                return JsonResponse({"status": "failure", "message": f"Missing '{param_name}' parameter", "status_code": 400})

            param_length = param['length']
            param_type = param['type']

            if param_type == 'str':
                if not isinstance(param_value, str):
                    return JsonResponse({"status": "failure", "message": f"Invalid '{param_name}' parameter type", "status_code": 400})

                if len(param_value) != param_length:
                    return JsonResponse({"status": "failure", "message": f"Invalid length for '{param_name}' parameter", "status_code": 400})

            data[param_name] = param_value

        mapped_command = command['mapped_command']

        command_args = tuple(data[param['name']] for param in parameters)

        formatted_command = mapped_command % command_args

        output = subprocess.run(formatted_command, shell=True, capture_output=True, text=True)

        if output.returncode == 0:
            return JsonResponse({"status": "success", "message": "Command executed successfully", "status_code": 200, "output": output.stdout})
        else:
            return JsonResponse({"status": "failure", "message": "Command execution failed", "status_code": 500, "output": output.stderr})

    return JsonResponse({"status": "failure", "message": "Invalid request method", "status_code": 400})
