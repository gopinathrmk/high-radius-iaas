import requests


# For token-based authentication, omit user and password (so that they default to None), and add the following header to
# the headers list: 'Authorization': 'Bearer <token value>'
def process_request(url, method, user=None, password=None, headers=None, payload=None, files=None, secure=False):

    """
    Processes a web request and handles result appropriately with retries.
    Returns the content of the web request if successfull.
    """
    if payload is not None:
        payload = json.dumps(payload)

    #configuring web request behavior
    timeout=10
    retries = 5
    sleep_between_retries = 5

    while retries > 0:
        try:

            if method is 'GET':
                response = requests.get(
                    url,
                    headers=headers,
                    auth=(user, password) if user else None,
                    verify=secure,
                    timeout=timeout,
                    files=files
                )
            elif method is 'POST':
                response = requests.post(
                    url,
                    headers=headers,
                    data=payload,
                    auth=(user, password) if user else None,
                    verify=secure,
                    timeout=timeout,
                    files=files
                )
            elif method is 'PUT':
                response = requests.put(
                    url,
                    headers=headers,
                    data=payload,
                    auth=(user, password) if user else None,
                    verify=secure,
                    timeout=timeout,
                    files=files
                )
            elif method is 'PATCH':
                response = requests.patch(
                    url,
                    headers=headers,
                    data=payload,
                    auth=(user, password) if user else None,
                    verify=secure,
                    timeout=timeout,
                    files=files
                )
            elif method is 'DELETE':
                response = requests.delete(
                    url,
                    headers=headers,
                    data=payload,
                    auth=(user, password) if user else None,
                    verify=secure,
                    timeout=timeout,
                    files=files
                )

        except requests.exceptions.HTTPError as error_code:
            print ("Http Error!")
            print("status code: {}".format(response.status_code))
            print("reason: {}".format(response.reason))
            print("text: {}".format(response.text))
            print("elapsed: {}".format(response.elapsed))
            #print("headers: {}".format(response.headers))
            #if payload is not None:
            #    print("payload: {}".format(payload))
            print(json.dumps(
                json.loads(response.content),
                indent=4
            ))
            exit(response.status_code)
        except requests.exceptions.ConnectionError as error_code:
            print ("Connection Error!")
            if retries == 1:
                print('Error: {c}, Message: {m}'.format(c = type(error_code).__name__, m = str(error_code)))
                exit(1)
            else:
                print('Error: {c}, Message: {m}'.format(c = type(error_code).__name__, m = str(error_code)))
                sleep(sleep_between_retries)
                retries -= 1
                print ("retries left: {}".format(retries))
                continue
            print('Error: {c}, Message: {m}'.format(c = type(error_code).__name__, m = str(error_code)))
            exit(1)
        except requests.exceptions.Timeout as error_code:
            print ("Timeout Error!")
            if retries == 1:
                print('Error: {c}, Message: {m}'.format(c = type(error_code).__name__, m = str(error_code)))
                exit(1)
            print('Error! Code: {c}, Message: {m}'.format(c = type(error_code).__name__, m = str(error_code)))
            sleep(sleep_between_retries)
            retries -= 1
            print ("retries left: {}".format(retries))
            continue
        except requests.exceptions.RequestException as error_code:
            print ("Error!")
            exit(response.status_code)
        break

    if response.ok:
        return response
    if response.status_code == 401:
        print("status code: {0}".format(response.status_code))
        print("reason: {0}".format(response.reason))
        exit(response.status_code)
    elif response.status_code == 500:
        print("status code: {0}".format(response.status_code))
        print("reason: {0}".format(response.reason))
        print("text: {0}".format(response.text))
        exit(response.status_code)
    else:
        print("Request failed!")
        print("status code: {0}".format(response.status_code))
        print("reason: {0}".format(response.reason))
        print("text: {0}".format(response.text))
        print("raise_for_status: {0}".format(response.raise_for_status()))
        print("elapsed: {0}".format(response.elapsed))
        print("headers: {0}".format(response.headers))
        if payload is not None:
            print("payload: {0}".format(payload))
        print(json.dumps(
            json.loads(response.content),
            indent=4
        ))
        exit(response.status_code)


def bitbucket_push_files(bitbucket_api_endpoint,username,token,respository,files_to_add_modify=[],files_to_delete=[],branch=None,message=None,author=None,secure=False):

    """pushes some files additions/changes/deltions to a given respository

    Args:
        bitbucket_api_endpoint: example: https://api.bitbucket.org/2.0/
        username: bitbucket user name.
        token: bitbucket token.
        respository: target repository name
        files_to_add_modify: list of files to add/modify with contents. example:
            [
                {
                    "path": "dir1/test1.txt"              ---> path inside the repository. "files" string should never be used as path as it marks files for deletion
                    "content": "file contents string"     ---> contents of new/modified file, can be multiline string
                },
                ...
            ]
        files_to_delete: list of files to delete. example:
            [
                "dir1/test1.txt",       ---> path inside the repository
                "dir2/dir3/test2.txt",  ---> path inside the repository
                ...
            ]
        branch: target branch for the commit. will be the main if omitted
        message: commit message. a default message is inserted if omitted
        author: author of the commit in the form 'John Doe <john.doe@example.com>'. request will fail if the format is not respected
                the token name will be taken as author if omitted
        secure: boolean to verify or not the api server's certificate (True/False) 

    Returns:
        No value returned
    """

    if not bitbucket_api_endpoint.endswith('/'):
        bitbucket_api_endpoint += '/'
    url = '{}repositories/{}/{}/src'.format(bitbucket_api_endpoint, username, respository)
    headers = {
        'Accept': 'application/json',
        'Authorization' : 'Bearer {}'.format(token)
    }
    files = []
    #files to add/modify
    files.extend(
        [
            (file["path"], (None, file["content"])) for file in files_to_add_modify
        ]
    )
    #files to delete
    files.extend(
        [
            ('files', (None, filepath)) for filepath in files_to_delete
        ]
    )
    if branch:
        files.extend(
            [
                ('branch', (None, branch))
            ]
        )
    if message:
        files.extend(
            [
                ('message', (None, message))
            ]
        )
    if author:
        files.extend(
            [
                ('author', (None, author))
            ]
        )

    r = process_request(url=url, method='POST', files=files, headers=headers,secure=secure)
    if r.ok:
        print("Changes commited successfully")
    else:
        print("ERROR - Failed to commit changes. details:\n\n")
        print(r.text)
        exit(1)
    

def bitbucket_files_test_example():

    bitbucket_push_files(bitbucket_api_endpoint='https://api.bitbucket.org/2.0',
                         username="nxmna",
                         token='xxxxxxxxxx',
                         respository="mna-test-repo",
                         files_to_add_modify=[
                            {
                                "path": "dir3/test1.txt",
                                "content": "test1.txt contents are here\nbla bla bla",
                            },
                            {
                                "path": "dir2/dir4/test2.txt",
                                "content": "test2.txt contents are here\nbla bla bla",
                            }
                         ],
                         files_to_delete=[
                             "dir1/test1.txt",
                             "test.txt"
                         ],
                         branch="feat-xxx",
                         message="this is a commit",
                         author='John Doe <john.doe@example.com>',
                         secure=True)
