#!/usr/bin/env python


"""

Copyright (c) 2020, Konrad Foerstner <konrad@foerstner.org>

Permission to use, copy, modify, and/or distribute this software for
any purpose with or without fee is hereby granted, provided that the
above copyright notice and this permission notice appear in all
copies.

THE SOFTWARE IS PROVIDED 'AS IS' AND THE AUTHOR DISCLAIMS ALL
WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL
DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR
PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.

"""

__description__ = ""
__author__ = "Konrad Foerstner <konrad@foerstner.org>"
__copyright__ = "2020 by Konrad Foerstner <konrad@foerstner.org>"
__license__ = "ISC license"
__email__ = "konrad@foerstner.org"
__version__ = ""

import argparse
import urllib.request
import json
import os
import pathlib
import subprocess
import time


def main():
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("--input_file", required=True)
    parser.add_argument("--output_folder", default="crossref_json")
    parser.add_argument("--wikidata_cli_executable", default="wd")
    args = parser.parse_args()
    crossref_base_url = "https://api.crossref.org/works/"

    dois = [line.strip() for line in open(args.input_file)]
    for doi in dois[728:860]:
        print(doi)

        if item_exists(doi, args.wikidata_cli_executable):
            continue
        metadata = get_metadata_from_crossref(doi, args.output_folder)
        if len(metadata) == 0:
            print("No Metadata")
            continue
        create_new_item(metadata, args.wikidata_cli_executable)
        time.sleep(3)


def create_new_item(metadata, wikidata_cli_executable):
    if metadata["institution"]["name"] == "bioRxiv":
        serve_q_number = "Q19835482"
    elif metadata["institution"]["name"] == "medRxiv":
        serve_q_number = "Q58465838"
    authors = _generate_author_list(metadata)
    entity_dict = {
        "labels": {"en": metadata["title"][0]},
        "descriptions": {"en": "scientific article (preprint)"},
        "claims": {
            "P31": "Q13442814",  # scholarly article
            "P356": metadata["DOI"],
            "P1433": serve_q_number,
            "P1476": {"text": metadata["title"][0], "language": "en"},
            "P577": metadata["created"]["date-time"].split("T")[0],
            "P2093": authors,
            "P921": ["Q84263196", "Q82069695", "Q81068910"],
            "P407": "Q1860",
        },
    }
    tmp_json_file = "tmp.json"
    with open(tmp_json_file, "w") as entity_json_fh:
        entity_json_fh.write(json.dumps(entity_dict))

    creation_result = subprocess.check_output(
        f"{wikidata_cli_executable} create-entity ./{tmp_json_file}".split()
    )
    print(creation_result)


def _generate_author_list(metadata):
    authors = []
    for author in metadata["author"]:
        if (not "given" in author.keys()) or (not "family" in author.keys()):
            continue
        authors.append(f"{author['given']} {author['family']}")
    return authors


def get_metadata_from_crossref(
    doi, output_folder, crossref_base_url="https://api.crossref.org/works"
):

    pathlib.Path(output_folder).mkdir(exist_ok=True)
    json_file_path = f"{output_folder}/{doi.replace('/', '_')}.json"
    if not os.path.isfile(json_file_path):
        try:
            urllib.request.urlretrieve(f"{crossref_base_url}/{doi}", json_file_path)
        except urllib.error.HTTPError:
            return {}
    metadata = json.load(open(json_file_path))["message"]
    return metadata


def item_exists(doi, wikidata_cli_executable):
    """
    Check by querying fors items with that DOI.
    """

    tmp_sparql_file = "tmp.sparql"
    with open(tmp_sparql_file, "w") as output_fh:
        sparql_query = f'SELECT ?jo WHERE {{?jo wdt:P356 "{doi}".}}'
        output_fh.write(sparql_query)
    try:
        query_result = subprocess.check_output(
            f"{wikidata_cli_executable} sparql "
            f"{tmp_sparql_file} -e https://query.wikidata.org/sparql".split()
        )
    except subprocess.CalledProcessError:
        return False
    # If this string is return the item is not existing
    return not "no result found" in str(query_result)


main()
