import pandas as pd
import pprint as pp
from itertools import chain
import collections

from pancakevcf.HeaderExtraction import *

class VcfParse:
    def __init__(self, input_vcf):
        he = VcfMeta(input_vcf)
        self.vcf_header = he.vcf_header
        self.sample_header = he.sample_header
        self.meta_dict = he.meta_dict
        self.csq = self.csq_flag()
        self.csq_labels = []
        if self.csq:
            self.vcf_header_extended = self.vcf_header + ['CSQdict']
            self.csq_labels = he.meta_dict['INFO']['CSQ'][2].split(':',1)[1].split('|')
            self.csq_len = len(self.csq_labels)
        else:
            self.vcf_header_extended = self.vcf_header
        self.df = self.main_parse(input_vcf)

    def csq_flag(self):
        """
        Checks if the meta dict includes an INFO field and if the info has CSQ annotation
        """
        if self.meta_dict.get("INFO"):
            if self.meta_dict['INFO'].get('CSQ'):
                return True
        else:
            return False


    def nestlists(self,ll):
        """
        adds FORMAT labels with format values in sample columns
        :param ll:
        :return:
        """
        for nr, i in enumerate(ll[9:]):
            ll[nr+9] = [ll[8],i]
        if self:
            return ll

    def zipformat(self,ll):
        """
        zips together FORMAT labels, Sample name and format values into one dict
        :param ll:
        :return:
        """
        for nr, plist in enumerate(ll[9:]):
            formatlist = [self.vcf_header_extended[nr+9]+'_'+ i for i in plist[0].split(':')]
            ll[nr + 9] = dict(zip(formatlist,plist[1].split(':')))
        return ll

    def split_ref_alt(self,ll):
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
        li = self.nestlists(li)
        li = self.zipformat(li)
        li = self.split_ref_alt(li)
        li.pop(8)
        return li

    def splitinfo(self, li):
        defdi = defaultdict()
        for i in li[7].split(';'):
            if '=' not in i:
                defdi[i] = 'True'
            else:
                l4d = i.split('=')
                defdi[l4d[0]] = l4d[1]
        li[7] = defdi
        if self:
            return li



    def read_vcf(self, input_vcf):
        vcf_file = VCF('{}'.format(input_vcf), strict_gt=True)
        if self:
            return vcf_file

    def parse_vcf_elements(self, vcf_file):
        masterlist = []
        for i in vcf_file:
            li = []
            for ii in str(i).split('\t'):
                li.append(ii.strip())
            li = self.format2samples(li)
            li = self.splitinfo(li)
            ret_list = li
            if self.csq:
                for infolist in li[7]['CSQ'].split(','):
                    nl = li.copy()
                    z = dict(zip(self.csq_labels, infolist.split('|')))
                    nl.append(z)
                    ret_list = nl
            masterlist.append(ret_list)
        return masterlist

    def masterlist2df(self,masterlist):
        dictlist = []
        for li in masterlist:
            mergeddict = defaultdict()
            for d in li[7:]:
                mergeddict.update(d)
            dictlist.append(mergeddict)
        infodf = pd.DataFrame(dictlist)
        self.vcf_header_extended.pop(8)
        df = pd.DataFrame(masterlist, columns=self.vcf_header_extended)
        combdf = pd.concat([df.reset_index(drop=True), infodf], axis=1)
        return combdf

    def main_parse(self, input_vcf):
        vcf_file = self.read_vcf(input_vcf)
        masterlist = self.parse_vcf_elements(vcf_file)
        df = self.masterlist2df(masterlist)
        return df


    def pprint_columns(self):
        pp.pprint(list(self.df.columns.values))



