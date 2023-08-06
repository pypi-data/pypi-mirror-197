import re
from typing import Dict, List, Any, Union
from itertools import chain


class MetaJsonParser:
    """MetaJson parsing utilities."""

    @staticmethod
    def _parse_datetimes(value: str) -> bool:
        """Determine if a string is a potential datetime.

        Attributes
        ----------
        value: str
            Variable to evaluate.

        Returns
        -------
        bool
            True if a datetime, false otherwise.
        """
        re_list = [
            r"(\d{4}(\-|\/)(0\d|1[0-2])(\-|\/)(0\d|1\d|2\d|3[0-1]))",
            r"((0\d|1\d|2\d|3[0-1])(\-|\/)(0\d|1[0-2])(\-|\/)\d{4})",
            r"((0\d|1[0-2])(\-|\/)(0\d|1\d|2\d|3[0-1])(\-|\/)\d{4})",
        ]
        rgx = re.compile("|".join(re_list))
        return bool(re.match(rgx, value))

    def types_parser(self, response: Any) -> Union[Union[Dict, List], str]:
        """Given a JSON response, create a dictionary with the value types
        instead of the actual values.

        Attributes
        ----------
        response:
            Deserialized JSON response, could be total or partial.

        Return
        -------
        list, dict, str
            Same response but with data types instead of values.
        """
        if isinstance(response, dict):
            return {k: self.types_parser(v) for k, v in response.items()}
        elif isinstance(response, list):
            return [self.types_parser(r) for r in response]
        else:
            if self._parse_datetimes(str(response)):
                return "datetime"
            return re.sub("(<class '|'>)", "", str(type(response)))

    def _hard_flatten(self, vals: List) -> List:
        """Chain nested lists into a new one.

        Attributes
        ----------
        vals: list
            List with nested lists.

        Returns
        -------
        list
            List with all previous nested values.
        """
        # fmt: off
        flat_list = map(lambda x: self._hard_flatten(x) if isinstance(
            x, list) else [x], vals)
        return [*chain(*flat_list)]

    def attribute_parser(self, response: Any) -> List:
        """Given a JSON response, create a list grouping its attributes.

        Attributes
        ----------
        response:
            Deserialized JSON response, could be total or partial.

        Returns
        -------
        list
            List with grouped keys lists [primary keys, subkeys].
        """
        # fmt: off
        if isinstance(response, dict):
            return [list(response.keys()),
                    self.attribute_parser(list(response.values()))]
        elif isinstance(response, list):
            return self._hard_flatten(
                    [self.attribute_parser(r) for r in response])
        else:
            return []

    def _soft_flatten(self, vals: List) -> List:
        """Turn double braces into one.

        Attributes
        ----------
        vals: list
            List with nested lists.

        Returns
        -------
        list
            List with reduced braces.
        """
        new_list = map(lambda x: x if isinstance(x, list) else [x], vals)
        return [*chain(*new_list)]

    def layer_parser(self, response: Any) -> List:
        """Given a JSON response, create a list showing attributes'
        depth per layer.

        Attributes
        ----------
        response:
            Deserialized JSON response, could be total or partial.

        Returns
        -------
        list
            List with key pairs [key, [subkeys]].
        """
        if isinstance(response, dict):
            return [[k, self.layer_parser(v)] for k, v in response.items()]
        elif isinstance(response, list):
            return self._soft_flatten([self.layer_parser(r) for r in response])
        else:
            return []

    def layer_processing(self, parsed_layer: List) -> List:
        """Create a list with sorted attribute layers from a previously parsed
        response into layers.

        Attributes
        ----------
        parsed_layer: list
            Result from layer_parser method.

        Returns
        -------
        list
            List with grouped attributes per layer [[layer1], [layer2]...].
        """
        layers = []
        while len(parsed_layer) > 0:
            layers.append([p.pop(0) for p in parsed_layer if len(p) > 0])
            bring_next = [p[0] for p in parsed_layer if len(p) > 0]
            parsed_layer = [*chain(*filter(lambda x: x != [], bring_next))]
        return layers

    @staticmethod
    def layers_retrieval(processed_layer: List) -> Dict:
        """Create a dictionary with the processed attribute layers.

        Attributes
        ----------
        processed_layer: list
            Result from layer_processing method.

        Returns
        -------
        dict
            Dictionary with attributes per layer {"layer_0": [attributes],...}.
        """
        return {f"layer_{idx}": val for idx, val in enumerate(processed_layer)}
