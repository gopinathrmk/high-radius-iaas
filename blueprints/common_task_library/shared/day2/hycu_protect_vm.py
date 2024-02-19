import requests
from datetime import datetime

# Avoid security exceptions/warnings
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

ARRAY_VMNAME = "@@{VM_Provision.name}@@".split(',')

HYCU_ENDPOINT = 'hycu.emeagso.lab'
HYCU_USER = 'admin'
HYCU_SECRET = 'Nutanix/4u!'
BACKUP_VM = "@@{backup_vm}@@"

def huFindItemByValue(items, propName, propValue):
    for key in items:
        if items[key][propName] == propValue:
            return items[key]
    return None

def huRestGeneric(server, username, password, url, timeout, pagesize, returnRaw=False, maxitems=None):
    items = []
    pageNumber = 1
    while True:
        # Prepare the HTTP get request
        if (pagesize == None):
            requestUrl = "https://{}:8443/rest/v1.0/{}".format(server, url)
        else:
            requestUrl = "https://{}:8443/rest/v1.0/{}pageSize={}&pageNumber={}".format(server, url, pagesize, pageNumber)
        response = requests.get(requestUrl,auth=(username,password), cert="",timeout=timeout,verify=False)
        if response.status_code != 200:
            print('Status:', response.status_code, 'Failed to retrieve REST results. Exiting.')
            exit(response.status_code)

        if returnRaw == True:
            return response

        data = response.json()
        items += data['entities']
        pagesize = (data['metadata']['pageSize'])

        # Exit the loop if we retrieved all of the items
        if len(items) == (data['metadata']['totalEntityCount']):
            break
        if (maxitems != None) and maxitems < len(items):
            break
        pageNumber += 1

    return items

def huGetVMs(server, username, password, timeout, pagesize):
    """ Retrieves dictionary of event[uuid] """
    dict = {}
    data = huRestGeneric(server, username, password, 'vms?forceSync=false&',timeout, pagesize)
    for item in data:
        dict[item['uuid']] = item
    return dict

def huGetVGs(server, username, password, timeout, pagesize):
    """ Retrieves dictionary of event[uuid] """
    dict = {}
    data = huRestGeneric(server, username, password, 'volumegroups?forceSync=false&',timeout, pagesize)
    for item in data:
        dict[item['uuid']] = item
    return dict

def huGetJobsForVM(vmUUID, server, username, password, pagesize, timeout):
    """ Returns a list of jobs for selected vmUUID """
    return huRestGeneric(server, username, password, 'vms/{}/backups?'.format(vmUUID), timeout, pagesize)

def huGetJobsForVG(vgUUID, server, username, password, pagesize, timeout):
    """ Returns a list of jobs for selected vgUUID """
    return huRestGeneric(server, username, password, 'volumegroups/{}/backups?'.format(vgUUID), timeout, pagesize)

def huGetLastSuccessfulUUID(backups):
    backup = None
    for item in backups:
        # Select the first item in the list
        if backup == None:
            backup = item
            continue
        if item['status'] == 'OK' and item['restorePointInMillis'] > backup['restorePointInMillis']:
            backup = item
    # If there is no single backup in the list we cannot identify the right target to be used
    if (backup == None):
        print('Status:', 'Cannot find at least one previous backup of the selected VM')
        exit(480)
    return backup['uuid']

def huBackupVm(vmuuid, server, username, password, timeout=5):
    # Prepare the HTTP get request
    data = {
        "uuidList": [
            "{}".format(vmuuid)
        ]
        }
    url = "https://{}:8443/rest/v1.0/schedules/backup".format(server)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*'
    }
    response = requests.post(url,auth=(username,password), cert="", headers=headers, verify=False, json=data, timeout=timeout)
    print('response is {}'.format(response))
    if response.ok:
        data = response.json()
        return data
    if response.status_code not in [200,201,202]:
        print('Status:', response.status_code, 'Failed to trigger a Backup of {}. Exiting.'.format(vmUUID))
        exit(response.status_code)

def huBackupVg(vgUUID, server, username, password, timeout):
    # Prepare the HTTP get request
    options = '{ \
        "uuidList":["{}"] \
    }'.format(vgUUID)

    requestUrl = "https://{}:8443/rest/v1.0/schedules/backupVolumeGroup".format(server)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*'
    }
    response = requests.post(requestUrl,auth=(username,password), cert="", headers=headers, verify=False, data=options, timeout=timeout)
    if response.status_code not in [200,201,202]:
        print('Status:', response.status_code, 'Failed to trigger a Backup of {}. Exiting.'.format(vgUUID))
        exit(response.status_code)

    return response.json()

def huGetJobStatus(server, username, password, jobUuid, timeout):
    """ Retrieves Job status """
    print(jobUuid)
    endpoint = "jobs/{}".format(jobUuid)
    data = huRestGeneric(server, username, password, endpoint, timeout, None)
    return data[0]['status']

def main():
    # REST call intializations
    nTimeout = 5
    pageSize = None

    # Retrieve the list of VMs from HYCU Rest API server (page by page)
    vms = huGetVMs(HYCU_ENDPOINT, HYCU_USER, HYCU_SECRET, timeout=nTimeout, pagesize=pageSize)

    for v in ARRAY_VMNAME:
        # Check if the given VM name is valid
        vm = huFindItemByValue(vms, 'vmName', v)
        if (vm == None):
            print('Status:', 'Cannot find VM "{}" in the list of HYCU VMs'.format(vm))
            exit(1)

        if ('yes' in BACKUP_VM):
            backup_result = huBackupVm(vm['uuid'], HYCU_ENDPOINT, HYCU_USER, HYCU_SECRET, timeout=nTimeout)
            jobUuid = backup_result['entities'][0]
            if not jobUuid:
                exit(1)
            if jobUuid:
                print('job uuid is {}'.format(jobUuid))
                status = 'EXECUTING'
                while status == 'EXECUTING':
                    sleep (10)
                    status = huGetJobStatus(HYCU_ENDPOINT, HYCU_USER, HYCU_SECRET, jobUuid, timeout=nTimeout)
                print('Job complete. Status: {}\n'.format(status))
            if (status != 'OK'):
                exit(1)

if __name__ == "__main__":
    main()