from __future__ import annotations

import librtree.ext as ext  # type: ignore
import json

from typing import Any, Callable, TextIO
from librtree.deserialise import Deserialise


class RTreeStyle(Deserialise):
    '''
    A Ruby wrapper around RTree styles, used in PostScript plotting.
    '''

    def __init__(self):
        self._style = None

    @classmethod
    def json_read(cls, io: TextIO) -> RTreeStyle:
        '''
        Create a new Style instance from JSON stream

        :param io: the stream from which to read JSON

        .. code-block:: python

           with open('file.style', 'r') as io:
               style = RTreeStyle.json_read(io)
        '''
        style: RTreeStyle = cls.__new__(cls)
        style._style = ext.RTreeStyle.json_read(io)
        return style

    @classmethod
    def from_json(cls, json: str) -> RTreeStyle:
        '''
        Create a new RTreeStyle instance from JSON string

        :param json: the JSON string
        '''
        return cls._deserialise_text(json, cls.json_read)

    @classmethod
    def from_list(cls, levels: list)  -> RTreeStyle:
        '''
        Create a new RtreeStyle instance from list (or tuple)
        of appropriate dicts.

        :param levels: a list of dicts, this will be converted
          to JSON and read by :meth:`from_json`

        .. code-block:: python

           style = RTreeStyle.from_list(
             [
               {
                 'fill': {
                   'rgb': (0.5, 0.5, 0.5)
                 },
                 'stroke': {
                   'rgb': (0, 0, 1),
                   'width': 3
                 }
               }
             ]
           )
        '''
        return cls.from_json(json.dumps(levels))
