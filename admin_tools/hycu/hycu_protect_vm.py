import sys
import argparse
import requests
import time

# Avoid security exceptions/warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

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
            requestUrl = "https://%s:8443/rest/v1.0/%s" %(server, url)
        else:
            requestUrl = "https://%s:8443/rest/v1.0/%spageSize=%d&pageNumber=%d" %(server, url, pagesize, pageNumber)
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
    return huRestGeneric(server, username, password, 'vms/%s/backups?' %(vmUUID), timeout, pagesize)

def huGetJobsForVG(vgUUID, server, username, password, pagesize, timeout):
    """ Returns a list of jobs for selected vgUUID """
    return huRestGeneric(server, username, password, 'volumegroups/%s/backups?' %(vgUUID), timeout, pagesize)

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

def huBackupVm(vmUUID, server, username, password, timeout):
    # Prepare the HTTP get request
    options = '{ \
        "uuidList":["%s"] \
    }' %(vmUUID)

    requestUrl = "https://%s:8443/rest/v1.0/schedules/backup" %(server)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*'
    }
    response = requests.post(requestUrl,auth=(username,password), cert="", headers=headers, verify=False, data=options, timeout=timeout)
    if response.status_code not in [200,201,202]:
        print('Status:', response.status_code, 'Failed to trigger a Backup of %s. Exiting.' %(vmUUID))
        exit(response.status_code)

    return response.json()

def huBackupVg(vgUUID, server, username, password, timeout):
    # Prepare the HTTP get request
    options = '{ \
        "uuidList":["%s"] \
    }' %(vgUUID)

    requestUrl = "https://%s:8443/rest/v1.0/schedules/backupVolumeGroup" %(server)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*'
    }
    response = requests.post(requestUrl,auth=(username,password), cert="", headers=headers, verify=False, data=options, timeout=timeout)
    if response.status_code not in [200,201,202]:
        print('Status:', response.status_code, 'Failed to trigger a Backup of %s. Exiting.' %(vgUUID))
        exit(response.status_code)

    return response.json()

def huArchiveVm(backupUuid, policyUuid, archiveType, server, username, password, timeout):
    # Prepare the HTTP get request
    options = '{ \
        "backupUuid": "%s", \
        "policyUuid": "%s", \
        "archivingType": "%s" \
    }' %(backupUuid, policyUuid, archiveType)

    requestUrl = "https://%s:8443/rest/v1.0/schedules/archive" %(server)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*'
    }
    response = requests.post(requestUrl,auth=(username,password), cert="", headers=headers, verify=False, data=options, timeout=timeout)
    if response.status_code not in [200,201,202]:
        print('Status:', response.status_code, 'Failed to trigger an archive of %s.\n\nDetailed API response:' %(vmUUID))
        print(response.text)
        exit()

    return response.json()

def huArchiveVg(backupUuid, policyUuid, archiveType, server, username, password, timeout):
    # Prepare the HTTP get request
    options = '{ \
        "backupUuid": "%s", \
        "policyUuid": "%s", \
        "archivingType": "%s" \
    }' %(backupUuid, policyUuid, archiveType)

    requestUrl = "https://%s:8443/rest/v1.0/schedules/archiveVolumeGroup" %(server)
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*'
    }
    response = requests.post(requestUrl,auth=(username,password), cert="", headers=headers, verify=False, data=options, timeout=timeout)
    if response.status_code not in [200,201,202]:
        print('Status:', response.status_code, 'Failed to trigger an archive of %s.\n\nDetailed API response:' %(vgUUID))
        print(response.text)
        exit()

    return response.json()

def huGetJobStatus(server, username, password, jobUuid, timeout):
    """ Retrieves Job status """
    dict = {}
    endpoint = "jobs/%s" %(jobUuid)
    data = huRestGeneric(server, username, password, endpoint, timeout, None)
    return data[0]['status']

def main(argv):
    # Parse command line parameters VM and/or status
    myParser = argparse.ArgumentParser(description="HYCU for Enterprise Clouds backup and archive")
    myParser.add_argument("-s", "--server", help="HYCU Server IP", required=True)
    myParser.add_argument("-u", "--username", help="HYCU Username", required=True)
    myParser.add_argument("-p", "--password", help="HYCU Password", required=True)
    group = myParser.add_mutually_exclusive_group(required=True)
    group.add_argument("-v", "--vm", help="Virtual machine name")
    group.add_argument("-vg", "--vg", help="Volume Group name")
    operation = myParser.add_mutually_exclusive_group(required=True)
    operation.add_argument("-b", "--backup", type=str2bool, nargs='?', const=True, default=False, help="Excute backup")
    operation.add_argument("-a", "--archive", choices=['DAY', 'WEEK', 'MONTH', 'YEAR'], help="Execute archive of type")
    myParser.add_argument("-w", "--wait", type=str2bool, nargs='?', const=True, default=False, help="Wait out for job to complete", required=False)
    myParser.add_argument("-i", "--timeout", help="Advanced: REST Query timeout [default=5]", required=False)
    myParser.add_argument("-z", "--pagesize", help="Advanced: REST Query pagesize [default=None]", required=False)

    if len(sys.argv)==1:
        myParser.print_help()
        exit(1)

    args = myParser.parse_args(argv)

    # REST call intializations
    nTimeout = 5 if not args.timeout else int(args.timeout)
    pageSize = None if not args.pagesize else int(args.pagesize)

    if (args.vm != None):
        # Retrieve the list of VMs from HYCU Rest API server (page by page)
        vms = huGetVMs(args.server, args.username, args.password, timeout=nTimeout, pagesize=pageSize)

        # Check if the given VM name is valid
        vm = huFindItemByValue(vms, 'vmName', args.vm)
        if (vm == None):
            print('Status:', 'Cannot find VM "%s" in the list of HYCU VMs' %(args.vm))
            exit(1)

        if args.backup:
            result = huBackupVm(vm['uuid'], args.server, args.username, args.password, timeout=nTimeout)
        elif (args.archive != None):
            policyUuid = vm['protectionGroupUuid']
            backups = huGetJobsForVM(vm['uuid'], args.server, args.username, args.password, timeout=nTimeout, pagesize=pageSize)
            backupUuid = huGetLastSuccessfulUUID(backups)
            result = huArchiveVm(backupUuid, policyUuid, args.archive, args.server, args.username, args.password, timeout=nTimeout)

    if (args.vg != None):
        # Retrieve the list of VGs from HYCU Rest API server (page by page)
        vgs = huGetVGs(args.server, args.username, args.password, timeout=nTimeout, pagesize=pageSize)

        # Check if the given VG name is valid
        vg = huFindItemByValue(vgs, 'name', args.vg)
        if (vg == None):
            print('Status:', 'Cannot find VG "%s" in the list of HYCU VGs' %(args.vg))
            exit(1)

        if args.backup:
            result = huBackupVg(vg['uuid'], args.server, args.username, args.password, timeout=nTimeout)
        elif (args.archive != None):
            policyUuid = vg['protectionGroupUuid']
            backups = huGetJobsForVG(vg['uuid'], args.server, args.username, args.password, timeout=nTimeout, pagesize=pageSize)
            backupUuid = huGetLastSuccessfulUUID(backups)
            result = huArchiveVg(backupUuid, policyUuid, args.archive, args.server, args.username, args.password, timeout=nTimeout)

    jobUuid = result['entities'][0]
    if not jobUuid:
        exit(1)

    if args.backup:
        print ('Backup started. Job Uuid: %s' %(jobUuid))
    elif (args.archive != None):
        print ('Archive started. Job Uuid: %s' %(jobUuid))

    if not args.wait:
        exit(0)

    if jobUuid:
        status = 'EXECUTING';
        while status == 'EXECUTING':
            time.sleep (10)
            status = huGetJobStatus(args.server, args.username, args.password, jobUuid, timeout=nTimeout)
            #print('Job status - %s' %(status))

        print('Job complete. Status: %s\n' %(status))

    if (status != 'OK'):
        exit(1)

    exit(0)

if __name__ == "__main__":
    main(sys.argv[1:])