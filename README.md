VCFlat -- flatten Variant Call Format(VCF)
======

##A simple package to parse VCF files to a tab delimited flat file

The idea is to be able to flatten any [vcf](https://samtools.github.io/hts-specs/VCFv4.2.pdf). It is reccomended
to filter before hand but since python generators are used,
it shoud not take up all the memory.

 
Since this project is still very much an ongoing project please let me know if you try it out and if and how it failed

basic run would look something like this:

`python3 vcflat -i input_file -o output_file
`

vcflat uses the column keys from the first variant to generate the columns, if you want to get all possible columns
(since vcffiles can have a variable number of them) add the flag `--slowkeys` it is called slowkeys because you need to
iterate through the whole vcf file before you can create the columns (so twice as slow)

you can also use your own column keys and your own ordering of those keys by using:
`--keys ['CHROM'...]`

VCflat uses [Cyvcf2](https://github.com/brentp/cyvcf2) under the hood. Cyvcf2 *is a cython wrapper around [htslib](https://github.com/samtools/htslib)
 built for fast parsing of [Variant Call Format](https://en.m.wikipedia.org/wiki/Variant_Call_Format) (VCF) files.*