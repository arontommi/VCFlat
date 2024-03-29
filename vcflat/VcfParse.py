import sys
from csv import DictWriter
from cyvcf2 import VCF
from itertools import product, chain
import re

from vcflat.HeaderExtraction import VcfHeader


class VcfParse:
    def __init__(self,
                 input_vcf,
                 annotation=None,
                 long_anno=None,
                 samples_in_header=None):
        self.input_vcf = input_vcf
        self.vcf_meta = VcfHeader(self.input_vcf,
                                  samples_in_header=samples_in_header)
        self.anno_fields = self.check_for_annotations()
        self.long_anno = long_anno if long_anno is not None else 20
        self.annotation = annotation
        self.vcf_header_extended = self.vcf_meta.header
        self.csq = True
        if self.anno_fields:
            self.csq = True
            self.vcf_header_extended = self.vcf_meta.header
            self.csq_labels = {}
            for i in self.anno_fields:
                self.csq_labels[i] = self.get_csq_labels(i)
                self.vcf_header_extended = self.vcf_header_extended + [
                    i + "_dict"
                ]

    def check_for_annotations(self):
        list_of_annotations = []
        for k, v in self.vcf_meta.meta_dict["INFO"].items():
            for i in v["data"]:
                if "|" in i:
                    list_of_annotations.append(k)

        return list_of_annotations

    def get_csq_labels(self, anno_flag):
        """extract csq labels from meta info and cleans leading and trailing whitespace"""
        csq_labels = (
            self.vcf_meta.meta_dict["INFO"][anno_flag]["data"][2].split(
                ":", 1)[1].split("|"))
        csq_labels = [i.strip() for i in csq_labels]
        return csq_labels

    def parse_csq(self, li, csq_labels, anno_field):
        if li[7].get(anno_field):
            ret_list = []
            annotation_length = len(li[7][anno_field].split(",")[0].split("|"))
            if len(li[7][anno_field].split(",")) >= int(self.long_anno):
                z = dict(
                    zip(
                        csq_labels[anno_field],
                        ["To Long Annotation"] * annotation_length,
                    ))
                ret_list.append(z)
            else:
                for infolist in li[7][anno_field].split(","):
                    z = dict(zip(csq_labels[anno_field], infolist.split("|")))
                    ret_list.append(z)
            return ret_list

    def split_ref_alt(self, ll):
        """
        splits FORMAT elements that has two values into REF and ALT
        """
        ra = ["_1", "_2"]
        for nr, i in enumerate(ll[9:]):
            ldicts = dict()
            for k, v in i.items():
                if len(v.split(",")) == 2:
                    try:
                        if (self.vcf_meta.meta_dict["FORMAT"][k.split("_")[1]]
                            ["double_type"] == "REF_ALT"):
                            ra = ["_REF", "_ALT"]
                    except:
                        pass
                    vsp = [int(i) for i in v.split(",")]
                    k_ra = [k + r for r in ra]
                    ndict = dict()
                    for nk, nv in zip(k_ra, vsp):
                        ndict[nk] = nv
                    ldicts = {**ldicts, **ndict}
            ll[nr + 9] = {**i, **ldicts}
        return ll

    def parse_line_list(self, listfromvcfline):
        """
        goes through the later fields in the vcf and parses them
        :param listfromvcfline:
        :return:
        """
        li = nestlists(listfromvcfline)
        li = zipformat(li, header_list=self.vcf_meta.header)
        li = self.split_ref_alt(li)
        li = splitinfo(li)
        if self.csq:
            anno_list = []
            annokeeps = self.anno_fields
            if self.annotation:
                annokeeps = [self.annotation]
            for i in annokeeps:
                parsed_annotation = self.parse_csq(li, self.csq_labels, i)
                if parsed_annotation is not None:
                    anno_list.append(parsed_annotation)
            li = list(product([li], *anno_list))

        lod = []
        for lst in li:
            res = list(
                chain.from_iterable(i if isinstance(i, list) else [i]
                                    for i in lst))
            d = {k: v for k, v in zip(self.vcf_header_extended, res)}
            lod.append(d)
        return lod

    def parse(self, sample=None):
        s = "Sample"
        if sample:
            s = sample
        vcf_file = VCF("{}".format(self.input_vcf), strict_gt=True)
        for line in vcf_file:
            split_line = [i.strip("\n") for i in str(line).split("\t")]
            return_li = self.parse_line_list(split_line)
            for d in return_li:
                merged = flatten_d(d)
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
        key_list = keys.split()
        allkeys = self.get_header()
        keyset = set(key_list)
        not_in_allkeys = list(keyset.difference(allkeys))
        if keyset.issubset(allkeys):
            return key_list
        else:
            for key in not_in_allkeys:
                try:
                    rekey = re.compile(key)
                    newlist = list(filter(rekey.match, list(allkeys)))
                    if len(newlist) == 0:
                        sys.stderr.write("No column matching regex provided")
                    else:
                        for foundkey in reversed(newlist):
                            key_list.insert(key_list.index(key), foundkey)
                    key_list.pop(key_list.index(key))
                except re.error:
                    sys.stderr.write(
                        f" these keys are not found in the vcf file: "
                        f'{"".join([i for i in  keyset.difference(allkeys)])} \n'
                        f" please check your key input or Regex pattern could not be compiled"
                    )
            return key_list

    def write2csv(self, out, keys, sample=None):
        pars = self.parse(sample=sample)
        keys = dict.fromkeys([i for i in keys]).keys()
        with (open(out, "w") if out else sys.stdout) as csvfile:
            writer = DictWriter(csvfile,
                                keys,
                                delimiter="\t",
                                extrasaction="ignore")
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
        formatlist = [
            header_list[nr + 9] + "_" + i for i in plist[0].split(":")
        ]
        ll[nr + 9] = dict(zip(formatlist, plist[1].split(":")))
    return ll


def splitinfo(li):
    """ Splits the INFO column and generates a dict"""
    defdi = dict()
    for i in li[7].split(";"):
        if "=" not in i:
            defdi[i] = "True"
        else:
            l4d = i.split("=")
            defdi[l4d[0]] = l4d[1]
    li[7] = defdi
    return li


def valdidate_csq(li, anno_field):
    """
    Validates that INFO column has the csq dict.

    """
    if li[7].get(anno_field):
        return True


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
