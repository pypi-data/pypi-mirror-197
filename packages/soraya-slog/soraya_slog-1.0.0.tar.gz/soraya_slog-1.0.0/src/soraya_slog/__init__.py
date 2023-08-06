import json
from datetime import datetime

LOG_SEVERITY_DEBUG = 'DEBUG'
LOG_SEVERITY_INFO = 'INFO'
LOG_SEVERITY_NOTICE = 'NOTICE'
LOG_SEVERITY_WARNING = 'WARNING'
LOG_SEVERITY_ERROR = 'ERROR'
LOG_SEVERITY_CRITICAL = 'CRITICAL'
LOG_SEVERITY_ALERT = 'ALERT'
LOG_SEVERITY_EMERGENCY = 'EMERGENCY'

def __get_timestamp() -> str:
  return datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

def __log(severity: str, message: str, data: object = None) -> None:
  entry = { 'timestamp': __get_timestamp(),
            'severity': severity,
            'message': message }
  if (data != None):
    entry['data'] = data
  print(json.dumps(entry))

def log(severity: str, message: str, data: object = None) -> None:
  try:
    return __log(severity, message, data)
  except Exception as e:
    print(f'{{'
          f' "timestamp": "{__get_timestamp()}",'
          f' "severity": "{LOG_SEVERITY_CRITICAL}",'
          f' "message": "Error while attempting to log message: {str(e)}",'
          f'}}')

def debug(message: str, data: object = None) -> None:
  return log(LOG_SEVERITY_DEBUG, message, data)

def info(message: str, data: object = None) -> None:
  return log(LOG_SEVERITY_INFO, message, data)

def notice(message: str, data: object = None) -> None:
  return log(LOG_SEVERITY_NOTICE, message, data)

def warning(message: str, data: object = None) -> None:
  return log(LOG_SEVERITY_WARNING, message, data)

def error(message: str, data: object = None) -> None:
  return log(LOG_SEVERITY_ERROR, message, data)

def critical(message: str, data: object = None) -> None:
  return log(LOG_SEVERITY_CRITICAL, message, data)

def alert(message: str, data: object = None) -> None:
  return log(LOG_SEVERITY_ALERT, message, data)

def emergency(message: str, data: object = None) -> None:
  return log(LOG_SEVERITY_EMERGENCY, message, data)