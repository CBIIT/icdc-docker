import flask
import json
import requests

from pidgin.errors import *
from pidgin.constants import *


app = flask.Flask(__name__)

app_info = {
    "swagger": "2.0",
    "info": {
        "title": "Pidgin OpenAPI Specification",
        "description": "A core metadata API for CDIS Gen 3 data commons. Code is available on [GitHub](https://github.com/uc-cdis/pidgin).",
        "version": "1.0",
        "termsOfService": "http://cdis.uchicago.edu/terms/",
        "contact": {
            "email": "cdis@uchicago.edu"
        },
        "license": {
            "name": "Apache 2.0",
            "url": "http://www.apache.org/licenses/LICENSE-2.0.html"
        }
    }
}


@app.route('/<path:object_id>')
def get_core_metadata(object_id):
    """
    Get core metadata from an object_id
    ---
    tags:
      - core_metadata
    produces:
      - application/json
      - x-bibtex
      - application/vnd.schemaorg.ld+json
    parameters:
      - name: object_id
        in: path
        type: string
        required: true
      - name: Accept
        in: header
        type: string
        enum: [application/json (default), x-bibtex, application/vnd.schemaorg.ld+json]
    responses:
      200:
        description: OK
        examples:
            application/json:
                '{"file_name": "my-file.txt", "data_format": "TXT", "file_size": 10, "object_id": "123"}'
            x-bibtex:
                '@misc {123, file_name = "my-file.txt", data_format = "TXT", file_size = "10", object_id = "123"}'
      401:
        description: Authentication error
      404:
        description: No core metadata was found for this object_id
    """
    accept = flask.request.headers.get('Accept')
    if accept == "x-bibtex":
        return get_bibtex_metadata(object_id)
    elif accept == "application/vnd.schemaorg.ld+json":
        return get_schemaorg_json_metadata(object_id)
    else: # accept == "application/json" or no accept header
        return get_json_metadata(object_id)


def get_schemaorg_json_metadata(object_id):
    """
    Get core metadata as a Schema.org JSON from an object_id.
    """
    try:
        metadata = get_metadata_dict(object_id)
        schemaorg = {
            "@context": "http://schema.org",
            "@type": "Dataset",
            "@id": "https://dataguids.org/index/" + object_id,
            "identifier": [
                {
                    "@type": "PropertyValue",
                    "propertyID": "dataguid",
                    "value": object_id
                },
                {
                    "@type": "PropertyValue",
                    "propertyID": "md5",
                    "value": metadata["md5sum"]
                }
            ]
        }
        if "publisher" in metadata:
            schemaorg["publisher"] = { "@type": "Organization", "name": metadata["publisher"]}
        if "creator" in metadata:
            schemaorg["author"] = {"name": metadata["creator"]}
        if "description" in metadata:
            schemaorg["description"] = metadata["description"]
        if "type" in metadata:
            schemaorg["additionalType"] = metadata["type"]
        if "file_name" in metadata:
            schemaorg["name"] = metadata["file_name"]
        if "updated_datetime" in metadata:
            schemaorg["datePublished"] = metadata["updated_datetime"]

  #"schemaVersion": "http://datacite.org/schema/kernel-4",

        return json.dumps(schemaorg) # translate dictionary to json
    except PidginException as e:
        return e.message, e.code


def get_json_metadata(object_id):
    """
    Get core metadata as JSON from an object_id.
    """
    try:
        metadata = get_metadata_dict(object_id)
        return json.dumps(metadata) # translate dictionary to json
    except PidginException as e:
        return e.message, e.code


def get_bibtex_metadata(object_id):
    """
    Get core metadata as BibTeX from an object_id.
    """
    try:
        metadata = get_metadata_dict(object_id)
        return translate_dict_to_bibtex(metadata)
    except PidginException as e:
        return e.message, e.code


def get_metadata_dict(object_id):
    """
    Create a dictionary containing the metadata for a given object_id.
    """
    response = request_metadata(object_id) # query to peregrine
    metadata = flatten_dict(response)

    if all(field in metadata for field in CITATION_FIELDS):
        metadata['citation'] = generate_citation(metadata)

    return remove_unused_fields(metadata)


def translate_dict_to_bibtex(d):
    """
    Translate a dictionary to a BibTeX string.
    """
    items = ['{} = "{}"'.format(k, v) for k, v in d.items()]
    bibtex_items = ', '.join(items)
    bibtex_str = '@misc {' + d['object_id'] + ', ' + bibtex_items + '}'
    return bibtex_str


def flatten_dict(d):
    """
    Flatten a dictionary that contains core metadata.
    """
    flat_d = {}
    try:
        data_type = list(d['data'].keys())[0]
        for k, v in d['data'][data_type][0].items():
            if k == 'core_metadata_collections':
                if v:
                    # object_id is unique so the list should only contain one item
                    flat_d.update(v[0])
            else:
                flat_d[k] = v
    except (AttributeError, IndexError):
        error = 'Core metadata not available for this file'
        if 'errors' in d:
            error += ': ' + d['errors'][0]
        raise NoCoreMetadataException(error)
    return flat_d


def generate_citation(metadata_dict):
    """
    Generate a citation from the other metadata.
    """
    format_args = dict(metadata_dict)
    format_args['year'] = format_args.pop('updated_datetime').split('-')[0]
    format_string = '{creator}, {year}: {title}. {publisher}, {object_id}'
    return format_string.format(**format_args)


def remove_unused_fields(d):
    """
    Remove from the dictionary fields that should not be in the final output.
    """
    copy = dict(d)
    copy.pop('title', None)
    return copy


def get_file_type(object_id):
    """
    Get the type of file from the object_id.
    """
    query_txt = '{ datanode (object_id: "' + object_id + '") { type } }'
    response = send_query(query_txt)
    try:
        file_type = response['data']['datanode'][0]['type']
    except IndexError:
        raise ObjectNotFoundException('object_id "' + object_id + '" not found')
    return file_type


def request_metadata(object_id):
    """
    Write a query and transmit it to send_query().
    """
    file_type = get_file_type(object_id)
    response = send_query(build_query(object_id, file_type, True))

    # if the file has no core metadata, get the other metadata only
    if not has_core_metadata(response, file_type):
        response = send_query(build_query(object_id, file_type))

    return response


def has_core_metadata(response, file_type):
    """
    Return True if a query response contains core metadata, False otherwise.
    """
    try:
        # try to access the core_metadata
        response['data'][file_type][0]['core_metadata_collections'][0]
    except:
        return False
    return True


def build_query(object_id, file_type, get_core_metadata = False):
    """
    Build the query to get the core metadata.

    Args:
        object_id: the file's GUID.
        file_type: the type of file to query.
        get_core_metadata: True if core metadata can be queried for this file, False otherwise.
    """
    query_txt = '{{ {} (object_id: "{}") {{ '.format(file_type, object_id)
    if get_core_metadata:
        fields = ' '.join(CORE_METADATA_QUERY_FIELDS)
        query_txt += 'core_metadata_collections {{ {} }} '.format(fields)
    fields = ' '.join(METADATA_QUERY_FIELDS)
    query_txt += '{} }} }}'.format(fields)
    return query_txt


def send_query(query_txt):
    """
    Send a query to peregrine and return the jsonified response.
    """
    api_url = app.config.get('API_URL')
    if not api_url:
        raise PidginException('Pidgin is not configured with API_URL')

    auth = flask.request.headers.get('Authorization')
    query = {'query': query_txt}
    response = requests.post(api_url, headers={'Authorization': auth}, json=query)
    data = response.json()

    if response.status_code == 401 or response.status_code == 403:
        raise AuthenticationException(data['message'])

    return data


@app.route('/_status', methods=['GET'])
def health_check():
    """
    Health check endpoint
    ---
    tags:
      - system
    responses:
      200:
        description: Healthy
      default:
        description: Unhealthy
    """
    return 'Healthy', 200

