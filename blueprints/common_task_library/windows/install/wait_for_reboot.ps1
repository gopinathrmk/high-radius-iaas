# Set WinRM service to Automatic (Delayed) start before doing this to give Windows more time to start.
# Tests if WinRM is up by sending an unauthenticated request for its identity.

### Capture Macros ###

ip_address = "@@{address}@@"

###


### Global Variables ###

method = "POST"
url = "http://{}:5985/wsman".format(ip_address)
headers = {
  'WSMANIDENTIFY': 'unauthenticated',
  'Content-Type': 'application/soap+xml;charset=UTF-8'
}
payload = """
    <s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:wsmid="http://schemas.dmtf.org/wbem/wsman/identity/1/wsmanidentity.xsd">
        <s:Header/>
        <s:Body>
            <wsmid:Identify/>
        </s:Body>
    </s:Envelope>
"""

###


### Functions ###

def process_request(
    url,
    method,
    headers,
    payload=None,
    username=None,
    password=None,
    auth=None
):

    if (payload != None):
        payload = json.dumps(payload)

    if (username != None):
        auth = "BASIC"

    r = urlreq(
            url,
            verb=method,
            auth=auth,
            user=username,
            passwd=password,
            params=payload,
            verify=False,
            headers=headers
        )

    if r.ok:
        try:
            return json.loads(r.content)
        except:
            return r.content
    else:
        print("Request failed")
        print("Status code: {}".format(r.status_code))
        print("Headers: {}".format(headers))
        print("Payload: {}".format(payload))
        print(json.dumps(r, indent=4))
        exit(1)

###


### Wait for VM to go down ###
# Waits 30 minutes

print("Waiting for VM to be inaccessible...")

count = 0
while (count < 360):
    try:
        resp = process_request(url, method, headers, payload)
    except:
        print("VM Down")
        break
    else:
        count = count + 1
        print("Retry...{}".format(count))
        sleep(5)
else:
    print("Failed waiting for VM to reboot!")
    exit(1)

###


### Waits for VM to be up ###
# Waits 30 minutes

print("Waiting for VM to be accessible...")

count = 0
while (count < 30):
    try:
        resp = process_request(url, method, headers, payload)
    except:
        count = count + 1
        print("Retry...{}".format(count))
        sleep(60)
    else:
        print("VM Up")
        break
else:
    print("Failed waiting for VM to reboot!")
    exit(1)

sleep(120)
print("VM is accessible!")

###