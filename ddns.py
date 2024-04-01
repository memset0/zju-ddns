import argparse
import os
import json
import yaml
from os import path, popen
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.dnspod.v20210323 import dnspod_client, models

config = {}
cache_dir = ''


def DescribeRecordList(params):
    try:
        cred = credential.Credential(config['secret']['id'], config['secret']['key'])
        httpProfile = HttpProfile()
        httpProfile.endpoint = "dnspod.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = dnspod_client.DnspodClient(cred, "", clientProfile)
        req = models.DescribeRecordListRequest()
        req.from_json_string(json.dumps(params))
        resp = client.DescribeRecordList(req)
        return json.loads(resp.to_json_string())
    except TencentCloudSDKException as err:
        print(err)


def ModifyRecord(params):
    try:
        cred = credential.Credential(config['secret']['id'], config['secret']['key'])
        httpProfile = HttpProfile()
        httpProfile.endpoint = "dnspod.tencentcloudapi.com"
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = dnspod_client.DnspodClient(cred, "", clientProfile)
        req = models.ModifyRecordRequest()
        req.from_json_string(json.dumps(params))
        resp = client.ModifyRecord(req)
        return json.loads(resp.to_json_string())
    except TencentCloudSDKException as err:
        print(err)


def update(host_ip):
    print('update:', host_ip)
    record_list = DescribeRecordList({"Domain": config['domain']})['RecordList']
    for record in record_list:
        if record['Name'] in config['subdomain']:
            params = {}
            params['Domain'] = config['domain']
            params['SubDomain'] = record['Name']
            params['RecordId'] = record['RecordId']
            params['RecordType'] = 'A'
            params['RecordLine'] = '默认'
            params['Value'] = host_ip
            params['TTL'] = 600
            print('record:', record)
            print('params:', params)
            print('modify:', ModifyRecord(params))


def get_cache():
    if not path.exists(cache_dir):
        return ''
    with open(cache_dir, 'r+', encoding='utf8') as file:
        return file.read()


def set_cache(new_cache):
    with open(cache_dir, 'w+', encoding='utf8') as file:
        file.write(new_cache)


def get_host_ip():
    handle = popen('ipconfig')
    result = handle.read().splitlines()
    for i in range(len(result)):
        if not result[i] or result[i].startswith(' '):
            continue
        if config['keyword'] in result[i]:
            print(result[i][:-1])
            for j in range(i + 1, len(result)):
                if 'IPv4' in result[j]:
                    host_ip = result[j].split(': ')[1].strip()
                    print('host ip:', host_ip)
                    return host_ip
    return ''


def load_config():
    global config, cache_dir
    parser = argparse.ArgumentParser(description='Process some configurations.')
    parser.add_argument('-c', '--config', help='Specify the location of the configuration file.', default='config.yml')
    args = parser.parse_args()

    config_dir = args.config if os.path.isabs(args.config) else os.path.join(os.getcwd(), args.config)
    if not os.path.exists(config_dir):
        print('config.yml not found!')
        input('Press Enter to exit...')
        return

    cache_dir = os.path.abspath(os.path.join(os.path.dirname(config_dir), './cache.txt'))
    with open(config_dir, 'r+', encoding='utf8') as file:
        config_text = file.read()
        config = yaml.load(config_text, Loader=yaml.SafeLoader)
        file.close()
    print('config:', config)


if __name__ == '__main__':
    load_config()
    host_ip = get_host_ip()
    if host_ip != get_cache():
        update(host_ip)
        set_cache(host_ip)
    else:
        print('Cache hit, skipped!')
