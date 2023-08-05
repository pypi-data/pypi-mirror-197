from .relational_entity import TxpRelationalEntity
import txp.common.models.protos.models_pb2 as models_pb2
import google.protobuf.timestamp_pb2 as timestamp_pb2
import dataclasses
import datetime
from typing import Any


@dataclasses.dataclass
class AssetMetrics(TxpRelationalEntity):
    asset_type: str = ""
    last_seen: str = ""
    rpm: float = 0.0
    temperature: float = 0.0
    worked_hours: float = 0.0
    asset_id: str = ""

    @classmethod
    def firestore_collection_name(cls) -> str:
        return "asset_metrics"

    @classmethod
    def get_proto_class(cls):
        return models_pb2.AssetMetricsProto
