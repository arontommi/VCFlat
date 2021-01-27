from vcflat.HeaderExtraction import VcfHeader
from vcflat.VcfParse import VcfParse
import pprint as pp


def pprint_meta(input_vcf):
    pp.pprint(VcfHeader(input_vcf).meta_dict, depth=4)


def pprint_vcf_body_header(input_vcf):
    pp.pprint(VcfHeader(input_vcf).header)


def pprint_available_keys(input_vcf):
    pp.pprint(VcfParse(input_vcf).get_header_fast())
