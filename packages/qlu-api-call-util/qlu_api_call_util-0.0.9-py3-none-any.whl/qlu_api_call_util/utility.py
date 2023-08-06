import enum
from urllib.parse import urlparse

ALLOWED_METHODS = ['get', 'post', 'put', 'patch', 'delete']

class SingleCallMethodCode(enum.Enum):
    NO_ERROR = 0
    ERROR_URL = -1
    ERROR_WRONG_PARAM_DICT = -2
    ERROR_WRONG_DURATION_PARAM = -3
    ERROR_REQ_FAILED = -4

class MultiCallMethodCode(enum.Enum):
    NO_ERROR = 0
    ERROR_URL_PARAM = -21
    ERROR_METHOD_PARAM = -22
    ERROR_RETRIES_PARAM = -23
    ERROR_DURATION_BEFORE_RETRY_PARAM = -24
    ERROR_DATA_DICT_PARAM = -25,
    ERROR_HEADER_DICT_PARAM = -26


def is_url(url):
  try:
    result = urlparse(url)
    return all([result.scheme, result.netloc])
  except ValueError:
    return False
  
def is_allowed_method(method):
    if type(method).__name__=='str' and method.lower() in ALLOWED_METHODS:
        return True
    return False

def create_url_for_get_query(url, data_dict):
    if not data_dict == None:
        url += '?'
        for key, value in data_dict.items():
            url += (str(key) + '=' + str(value) + '&')
        url = url[:-1]
    return url

def generate_retry_duration_list(retries, duration_before_retry):
    len_dur_lst = len(duration_before_retry)
    if retries == len_dur_lst:    
        return duration_before_retry    
    elif retries > len_dur_lst:
        last_element = duration_before_retry[-1]
        repetitions = retries - len_dur_lst
        duration_before_retry.extend([last_element] * repetitions)
    elif retries < len_dur_lst:
        duration_before_retry = duration_before_retry[0:retries]
    return duration_before_retry