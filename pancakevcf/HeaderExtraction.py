from collections import defaultdict
from cyvcf2 import VCF
import pprint as pp


class VcfHeader(object):
    """Class around meta information about vcf file as well as funtions to view it"""

    input_vcf = ''
    header = []
    meta_dict = {}
    def __init__(self, input_vcf, header, meta_dict):

        self.input_vcf = input_vcf
        self.header = header
        self.meta_dict = meta_dict


    def pprint_meta(self,key=False):

        if key:

            try:
                print(f'\n'
                      f'Printing out the values from the meta dict for {key}\n'
                      f'Starts with a key and then gives a info for the output\n')
                for k,v in self.meta_dict[key].items():
                    print(f"Key = {k} : Values = {v}")
            except AttributeError:
                print(f'Seems like the key value pairs did not play nicely for {key} \n'
                      'but here is the output anyway ')
                print(self.meta_dict[key])
        else:
            pp.pprint(self.meta_dict,depth=1)

    def determine_keys(self):
        pass


class VcfMeta:
    def __init__(self,input_vcf):
        self.vcf_header = self.populatevcfheader(input_vcf=input_vcf)

    """ class to create a vcfinfo object """


    @staticmethod
    def get_raw_header(input_vcf):
        """
        Gets input_vcf as input
        returns the raw header of the vcf file
        """
        vcf_file = VCF('{}'.format(input_vcf), strict_gt=True)
        raw_vcf_header_list = [header_line for header_line in vcf_file.raw_header.split("\n") if header_line]

        return raw_vcf_header_list

    def extract_header(self, input_vcf):
        """
        looks for the real header file of the vcf file and creates a vcf_header list
        :returns header_list
        """
        vcf_header = ''
        raw_header = self.get_raw_header(input_vcf)
        for i in raw_header:
            if i.startswith('#CHROM'):
                vcf_header = [ii for ii in i.split('\t')]
        return vcf_header

    @staticmethod
    def pop_header(raw_header):
        """
        removes the header from the raw header
        :return:
        """
        for i in raw_header:
            if i.startswith('#CHROM'):
                raw_header.pop()
        return raw_header


    @staticmethod
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
            else :
                i = i.replace('##', '')
                ii = i.split('=', 1)
            clean_list.append(ii)
        return clean_list

    @staticmethod
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


    @staticmethod
    def validate_meta(base_dict):
        """
        Checks if INFO FORMAT and FILTER are in metainfo
        :return:
        """
        metalist = [i for i in  base_dict]
        includelist = ['INFO', 'FORMAT','FILTER']
        run_dict_chunking = True
        if set(includelist).issubset(metalist):
            pass
        else:
            run_dict_chunking = False

        return run_dict_chunking

    @staticmethod
    def custom_dict_chunking(basedict, field, how_many):
        new_dict_list = []
        for v in basedict[field]:
            new_dict_list.append(v.split(',', how_many))
        basedict[field] = new_dict_list

        return basedict

    @staticmethod
    def list2dict(basedict, field):
        list_from_dict = basedict[field]
        basedict[field] = {}

        for info_list in list_from_dict:
            l4d = []
            for i in info_list:
                l4d.append(i.split("=",1)[1])

            basedict[field][l4d[0]] = l4d[1:]
        return basedict

    def generate_complete_dict(self,basedict,field,how_many):
        meta_dict = self.custom_dict_chunking(basedict,field, how_many)
        meta_dict = self.list2dict(meta_dict,field)
        return meta_dict


    def process_meta_dict(self, inputvcf):

        raw_header = self.get_raw_header(inputvcf)
        raw_header_popped = self.pop_header(raw_header)
        clean_meta = self.clean_meta(raw_header_popped)
        base_dict = self.dictify(clean_meta)

        chunk_dict = self.validate_meta(base_dict)

        meta_dict = {}
        if chunk_dict:
            for field in ['INFO', 'FORMAT']:
                meta_dict = self.generate_complete_dict(base_dict,field, 3)

            for field in ['FILTER']:
                meta_dict = self.generate_complete_dict(meta_dict, field, 1)
        return meta_dict


    def populatevcfheader(self,input_vcf):

        header = self.extract_header(input_vcf)
        metadict = self.process_meta_dict(input_vcf)

        vcf_header = VcfHeader(input_vcf,header,metadict)

        return vcf_header


