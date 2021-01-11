# VCFlat: Changelog

## [0.2.1] Fast fixes

* `--anno` option bug fixes
* `--long_anno` added so that annotation that is long can be ignored (default set at 20)
* basic regexes implemented for the `--keys` option


## [0.2.0] Some major Things that broke quicky

* `--anno` option added to deal with multi annotated vcf files were
* minor fixes to the existing code

## [0.1.1] First real fixes

* Now extracts all annotations and not just the last one
* Generates a new row if there are more than one annotations per variant



## [0.1.0] Initial implementation 

* A simple parser that takes a vcf file and spits out a tab delimited files
* Very limited functionality