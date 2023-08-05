#!/usr/bin/env python


import sys
import argparse
import os
import json
import logging
import firecrest as fc


## https://docs.python.org/dev/howto/argparse.html#the-basics

parser = argparse.ArgumentParser(description='Simple wrapper for pyFireCREST API')
parser.add_argument('-l', "--list", action='store_true', help='List files')
parser.add_argument('-a', "--address", action='store', type=str,help='Host name (e.g. daint or alps)')  
parser.add_argument('-t', "--target", action='store', type=str, 
                        help='Target folder, e.g. /store/2go/go30/JAG_test/')
parser.add_argument('-s', "--source", action='store', type=str, 
                        help='Source folder, e.g. /store/2go/go30/JAG_test/') 
parser.add_argument('--upload', action='store_true',  
                        help='upload')
parser.add_argument('--download', action='store_true', 
                        help='download')                                               
args = parser.parse_args()
#print(args)


def read_secrets() -> dict:
    filename = os.path.join('secrets.json')
    try:
        with open(filename, mode='r') as f:
            return json.loads(f.read())
    except FileNotFoundError:
        return {}


def download_obj(client, host, file_path, downloaded_file_name = '' ):
## add if not defined....
    downloaded_file_name = os.path.split(file_path)[1]
    print(downloaded_file_name)
    down_obj = client.external_download(host, file_path)


    print("Downloading", file_path, "from", host, "host.")
    print(down_obj.status)
    down_obj.finish_download(downloaded_file_name)
    print("Download complete")
    return{}


def upload_obj(client, host, file, host_dir):
    # This call will only create the link to Object Storage
    up_obj = client.external_upload(host, file, host_dir)

    print("Uploading", file, "to", host, "host in", host_dir, "directory")
    # You can follow the progress of the transfer through the status property
    print(up_obj.status)
    # As soon as down_obj.status is 111 we can proceed with the upload of local file to the staging area
    up_obj.finish_upload()


def main():

    secrets = read_secrets()

# Setup the client for the specific account
    client = fc.Firecrest(
    firecrest_url="https://firecrest.cscs.ch",
    authorization=fc.ClientCredentialsAuth( secrets["client_id"], secrets["client_secret"], secrets["token_uri"])
                                                                )

    if args.upload:
        print("time for an upload")
        upload_obj(client, args.address, args.source, args.target)
    elif args.download:
         print("time for an download")
         download_obj(client, args.address, args.source)
    elif args.list:
        print("list files")
        print(client.list_files(args.address, args.target))

    else:
        print("Please specify an option")
    

if __name__ == '__main__':
   main()

