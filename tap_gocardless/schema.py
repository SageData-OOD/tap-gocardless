import os
import json
from singer import metadata

# Reference: https://github.com/singer-io/getting-started/blob/master/docs/DISCOVERY_MODE.md#Metadata
STREAMS = {
    'events': {
        'key_properties': ['id'],
        'replication_method': 'INCREMENTAL',
        'replication_keys': ['created_at']
    },
    "mandates": {
        'key_properties': ['id'],
        'replication_method': 'INCREMENTAL',
        'replication_keys': ['created_at']
    },
    'payments': {
        'key_properties': ['id'],
        'replication_method': 'INCREMENTAL',
        'replication_keys': ['created_at']
    },
    'payouts': {
        'key_properties': ['id'],
        'replication_method': 'INCREMENTAL',
        'replication_keys': ['created_at']
    },
    'payout_items': {
        # DP: amount is part of the primary key, because payout items don't have their own ids
        # this is the closest that we can get to reality by having all fields in the payout item
        # make the primary key
        'key_properties': ["payout_id",  "payment_id", "type", "amount"],
        'replication_method': 'INCREMENTAL',
        'replication_keys': []
    },
    'refunds': {
        'key_properties': ['id'],
        'replication_method': 'INCREMENTAL',
        'replication_keys': ['created_at']
    },
    'tax_rates': {
        'key_properties': ['id'],
        'replication_method': 'FULL_TABLE',
        'replication_keys': []
    },
    'customers': {
        'key_properties': ['id'],
        'replication_method': 'INCREMENTAL',
        'replication_keys': ['created_at']
    }
}

def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)

def get_schemas():
    schemas = {}
    field_metadata = {}

    for stream_name, stream_metadata in STREAMS.items():
        schema_path = get_abs_path('schemas/{}.json'.format(stream_name))
        with open(schema_path) as file:
            schema = json.load(file)
        schemas[stream_name] = schema
        mdata = metadata.new()

        # Documentation: https://github.com/singer-io/getting-started/blob/master/docs/DISCOVERY_MODE.md#singer-python-helper-functions
        # Reference: https://github.com/singer-io/singer-python/blob/master/singer/metadata.py#L25-L44
        mdata = metadata.get_standard_metadata(
            schema=schema,
            key_properties=stream_metadata.get('key_properties', None),
            valid_replication_keys=stream_metadata.get('replication_keys', None),
            replication_method=stream_metadata.get('replication_method', None)
        )
        field_metadata[stream_name] = mdata

    return schemas, field_metadata
