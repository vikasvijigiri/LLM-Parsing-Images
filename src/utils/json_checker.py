import json
is_json = lambda x: isinstance(x, (dict, list)) or isinstance(x, str) and not json.loads(json.dumps(x))
