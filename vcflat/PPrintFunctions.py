from vcflat.HeaderExtraction import VcfHeader

import pprint as pp


def pprint_meta(input_vcf):
    pp.pprint(VcfHeader(input_vcf).meta_dict, depth=4)


def pprint_vcf_body_header(input_vcf):
    pp.pprint(VcfHeader(input_vcf).header)


def pprint_available_keys(input_vcf):
    pass