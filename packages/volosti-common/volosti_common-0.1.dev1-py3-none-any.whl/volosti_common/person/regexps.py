from re import compile

RAW_PASSWORD = compile(r'^[ -~]+$')
USERNAME = compile(r'^[A-Za-z0-9-._]+$')
