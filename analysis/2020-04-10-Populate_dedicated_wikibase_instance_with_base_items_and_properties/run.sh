main(){
    readonly INSTANCE="https://preprints.wiki.opencura.com/"
    readonly ENDPOINT="https://query.wikidata.org/sparql"
    readonly WDCLI="singularity exec ../../data/2020-03-29-wikidata-cli_Singularity_image/wikidata-cli_2020-03-29.sif /wikibase-cli/bin/wb"
    add_base_properties
}

add_base_properties(){
   ${WDCLI} create-entity '{"type": "property", "labels":{"en": "published in"}}' -i ${INSTANCE}
   # ${WDCLI} create-entity '{"type": "property", "labels":{"en": "publication date"}}' -i ${INSTANCE}
   # ${WDCLI} create-entity '{"type": "property", "labels":{"en": "publication date"}}' -i ${INSTANCE}
}

add_scholarly_article(){
    ${WDCLI} label Q1 -i ${INSTANCE}
}


main
