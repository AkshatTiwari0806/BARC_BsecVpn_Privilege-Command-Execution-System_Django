

import os
import json
import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

@csrf_exempt
def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if username is None:
            return JsonResponse({"status": "failure", "message": "Missing 'username' parameter", "status_code": 400})
        commands_file_path = os.path.join(settings.BASE_DIR, 'Barcapp', 'commands.json')
        with open(commands_file_path) as json_file:
            data = json.load(json_file)
            for command in data:
                if command['name'] == 'add_user' and len(username) <= command['parameters'][0]['length']:
                    process = subprocess.Popen(command['mapped_command'], stdout=subprocess.PIPE, shell=True)
                    output, error = process.communicate()
                    if process.returncode == 0:
                        return JsonResponse({"status": "success", "message": output.decode('utf-8'), "status_code": 200})
                    else:
                        return JsonResponse({"status": "failure", "message": error.decode('utf-8'), "status_code": 500})
        return JsonResponse({"status": "failure", "message": "Invalid command", "status_code": 400})
    else:
        return JsonResponse({"status": "failure", "message": "Invalid request method", "status_code": 400})
