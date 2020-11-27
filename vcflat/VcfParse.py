import sys
from csv import DictWriter
from cyvcf2 import VCF
from itertools import tee

from vcflat.HeaderExtraction import populatevcfheader


class VcfParse:
    def __init__(self, input_vcf):
        self.input_vcf = input_vcf
        self.vcf_meta = populatevcfheader(self.input_vcf)
        self.anno_fields = self.check_for_annotations()
        self.csq = self.csq_flag()
        self.vcf_header_extended = self.vcf_meta.header
        if self.csq:
            self.csq_labels = self.get_csq_labels()
            self.vcf_header_extended = self.vcf_meta.header + ['CSQdict']

    def check_for_annotations(self):
        list_of_annotations = []
        for k, v in self.vcf_meta.meta_dict['INFO'].items():
            for i in v:
                if '|' in i:
                    list_of_annotations.append(k)

        return list_of_annotations


    def csq_flag(self):
        """
        Checks if the meta dict includes an INFO field and if the info has CSQ annotation
        """

        if self.vcf_meta.meta_dict.get("INFO"):
            if self.vcf_meta.meta_dict['INFO'].get(self.anno_fields[0]):
                return True
        else:
            return False

    def get_csq_labels(self):
        """extract csq labels from meta info"""
        csq_labels = self.vcf_meta.meta_dict['INFO'][self.anno_fields[0]][2].split(':', 1)[1].split('|')
        return csq_labels

    def parse_line_list(self,listfromvcfline):
        """
        goes through the later fields in the vcf and parses them
        :param listfromvcfline:
        :return:
        """
        li = nestlists(listfromvcfline)
        li = zipformat(li, header_list=self.vcf_meta.header)
        li = split_ref_alt(li)
        li = generate_vaf(li)
        li = splitinfo(li)
        if self.csq:
            li = parse_csq(li, self.csq_labels, self.anno_fields)

        d = {k: v for k, v in zip(self.vcf_header_extended, li)}
        return d


    def parse(self, sample=None):
        s = 'Sample'
        if sample:
            s = sample
        vcf_file = VCF('{}'.format(self.input_vcf), strict_gt=True)
        for line in vcf_file:
            split_line = [i.strip('\n') for i in str(line).split('\t')]
            return_li = self.parse_line_list(split_line)
            merged = flatten_d(return_li)
            merged.update({"Sample": s})
            yield merged

    """functions to extract column headers"""

    def get_header(self):
        pars = self.parse()
        keys = set()
        for d in pars:
            keys.update(d.keys())
        return keys

    def get_header_fast(self):
        pars = self.parse()
        first_line = next(pars)
        keys = set(first_line.keys())
        return keys

    def sanitize_keys(self, keys):
        allkeys = self.get_header()
        keyset = set(keys.split())
        if keyset.issubset(allkeys):
            return keys.split()
        else:
            sys.stderr.write(f' these keys are not found in the vcf file: {"".join([i for i in  keyset.difference(allkeys)])} \n'
                     f' please check your key input')


    def write2csv(self, out, keys, sample=None):
        pars = self.parse(sample)
        keys = dict.fromkeys([i for i in keys]).keys()
        with (open(out, 'w') if out else sys.stdout) as csvfile:
            writer = DictWriter(csvfile, keys, delimiter='\t', extrasaction='ignore')
            writer.writeheader()
            for line in pars:
                writer.writerow(line)


def nestlists(ll):
    """
    adds FORMAT labels with format values in sample columns
    :param ll:
    :return:
    """
    for nr, i in enumerate(ll[9:]):
        ll[nr + 9] = [ll[8], i]
    return ll

def zipformat(ll, header_list):
    """
    zips together FORMAT labels, Sample name and format values into one dict
    """
    for nr, plist in enumerate(ll[9:]):
        formatlist = [header_list[nr + 9] + '_' + i for i in plist[0].split(':')]
        ll[nr + 9] = dict(zip(formatlist, plist[1].split(':')))
    return ll

def split_ref_alt(ll):
    """
    splits FORMAT elements that has two values into REF and ALT
    """
    ra = ['_REF', '_ALT']
    for nr, i in enumerate(ll[9:]):
        ldicts = dict()
        for k, v in i.items():
            if len(v.split(',')) == 2:
                vsp = [int(i) for i in v.split(',')]
                k_ra = [k + r for r in ra]
                ndict = dict()
                for nk, nv in zip(k_ra, vsp):
                    ndict[nk] = nv
                ldicts = {**ldicts, **ndict}
        ll[nr + 9] = {**i, **ldicts}
    return ll

def generate_vaf(ll):
    """
    Creates VAF tab (variant allele frequency) AD_ALT / (AD_REF + AD_ALT)
    """
    for nr, i in enumerate(ll[9:]):
        refdp = 1
        altdp = 1
        ndict = {}
        sample = ''
        for k, v in i.items():
            if k.endswith("AD_REF"):
                refdp = v
                sample = k.strip("AD_REF")
            if k.endswith("AD_ALT"):
                altdp = v
            totdp = refdp + altdp
            try:
                vaf = altdp / totdp
            except ZeroDivisionError:
                vaf = 0
            ndict = {f'{sample}_VAF': vaf}
        if sample == '':
            pass
        else:
            ll[nr + 9] = {**i, **ndict}
    return ll

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

def valdidate_csq(li, anno_field):
    """
    Validates that INFO column has the csq dict.

    """

    if not li[7].get(anno_field):
        return True

def parse_csq(li, csq_labels, anno_field):
    ret_list = li.copy()
    flag = valdidate_csq(li, anno_field)
    if not flag:
        for infolist in li[7][anno_field].split(','):
            nl = li.copy()
            z = dict(zip(csq_labels, infolist.split('|')))
            nl.append(z)
            ret_list = nl
    return ret_list

def flatten_d(d):
    """
    collects and flattens nested dicts ( unnesting )
    :param d: nested dict
    :return: unnested dict
    """
    mergeddict = dict()
    for k, v in d.items():
        if type(v) is dict:
            mergeddict.update(v)
    dd = {**d, **mergeddict}
    return dd
