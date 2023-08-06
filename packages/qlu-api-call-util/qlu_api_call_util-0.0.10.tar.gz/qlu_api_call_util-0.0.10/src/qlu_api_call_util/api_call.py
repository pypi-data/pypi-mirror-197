import json
import asyncio
import aiohttp
from urllib.parse import urlparse
from multiprocessing.pool import ThreadPool
from .utility import is_url, is_allowed_method, create_url_for_get_query, generate_retry_duration_list, ALLOWED_METHODS, SingleCallMethodCode, MultiCallMethodCode

async def make_api_request_async(url, data_dict=None, header_dict={'Content-Type': 'application/json'}, method='POST', retries=3, duration_before_retry=[1], verbose=False, is_resp_json=True, session_timeout=300, request_timeout=300):
    if verbose:
        print("API called")
    if not is_url(url):
        return {
            'statusCode': SingleCallMethodCode.ERROR_URL.value
        }
    
    if data_dict != None and not type(data_dict).__name__ == 'dict':
        return {
            'statusCode': SingleCallMethodCode.ERROR_WRONG_PARAM_DICT.value
        }
    
    if not type(duration_before_retry).__name__ == 'list' or len(duration_before_retry)==0 or not all(isinstance(x, int) for x in duration_before_retry):
        return {
            'statusCode': SingleCallMethodCode.ERROR_WRONG_DURATION_PARAM.value
        }
    
    duration_before_retry = generate_retry_duration_list(retries=retries, duration_before_retry=duration_before_retry)
        
    if method == "GET":
        url = create_url_for_get_query(url=url, data_dict=data_dict)

    elif method == "POST":
        data_dict = json.dumps(data_dict)

    elif method == "PUT":
        data_dict = json.dumps(data_dict)

    elif method == "PATCH":
        data_dict = json.dumps(data_dict)

    elif method == "DELETE":
        pass

    
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
    #initiate a http session. Retry it N number of times if connection not previously established
        for i in range(retries):
            try:
                #request a session using given method, url and data_dict if any
                async with session.request(method, url, data=data_dict, headers=header_dict, timeout=request_timeout) as response:
                    if verbose:
                        print(response.status)
                    #response 
                    if response.status == 200:
                        #json_resp = await response.json()
                        if verbose:
                            print("API Finished")
                        if is_resp_json:
                            return {
                                'statusCode': SingleCallMethodCode.NO_ERROR.value,
                                'methodCode': response.status,
                                'data': await response.json(content_type=None)
                            }
                        else:
                            return {
                                'statusCode': SingleCallMethodCode.NO_ERROR.value,
                                'methodCode': response.status,
                                'data': await response.text()
                            }
                        # return await response.json()
                    else:
                        response_text = await response.text()
                        print(f"API {url} request failed with status {response.status}: {response_text}")
            except aiohttp.ClientError as e:
                if verbose:
                    print(f"API: {url} request failed with error: {e}")
            if verbose:
                print(f'Waiting {duration_before_retry[i]} second before retrying API call {url}')
            await asyncio.sleep(duration_before_retry[i])  # Wait N seconds before retrying
        if verbose:
            print(f"API: {url} request failed after {retries} retries.")
        return {
            'statusCode': SingleCallMethodCode.ERROR_REQ_FAILED.value,
            'methodCode': response.status
        }
    
async def make_multiple_api_requests_async(urls_lst=[], data_dicts_lst=[], header_dicts_lst=[{'Content-Type': 'application/json'}], methods_lst=[], retries_lst=[1], duration_before_retry_lst=[[1]], verbose=False, is_resp_json_lst=[], session_timeout=300, request_timeout=300):
    if not type(urls_lst).__name__ == 'list' or not all([is_url(url) for url in urls_lst]):
        return {
                'statusCode': MultiCallMethodCode.ERROR_URL_PARAM.value
        } 
       
    if not type(methods_lst).__name__ == 'list' or not all([is_allowed_method(method) for method in ALLOWED_METHODS]): 
        return {
                'statusCode': MultiCallMethodCode.ERROR_METHOD_PARAM.value
        } 
       
    if not type(retries_lst).__name__ == 'list':
        return {
                'statusCode': MultiCallMethodCode.ERROR_RETRIES_PARAM.value
        } 
       
    if not type(duration_before_retry_lst).__name__ == 'list':
        return {
                'statusCode': MultiCallMethodCode.ERROR_DURATION_BEFORE_RETRY_PARAM.value
        } 
       
    if not type(data_dicts_lst).__name__ == 'list':
        return {
            'statusCode': MultiCallMethodCode.ERROR_DATA_DICT_PARAM.value
        } 
    
    if not type(header_dicts_lst).__name__ == 'list':
        return {
            'statusCode': MultiCallMethodCode.ERROR_HEADER_DICT_PARAM.value
        } 
    
    api_job_lsts = []
    for idx, url in enumerate(urls_lst):
        api_job_lsts.append(make_api_request_async(url=url, method=methods_lst[idx], retries=retries_lst[idx], duration_before_retry=duration_before_retry_lst[idx], data_dict=data_dicts_lst[idx], header_dict=header_dicts_lst[idx], verbose=verbose, is_resp_json=is_resp_json_lst[idx], session_timeout=session_timeout, request_timeout=request_timeout))
    api_responses = await asyncio.gather(*api_job_lsts)
    return api_responses

def create_task_api_request_call(url, data_dict=None, header_dict={'Content-Type': 'application/json'}, method='POST', retries=3, duration_before_retry=[1,2,3], verbose=False, session_timeout=300, request_timeout=300):
    return asyncio.create_task(make_api_request_async(url=url, method=method, retries=retries, duration_before_retry=duration_before_retry, data_dict=data_dict, header_dict=header_dict, verbose=verbose, session_timeout=session_timeout, request_timeout=request_timeout))

def create_task_mult_api_request_call(urls_lst=[], data_dicts_lst=[], header_dicts_lst=[{'Content-Type': 'application/json'}], methods_lst=[], retries_lst=[1], duration_before_retry_lst=[[1]], verbose=False, session_timeout=300, request_timeout=300):
    return asyncio.create_task(make_multiple_api_requests_async(urls_lst=urls_lst, data_dicts_lst=data_dicts_lst, header_dicts_lst=header_dicts_lst, methods_lst=methods_lst, retries_lst=retries_lst, duration_before_retry_lst=duration_before_retry_lst, verbose=verbose, is_resp_json_lst=[], session_timeout=session_timeout, request_timeout=request_timeout))


# PRE-BUILT METHODS DEVELOPED FOR CUSTOM NEED
async def make_post_api_request_async(url, data_dict=None, header_dict={'Content-Type': 'application/json'}, method='POST', retries=3, duration_before_retry=[1,2,3], verbose=False, is_resp_json=True, session_timeout=300, request_timeout=300):
    if verbose:
        print("API called")
    if not is_url(url):
        return {
            'statusCode': SingleCallMethodCode.ERROR_URL.value
        }
    
    if data_dict != None and not type(data_dict).__name__ == 'dict':
        return {
            'statusCode': SingleCallMethodCode.ERROR_WRONG_PARAM_DICT.value
        }
    
    if not type(duration_before_retry).__name__ == 'list' or len(duration_before_retry)==0 or not all(isinstance(x, int) for x in duration_before_retry):
        return {
            'statusCode': SingleCallMethodCode.ERROR_WRONG_DURATION_PARAM.value
        }
    
    duration_before_retry = generate_retry_duration_list(retries=retries, duration_before_retry=duration_before_retry)
        
    if method == "GET":
        url = create_url_for_get_query(url=url, data_dict=data_dict)

    elif method == "POST":
        data_dict = json.dumps(data_dict)

    elif method == "PUT":
        data_dict = json.dumps(data_dict)

    elif method == "PATCH":
        data_dict = json.dumps(data_dict)

    elif method == "DELETE":
        pass

    
    async with aiohttp.ClientSession(timeout=session_timeout) as session:
    #initiate a http session. Retry it N number of times if connection not previously established
        for i in range(retries):
            try:
                #request a session using given method, url and data_dict if any
                async with session.request(method, url, data=data_dict, headers=header_dict, timeout=request_timeout) as response:
                    if verbose:
                        print(response.status)
                    #response 
                    if response.status == 200:
                        #json_resp = await response.json()
                        if verbose:
                            print("API Finished")
                        if is_resp_json:
                            return {
                                'statusCode': SingleCallMethodCode.NO_ERROR.value,
                                'methodCode': response.status,
                                'data': await response.json(content_type=None)
                            }
                        else:
                            return {
                                'statusCode': SingleCallMethodCode.NO_ERROR.value,
                                'methodCode': response.status,
                                'data': await response.text()
                            }
                        # return await response.json()
                    else:
                        response_text = await response.text()
                        print(f"API {url} request failed with status {response.status}: {response_text}")
            except aiohttp.ClientError as e:
                if verbose:
                    print(f"API: {url} request failed with error: {e}")
            if verbose:
                print(f'Waiting {duration_before_retry[i]} second before retrying API call {url}')
            await asyncio.sleep(duration_before_retry[i])  # Wait N seconds before retrying
        if verbose:
            print(f"API: {url} request failed after {retries} retries.")
        return {
            'statusCode': SingleCallMethodCode.ERROR_REQ_FAILED.value,
            'methodCode': response.status
        }
    
def create_task_post_api_request_call(url, data_dict=None, header_dict={'Content-Type': 'application/json'}, retries=3, duration_before_retry=[1,2,3], verbose=False, is_resp_json=True):
    return asyncio.create_task(make_post_api_request_async(url=url, retries=retries, duration_before_retry=duration_before_retry, data_dict=data_dict, header_dict=header_dict, verbose=verbose))

def create_async_post_request(url, data_dict=None, header_dict={'Content-Type': 'application/json'}, retries=3, duration_before_retry=[1,2,3], verbose=False, is_resp_json=False, session_timeout=300, request_timeout=300):
    pool = ThreadPool(processes=1)
    TASK = make_api_request_async(url, data_dict=data_dict, header_dict=header_dict, retries=retries, duration_before_retry=duration_before_retry, verbose=False, is_resp_json=is_resp_json, session_timeout=session_timeout, request_timeout=request_timeout)
    async_call = pool.apply_async(asyncio.run, (TASK,))
    return async_call

def create_async_request(url, data_dict=None, header_dict={'Content-Type': 'application/json'}, method='POST', retries=3, duration_before_retry=[1,2,3], verbose=False, is_resp_json=False, session_timeout=300, request_timeout=300):
    pool = ThreadPool(processes=1)
    TASK = make_api_request_async(url, data_dict=data_dict, header_dict=header_dict, method=method, retries=retries, duration_before_retry=duration_before_retry, verbose=False, is_resp_json=is_resp_json, session_timeout=session_timeout, request_timeout=request_timeout)
    async_call = pool.apply_async(asyncio.run, (TASK,))
    return async_call