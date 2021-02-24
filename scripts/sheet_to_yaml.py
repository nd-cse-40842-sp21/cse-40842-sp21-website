#!/usr/bin/env python3

import os

from apiclient          import discovery
from oauth2client       import client
from oauth2client       import tools
from oauth2client.file  import Storage

import httplib2
import yaml

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES              = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE  = os.path.expanduser('~/.config/google/form_processor_client_secret.json')
APPLICATION_NAME    = 'Python Form Processor'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir 	    = os.path.expanduser('~')
    credential_dir  = os.path.join(home_dir, '.config/google')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'sheets-credentials.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    credentials     = get_credentials()
    http 	    = credentials.authorize(httplib2.Http())
    discoveryUrl    = 'https://sheets.googleapis.com/$discovery/rest?version=v4'
    service 	    = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)
    spreadsheetId   = '12xiUNQG1RyxrvFDiybhoOzzzlMSnF-m9pW928OwSzDM'
    rangeName       = 'Form Responses!A2:E'

    result = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])
    blogs  = []
    for row in values:
        blogs.append({
            'netid':    row[2],
            'url':      row[3],
            'feed':     row[4],
        })
    
    print(yaml.safe_dump(sorted(blogs, key=lambda b: b['netid']), default_flow_style=False))

if __name__ == '__main__':
    main()
