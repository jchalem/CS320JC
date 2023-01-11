# project: p5
# submitter: jchalem
# partner: none
# hours: 15

import geopandas, re, netaddr
from bisect import bisect
import pandas as pd
from zipfile import ZipFile, ZIP_DEFLATED
from io import TextIOWrapper
import csv, io

ips = pd.read_csv("ip2location.csv")
ips_high = list(ips["high"])

def lookup_region(ipstring):
    ipaddr = re.sub("[a-zA-Z]", "0", ipstring)
    ip_translated = int(netaddr.IPAddress(ipaddr))
    idx = bisect(ips_high, ip_translated)
    country = ips.iloc[idx]["region"]
    return country

class Filing:
    def __init__(self, html):
        dates_tuples = re.findall(r'((19|20)+\d{2}-\d{2}-\d{2})',html)
        self.html = html
        self.dates = [d[0] for d in dates_tuples]
        self.sic = None
        for m in re.findall(r'SIC=(\d+)', html):
            self.sic = int(m)
            break
        self.addresses = []
        for addr_html in re.findall(r'<div class="mailer">([\s\S]+?)</div>', html):
            #if addr_html == "":
            #    continue
            lines = []
            for line in re.findall(r'<span class="mailerAddress">([\s\S]+?)</span>', addr_html):
                lines.append(line.strip())
            if "\n".join(lines) != "":
                self.addresses.append("\n".join(lines))

    def state(self):
        state_list = []
        for addr in self.addresses:
            if re.findall(r'([A-Z]{2})\s{1}\d{5}', addr):
                abbr = re.findall(r'([A-Z]{2})\s{1}\d{5}', addr)
                return abbr[0]
        return None