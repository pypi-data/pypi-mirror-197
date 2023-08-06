from typing import Dict, List, Union
from meta_json.meta_json_parser import MetaJsonParser


class MetaJson:
    """MetaJson main module."""

    def __init__(self, response: Union[Dict, List]):
        """Run all parsers in constructor."""

        parser = MetaJsonParser()
        self._types = parser.types_parser(response)
        self._attributes = parser.attribute_parser(response)
        layers = parser.layer_processing(parser.layer_parser(response))
        self._layers = parser.layers_retrieval(layers)

    @property
    def types(self):
        """Return types result."""
        return self._types

    @property
    def attributes(self):
        """Return attributes result."""
        return self._attributes

    @property
    def layers(self):
        """Return layers result."""
        return self._layers
