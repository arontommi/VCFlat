from collections import defaultdict
from cyvcf2 import VCF, Writer


class VcfMeta:
    def __init__(self, input_vcf):
        self.vcf_file = VCF('{}'.format(input_vcf), strict_gt=True)
        self.raw_vcf_header_list = [header_line for header_line in self.vcf_file.raw_header.split("\n") if header_line]
        self.extract_header()
        self.rename_long_header()
        self.sample_header = self.extract_samplenames()
        self.validateheadersyntax()
        self.meta_list = self.clean_meta()
        self.meta_dict = self.dictify()
        run_dict_chunking = self.validatemetaandheader()
        if run_dict_chunking is True:
            for i in ['INFO', 'FORMAT']:
                self.meta_dict = self.custom_dict_chunking(i, 3)
                self.meta_dict = self.list2dict(f'{i}')
            for i in ['FILTER']:
                self.meta_dict = self.custom_dict_chunking(i, 1)
                self.meta_dict = self.list2dict(f'{i}')

    def validateheadersyntax(self):
        """
        makes sure that the vcf has required fields
        :return:
        """
        if self.vcf_header[:8] == ['#CHROM','POS','ID','REF','ALT','QUAL','FILTER','INFO']:
            pass
        else:
            print('Wrong input')

    def validatemetaandheader(self):
        """
        Checks if INFO FORMAT and FILTER are in metainfo
        :return:
        """
        metalist = [i for i in  self.meta_dict]
        includelist = ['INFO', 'FORMAT','FILTER']
        run_dict_chunking = True
        if set(includelist).issubset(metalist):
            pass
        else:
            run_dict_chunking = False
        return run_dict_chunking

    def extract_header(self):
        """
        looks for the real header file of the vcf file and pops it out ( so it is not included in the meta file,
        and creates a vcf_header list
        """
        for n,i in enumerate(self.raw_vcf_header_list):
            if i.startswith('#CHROM'):
                self.raw_vcf_header_list.pop(n)
                self.vcf_header = [ii for ii in i.split('\t')]

    def rename_long_header(self):
        """
        if any of the sample names are to long, it is replaced with Sample #TODO to fix this
        :return:
        """
        if len(self.vcf_header) == 10:
            if len(self.vcf_header[9]) >= 10:
                self.vcf_header[9] = "Sample"
        return self.vcf_header

    def extract_samplenames(self):
        """
        returns samplenames
        :return:
        """
        return self.vcf_header[9:]

    def clean_meta(self):
        """
        cleans raw_vcf_header_list for downstream processing
        :return:
        """
        meta_list = []
        for i in self.raw_vcf_header_list:
            if '=<' in i:
                i = i.rstrip('>')
                i = i.replace('##', '')
                ii = i.split('=<', 1)
            else :
                i = i.replace('##', '')
                ii = i.split('=', 1)
            meta_list.append(ii)
        return meta_list


    def dictify(self):
        """
        create a dict of the meta.list
        :return:
        """
        meta_dict = defaultdict()
        for i in self.meta_list:
            try:
                key = i[0]
                value = i[1]
                if key not in meta_dict:
                    meta_dict[key] = [value]
                else:
                    meta_dict[key].append(value)
            except IndexError:
                print('index error')

        return meta_dict

    def chunks_dicts(self):
        """Yield successive n-sized chunks from l."""
        for key, value in self.meta_dict.items():
            new_dict_list = []
            for v in value:
                if v.startswith('ID'):
                    new_dict_list.append(v.split(',', 3))
                else :
                    new_dict_list.append([v])
            self.meta_dict[key] = new_dict_list

        return self.meta_dict

    def custom_dict_chunking(self, field, how_many):
        new_dict_list = []
        for v in self.meta_dict[f'{field}']:
            new_dict_list.append(v.split(',', how_many))
        self.meta_dict[field] = new_dict_list

        return self.meta_dict



    def list2dict(self, field):
        list_from_dict = self.meta_dict[f'{field}']
        self.meta_dict[f'{field}'] = {}

        for info_list in list_from_dict:
            l4d = []
            for i in info_list:
                l4d.append(i.split("=",1)[1])

            self.meta_dict[f'{field}'][l4d[0]] = l4d[1:]
        return self.meta_dict

