#!/usr/bin/python

import threading
from queue import Queue
import requests
import re
import os
import socket
import ipaddress

from .consts import *


class Scanner:
    """
    This class takes a list of ip addresses and scans hosts health.

    """

    max_threads = MAX_THREADS_COUNT
    ip_addresses = list()
    header_printed = False
    re_ip_pattern = re.compile(IP_ADDRESS_PATTERN)
    re_ip_cidr_pattern = re.compile(IP_ADDRESS_CIDR_PATTERN)

    def __init__(self, ip_addresses, ip_address_delmitier=",", run=True):
        """
        Initialize queue with ip addresses and run threaded workers.  .

        """

        self.prepare_ip_addresses(ip_addresses.split(ip_address_delmitier))

        self.queue = Queue()

        if len(self.ip_addresses) < MAX_THREADS_COUNT:
            self.max_threads = len(self.ip_addresses)

        for _ in range(self.max_threads):
            thread = threading.Thread(target=self.worker)
            thread.daemon = True
            thread.start()

        for worker in self.ip_addresses:
            ip = worker.strip()
            if self.re_ip_pattern.match(ip):
                self.queue.put(ip)
            else:
                print(INPUT_ERROR.format(ip))
                pass

        self.queue.join()

    def prepare_ip_addresses(self, raw_ip_addresses):
        ip_addresses = set()
        for ip_address in raw_ip_addresses:
            ip_address = ip_address.strip()
            if self.re_ip_pattern.match(ip_address) and self.validate_ip_address(ip_address):
                ip_addresses.add(ip_address)

            elif self.re_ip_cidr_pattern.match(ip_address):
                cidr_ip_addresses = ipaddress.ip_network(ip_address).hosts()
                if cidr_ip_addresses is not None:
                    for ip in ipaddress.ip_network(ip_address).hosts():
                        ip_addresses.add(str(ip))

            else:
                print(INPUT_ERROR.format(ip_address))
                pass

        self.ip_addresses = sorted(list(ip_addresses), key = ipaddress.IPv4Address)

    def validate_ip_address(self, address):
        try:
            ipaddress.ip_address(address)
            return True
        except ValueError:
            return False

    def scan_http(self, ip_address):
        """
        Makes an HTTP GET request to an ip address

        """
        output = {
            "ip_address": ip_address,
            "status_code": "000",
            "hostname": "",
            "server_type": ""
        }

        try:
            response = requests.get(IP_ADDRESS_URL.format(ip_address), timeout=5)

            output['status_code'] = str(response.status_code)
            output['server_type'] = self.server_type(response.headers["Server"])
            output['hostname'] = self.hostname(ip_address)

        except (requests.ConnectionError, requests.Timeout) as exception:
            pass

        self.print_response(output)

    def print_header(self):
        """
        Prints the output header

        """

        print ("{}\n{}\n{}".format(
            LINE,
            OUTPUT_COLUMN_FORMAT.format(*RESULT_HEADER_COLUMNS),
            LINE
        ))
        self.header_printed = True

    def print_response(self, response):
        """
        Prints the response output

        """
        status_color = GREEN
        if response['status_code'] == '000':
            status_color = RED
        elif response['status_code'] in ['404']:
            status_color = YELLOW

        output = OUTPUT_COLUMN_FORMAT.format(
            response['ip_address'],
            "{}{}{}".format(status_color, response['status_code'], END),
            response['hostname'],
            response['server_type']
        )

        if status_color is RED:
            output = "{}{}{}".format(status_color, output, END)

        print(output)

    def server_type(self, server):
        """
        Checks server type for specific server type versions

        """
        for i in SERVER_HEADERS:
            if re.match(i, server):
                return "*{}*".format(server)

        return server

    def hostname(self, ip_address):
        """
        Checks server hostname

        """
        try:
            hostname = socket.gethostbyaddr(ip_address)[0]
        except:
            hostname = ""
        return hostname

    def test_dir_browsing(self, content):
        """
        Checks if the server allows root-level directory listing

        """
        if INDEX_OF in content:
            return INDEX_OF_TRUE
        else:
            return INDEX_OF_FALSE

    def worker(self):
        """
        Used by each running thread to queue the work

        """
        while True:
            ip_address = self.queue.get()
            self.scan_http(ip_address)
            self.queue.task_done()
