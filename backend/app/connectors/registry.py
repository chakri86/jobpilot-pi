from app.connectors.base import BaseJobConnector
from app.connectors.mock_connector import MockJobConnector


def get_connector(source_type: str) -> BaseJobConnector:
    if source_type == "mock":
        return MockJobConnector()
    raise ValueError(f"Unsupported source type: {source_type}")
