VCFlat -- flatten Variant Call Format(VCF)
======

## A simple package to parse VCF files to a tab delimited flat file

The idea is to be able to flatten any [vcf](https://samtools.github.io/hts-specs/VCFv4.2.pdf).
It is reccomended to filter before hand but since python generators are used,
it shoud not take up all the memory.

### install
 
Since this project is still very much an ongoing project 
please let me know if you try it out and if and how it failed

you can try it out by pulling the docker image via docker hub

` docker pull arontommi/vcflat:latest
`

### Running 
basic run would look something like this:

`python3 -m vcflat -i input_file -o output_file
`

A more useful example would be:

`python3 -m vcflat -i inputfile -o outputfile --Sample my_sample_name --keys "Sample #CHROM POS REF ALT Gene_name .*_DP"`

This would create a nice simplified tab delimted file with a samplename (if you would want to combine multiple files lated down the road) 


vcflat uses the column keys from the first variant to generate the columns, if you want to get all possible columns
(since vcffiles can have a variable number of them) add the flag `--slowkeys` it is called slowkeys because you need to
iterate through the whole vcf file before you can create the columns (so twice as slow)

you can also use your own column keys and your own ordering of those keys by using:
`--keys '#CROM POS..` with the column keys being separated by space. you can also specify regexes (at least simple ones (for example '.*_PR_*')) 
to get all fields matchin a description (this is not tested extensivly yet so beware!)

I tend to run one vcf file with the `--slowkeys` flag and then pick relevant column names from there

### list of parameters:
```
    -h              :   (--help) prints out available options
    -i              :   (--inputfile) A VCF file. it can be gzipped as well
    -o              :   (--outputfile) Output file 
    -s              :   (--sample) Samplename
    --keys          :   key values in quotes sepated by space "CHROM POS.. "
    --slowkeys      :   In standard mode, VCFlat uses the first line to determine columns to use. If there are column keys that are not used in the first variant they are not included. This option creates column for all keys in all values, downside is that VCFlat has to iterate over two times over the data
    --annotation    :   To specify which annotation to use if there are multiple annotations on the vcf. since VCFlat creates a seperate line for each annotation, if there are multiple annotation it can soon balloon the file.
    --long_anno     :   To specify max number of annotations (default set at 20). very hand to reduce annotations for structural variant files
    
    pretty print functions (input file needs to be provided)
    --pprint_header         :   prints out the vcf header of the vcf file provided
    --pprint_body_header    :   prints out the body header of the vcf file 
    --pprint_available_keys :   prints out available keys for the vcf file 
```

VCFlat uses [Cyvcf2](https://github.com/brentp/cyvcf2) under the hood. Cyvcf2 *is a cython wrapper around [htslib](https://github.com/samtools/htslib)
 built for fast parsing of [Variant Call Format](https://en.m.wikipedia.org/wiki/Variant_Call_Format) (VCF) files.*
