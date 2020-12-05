# EU Regulation Corpus Compiler

A set of Python programs to retrieve EU regulatory documents from the Eur-Lex portal (https://eur-lex.europa.eu). 

The program uses a given SPARQL query to retrieve CELLAR records from the EU Sparql endpoint and download the corresponding `.xml` and `.html` files from the EU CELLAR endpoint.

The program also checks whether the files have already been downloaded so as to download only new files.

## Usage

Run `get_cellar_docs.py` to send the SPARQL query to EU Sparql endpoint and download the files corresponding to the returned CELLAR ids. 

## SPARQL query

The SPARQL query in the `sparql_queries/` directory was designed to retrieve EU regulatory documents in the financial domain using EuroVoc concept ids. It can be used as a template to create new queries for other domains, langages, types of documents, etc.

## Author
Selja Seppälä
(selja.seppala@ucc.ie)

## Acknowledgements
These programs were developed as part of "RegDef: A Computer-assisted Definition Authoring and Formalisation System for Legal Experts". The RegDef project is co-funded by a Marie Skłodowska-Curie Career-FIT Fellowship and Enterprise Ireland. Further details on the RegDef project are available at https://seljaseppala.wordpress.com/research/regdef/.

Career-FIT has received funding from the European Union’s Horizon2020 research and innovation programme under the Marie Skłodowska-Curie grant agreement No. 713654
