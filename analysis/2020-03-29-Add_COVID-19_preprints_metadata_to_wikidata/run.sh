#/bin/env bash

main(){
    readonly WDCLI="singularity exec ../../data/2020-03-29-wikidata-cli_Singularity_image/wikidata-cli_2020-03-29.sif /wikibase-cli/bin/wb"
    readonly INSTANCE="https://www.wikidata.org"
    readonly ENDPOINT="https://query.wikidata.org/sparql"
    # ${WDCLI} label Q1
    #${WDCLI} query --property P921 --object Q44559 --labels -e ${ENDPOINT}
    # ${WDCLI} sparql tmp.sparql -e ${ENDPOINT}

   python bin/add_wikidata_item_by_doi.py \
	   --input_file ../../data/2020-03-29-bioRxiv_and_medRxiv_COVID-19_DOI_list/DOI_of_COVID-19_preprints.txt \
          --wikidata_cli_executable "${WDCLI}"

}



main
