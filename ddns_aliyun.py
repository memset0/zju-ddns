# -*- coding: utf-8 -*-
# This file is auto-generated, don't edit it. Thanks.
import argparse
import os
import json
import yaml
import sys
from Tea.core import TeaCore
from typing import List
from os import path, popen

from alibabacloud_alidns20150109.client import Client as DnsClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_alidns20150109 import models as dns_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

config = {}
load_config = ''

class file:
	fp = {}
	def __init__(self, filename: str, mode: str):
		self.fp = open(filename, mode)
	def __del__(self):
		if self.fp:
			self.fp.close()
	def log(self, message: str):
		if self.fp:
			self.fp.write(message + '\n')

console = file('output.log', 'a')

def create_client(
	region_id: str,
	secret_id: str,
	secret_key: str
) -> DnsClient:
	"""
	整理请求参数
	"""
	api_config = open_api_models.Config()
	api_config.access_key_id = secret_id
	api_config.access_key_secret = secret_key
	api_config.region_id = region_id
	api_config.endpoint = f'alidns.cn-hangzhou.aliyuncs.com'
	return DnsClient(api_config)

def describe_domain_records(
	client: DnsClient,
	domain_name: str,
	rr: str,
	record_type: str,
) -> dns_models.DescribeDomainRecordsResponse:
	"""
	获取主域名的所有解析记录列表
	"""
	req = dns_models.DescribeDomainRecordsRequest()
	req.domain_name = domain_name
	req.rrkey_word = rr
	req.type = record_type
	try:
		resp = client.describe_domain_records(req)
		console.log('----------Describe-Domain-Records-Response----------')
		console.log(UtilClient.to_jsonstring(TeaCore.to_map(resp)))
		print('Records Fetched!')
		return resp
	except Exception as error:
		console.log(error.message)
	return

def update(
	host_ip: str
) -> None:
	client = create_client(config['region'], config['secret']['id'], config['secret']['key'])
	update_domain_record_request = dns_models.UpdateDomainRecordRequest(
		record_id = config['record'],
		rr = config['subdomain'][0],
		type = 'A',
		value = host_ip
	)
	runtime = util_models.RuntimeOptions()
	try:
		resp = client.update_domain_record_with_options(update_domain_record_request, runtime)
		console.log('----------Update-Domain-Record-Response----------')
		console.log(f'current ip: {host_ip}')
		console.log(UtilClient.to_jsonstring(TeaCore.to_map(resp)))
		print('View ooutput.log for the response')
	except Exception as error:
		console.log(error.message)
		console.log(error.data.get('Recommend'))
		UtilClient.assert_as_string(error.message)
	return

def get_cache():
	if not path.exists(cache_dir):
		return ''
	with open(cache_dir, 'r+', encoding = 'utf8') as file:
		return file.read()

def set_cache(new_cache):
	with open(cache_dir, 'w+', encoding = 'utf8') as file:
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
	parser = argparse.ArgumentParser(description = 'Process some configurations.')
	parser.add_argument('-c', '--config', help = 'Specify the location of the configuration file.', default = 'config.yml')
	args = parser.parse_args()

	config_dir = args.config if os.path.isabs(args.config) else os.path.join(os.getcwd(), args.config)
	if not os.path.exists(config_dir):
		print('config.yml not found!')
		input('Press Enter to exit...')
		return

	cache_dir = os.path.abspath(os.path.join(os.path.dirname(config_dir), './cache.txt'))
	with open(config_dir, 'r+', encoding = 'utf8') as file:
		config_text = file.read()
		config = yaml.load(config_text, Loader = yaml.SafeLoader)
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