# flake8: noqa
import argparse
import dataclasses
from datetime import datetime
import sys
from typing import Any, Dict

import buildflow
from buildflow import Flow

# Parser to allow run time configuration of arguments
parser = argparse.ArgumentParser()
parser.add_argument('--gcp_project', type=str, required=True)
args, _ = parser.parse_known_args(sys.argv)

# Set up a subscriber for the source.
# If this subscriber does not exist yet BuildFlow will create it.
input_sub = buildflow.PubSubSource(subscription=f'projects/{args.gcp_project}/subscriptions/taxiride-sub')
# Set up a BigQuery table for the sink.
# If this table does not exist yet BuildFlow will create it.
output_table = buildflow.BigQuerySink(table_id=f'{args.gcp_project}.buildflow_walkthrough.taxi_ride_data')

# Define an output type for our pipeline.
# By using a dataclass we can ensure our python type hints are validated
# against the BigQuery table's schema.
@dataclasses.dataclass
class TaxiOutput:
    ride_id: str
    point_idx: int
    latitude: float
    longitude: float
    timestamp: datetime
    meter_reading: float
    meter_increment: float
    ride_status: str
    passenger_count: int

flow = Flow()

# Define our processor.
@flow.processor(source=input_sub, sink=output_table)
def process(element: Dict[str, Any]) -> TaxiOutput:
    return element

# Run our flow.
flow.run()