import pandas as pd
import pprint as pp
import csv
from pancakevcf.HeaderExtraction import *


class VcfParse:
    def __init__(self, input_vcf, keys=False):
        self.vcf_meta = VcfMeta().populatevcfheader(input_vcf=input_vcf)

        self.csq = self.csq_flag()
        self.vcf_header_extended = self.vcf_meta.header
        if self.csq:
            self.csq_labels = self.get_csq_labels()
            self.vcf_header_extended = self.vcf_meta.header + ['CSQdict']

        if keys:
            self.df = self.write2csv(input_vcf,keys)
        else:
            keys = self.get_header(input_vcf)
            self.df = self.write2csv(input_vcf, keys)


    """Flag functions do determine what to run based on meta information information """
    def csq_flag(self):
        """
        Checks if the meta dict includes an INFO field and if the info has CSQ annotation
        """
        if self.vcf_meta.meta_dict.get("INFO"):
            if self.vcf_meta.meta_dict['INFO'].get('CSQ'):
                return True
        else:
            return False

    def get_csq_labels(self):
        """extract csq labels from meta info"""
        csq_labels = self.vcf_meta.meta_dict['INFO']['CSQ'][2].split(':',1)[1].split('|')
        return csq_labels


    """Functions to deal with FORMAT and Sample columns of the vcf"""

    @staticmethod
    def nestlists(ll):
        """
        adds FORMAT labels with format values in sample columns
        :param ll:
        :return:
        """
        for nr, i in enumerate(ll[9:]):
            ll[nr+9] = [ll[8],i]
        return ll

    @staticmethod
    def zipformat(ll,header_list):
        """
        zips together FORMAT labels, Sample name and format values into one dict
        :param ll:
        :param header_list:
        :return:
        """
        for nr, plist in enumerate(ll[9:]):
            formatlist = [header_list[nr+9]+'_'+ i for i in plist[0].split(':')]
            ll[nr + 9] = dict(zip(formatlist,plist[1].split(':')))
        return ll

    @staticmethod
    def split_ref_alt(ll):
        """
        splits FORMAT elements that has two values into REF and ALT

        """
        RA = ['_REF', '_ALT']
        for nr, i in enumerate(ll[9:]):
            ldicts = dict()
            for k, v in i.items():
                if len(v.split(',')) == 2:
                    vsp = [ int(i) for i in v.split(',')]
                    k_RA = [k+r for r in RA]
                    ndict = dict()
                    for nk , nv in zip(k_RA, vsp):
                        ndict[nk] = nv
                    ldicts = {**ldicts,**ndict}
            ll[nr + 9] = {**i, **ldicts}

        return(ll)

    def format2samples(self, li):
        """
        master function to parse FORMAT and sample elements of each vcf line
        :param li: vcf line
        :return: formatted vcf line and removes the FORMAT from the vcf line
        """
        li = self.nestlists(li)
        li = self.zipformat(li, header_list=self.vcf_meta.header)
        li = self.split_ref_alt(li)
        return li

    """Functions to deal with The Info column of the vcf"""

    @staticmethod
    def splitinfo(li):
        """ Splits the INFO column and generates a dict"""
        defdi = dict()
        for i in li[7].split(';'):
            if '=' not in i:
                defdi[i] = 'True'
            else:
                l4d = i.split('=')
                defdi[l4d[0]] = l4d[1]
        li[7] = defdi
        return li

    @staticmethod
    def valdidate_CSQ(li):
        """
        Validates that INFO column has the csq dict.
        :param li:
        :return:
        """

        if not li[7].get("CSQ"):
            return True

    def parse_csq(self, li,csq_labels):
        ret_list = li.copy()
        flag = self.valdidate_CSQ(li)
        if not flag:
            for infolist in li[7]['CSQ'].split(','):
                nl = li.copy()
                z = dict(zip(csq_labels, infolist.split('|')))
                nl.append(z)
                ret_list = nl
        return ret_list

    def read_vcf(self, input_vcf):
        vcf_file = VCF('{}'.format(input_vcf), strict_gt=True)
        return vcf_file

    def split_line(self, line):
        listfromvcfline = [i.strip('\n') for i in str(line).split('\t')]
        return listfromvcfline



    def parse_line_list(self,listfromvcfline):
        li = self.format2samples(listfromvcfline)
        li = self.splitinfo(li)
        if self.csq:
            li = self.parse_csq(li, self.csq_labels)
        d = {k: v for k, v in zip(self.vcf_header_extended, li)}
        return d

    def flatten_d(self, d):
        mergeddict = dict()
        for k,v in d.items():
            if type(v) is dict:
                mergeddict.update(v)
        dd = {**d, **mergeddict}
        return dd

    def parse(self, input_vcf):
        vcf_file = self.read_vcf(input_vcf)
        for i in vcf_file:
            line = self.split_line(i)
            return_li = self.parse_line_list(line)
            merged = self.flatten_d(return_li)
            yield merged

    def get_header(self, input_vcf):
        pars = self.parse(input_vcf)
        keys = set()
        for d in pars:
            keys.update(d.keys())
        return keys

    def write2csv(self, input_vcf, keys):
        pars = self.parse(input_vcf)

        file = '/Users/aroska/TestingData/writtenoutput.csv'
        with open(file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile,keys, delimiter='\t',extrasaction='ignore')
            writer.writeheader()
            nr = 0
            for line in pars:
                writer.writerow(line)
                nr += 1
                if nr % 10000 == 0:
                    print(f'{nr} processed')
        df = pd.read_csv('/Users/aroska/TestingData/writtenoutput.csv', sep='\t')
        return df
