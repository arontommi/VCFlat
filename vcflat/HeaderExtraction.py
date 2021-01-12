from collections import defaultdict
from cyvcf2 import VCF
import pprint as pp
import sys

class VcfHeader(object):
    """Class around meta information about vcf file as well as functions to view it"""

    def __init__(self, input_vcf, header=None, meta_dict=None):

        self.input_vcf = input_vcf
        self.header = header if header is not None else []
        self.meta_dict = meta_dict if meta_dict is not None else {}

    def pprint_meta(self, key=False):
        self.meta_dict = process_meta_dict(self.input_vcf)
        if key:
            try:
                print(f'\n'
                      f'Printing out the values from the meta dict for {key}\n'
                      f'Starts with a key and then gives a info for the output\n')
                for k, v in self.meta_dict[key].items():
                    print(f"Key = {k} : Values = {v}")
            except AttributeError:
                print(f'Seems like the key value pairs did not play nicely for {key} \n'
                      'but here is the output anyway ')
                print(self.meta_dict[key])
        else:
            pp.pprint(self.meta_dict, depth=3)

    def determine_keys(self):
        pass


def get_raw_header(input_vcf):
    """
    Gets input_vcf as input
    returns the raw header of the vcf file
    """
    vcf_file = VCF('{}'.format(input_vcf), strict_gt=True)
    raw_vcf_header_list = [header_line for header_line in vcf_file.raw_header.split("\n") if header_line]

    return raw_vcf_header_list


def extract_header(input_vcf):
    """
    looks for the real header file of the vcf file and creates a vcf_header list
    :returns header_list
    """
    vcf_header = ''
    raw_header = get_raw_header(input_vcf)
    for i in raw_header:
        if i.startswith('#CHROM'):
            vcf_header = [ii for ii in i.split('\t')]
    return vcf_header


def pop_header(raw_header):
    """
    removes the header from the raw header
    :return:
    """
    for i in raw_header:
        if i.startswith('#CHROM'):
            raw_header.pop()
    return raw_header


def clean_meta(unclean_list):
    """
    cleans raw_vcf_header_list for downstream processing
    :return:
    """
    clean_list = []
    for i in unclean_list:
        if '=<' in i:
            i = i.rstrip('>')
            i = i.replace('##', '')
            ii = i.split('=<', 1)
        else:
            i = i.replace('##', '')
            ii = i.split('=', 1)
        clean_list.append(ii)
    return clean_list


def dictify(clean_list):
    """
    create a dict of the meta.list
    :return:
    """
    base_dict = defaultdict()
    for i in clean_list:
        try:
            key = i[0]
            value = i[1]
            if key not in base_dict:
                base_dict[key] = [value]
            else:
                base_dict[key].append(value)
        except IndexError:
            print('index error')

    return base_dict


def validate_meta(base_dict):
    """
    Checks if INFO and FORMAT are in metainfo
    :return:
    """
    metalist = [i for i in base_dict]
    includelist = ['INFO', 'FORMAT', 'FILTER']
    inmeta = {}
    for i in includelist:
        if i in metalist:
            inmeta[i] = True
        else:
            inmeta[i] = False
    return inmeta


def custom_dict_chunking(basedict, field, how_many):
    """
    splits a dict value based on comma x amount of times

    :param basedict: a dict with keys and messy values
    :param field: what key to split in the dict
    :param how_many: how many fields should remain after splitting
    :return: clean dict (hopefully)
    """

    new_dict_list = []
    for v in basedict[field]:
        new_dict_list.append(v.split(',', how_many))
    basedict[field] = new_dict_list

    return basedict


def list2dict(basedict, field):
    """
    generates a dict from list by splitting up the key value pairs seperated by =
    :param basedict: dict to work on
    :param field:  field in dict to work on
    :return: fixed dict
    """

    list_from_dict = basedict[field]
    basedict[field] = {}

    for info_list in list_from_dict:
        l4d = []
        for i in info_list:
            l4d.append(i.split("=", 1)[1])
        basedict[field][l4d[0]] = {"data": l4d[1:]}
    return basedict


def generate_complete_dict(basedict, field, how_many):
    """
    basic wrapper function around generating nice dicts from nested data
    :param basedict: original dict
    :param field:  what field to extract
    :param how_many: how many "chunks" to extract
    :return: a nice structured dict
    """

    dict_list = custom_dict_chunking(basedict, field, how_many)
    meta_dict = list2dict(dict_list, field)

    return meta_dict


def process_meta_dict(inputvcf):
    """
    main parsing of the vcf header (everything that starts with ## into a nice dict of all meta information
    :param inputvcf: basic VCF file
    :return: a nice dict with all header elements and their subelements structured
    """
    raw_header = get_raw_header(inputvcf)
    raw_header_popped = pop_header(raw_header)
    cleaned_meta = clean_meta(raw_header_popped)
    base_dict = dictify(cleaned_meta)

    chunk_dict = validate_meta(base_dict)

    meta_dict = {}
    if chunk_dict['INFO']:
        meta_dict = generate_complete_dict(base_dict, "INFO", 3)
    if chunk_dict['FORMAT']:
        meta_dict = generate_complete_dict(base_dict, 'FORMAT', 3)
    if chunk_dict['FILTER']:
        meta_dict = generate_complete_dict(meta_dict, 'FILTER', 1)
    return meta_dict


def populatevcfheader(input_vcf, samples_in_header=None):
    """
    returns a header on the original vcf with "samplefield" being the sample names (fields after the "INFO" samples)


    :param input_vcf: basic VCF file
    :param samples_in_header: samplenames
    :return: things that should be in the actual header of the vcf
    """
    metadict = process_meta_dict(input_vcf)
    header = extract_header(input_vcf)
    if samples_in_header:
        samples_in_header = samples_in_header.split()
        if len(samples_in_header) == len(header[9:]):
            header = header[:9] + samples_in_header
        else:
            sys.exit(f" '--samples_in_header' given has {len(samples_in_header)}, "
                             f"but there are {len(header[9:])} samples columns in the vcf body header")

    vcf_header = VcfHeader(input_vcf, header, metadict)
    return vcf_header

def detect_double_type(input_vcf):
    metadict = process_meta_dict(input_vcf)
    for k, v in metadict["FORMAT"].items():
        double_type = "NAN"
        if any('ref' and 'alt' in i for i in v["data"]):
            double_type = "REF_ALT"
        if any('tier' in i for i in v['data']):
            double_type = "TIERS"
        metadict['FORMAT'][k]['double_type'] = double_type
    return metadict
