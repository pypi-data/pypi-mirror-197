from __future__ import annotations
from typing import Dict, List, Tuple, Optional
from uuid import UUID

from drb.core.item_class import ItemClass
from drb.core.node import DrbNode
from drb.exceptions.core import DrbException
from drb.metadata.metadata import _retrieve_cortex_file
from drb.topics import resolver
from drb.utils.plugins import get_entry_points
from drb.extractor import Extractor
from drb.extractor.extractor import __factories
from drb.topics.resolver import ItemClassLoader
import os
import jsonschema
import yaml
import importlib
import logging

_logger = logging.getLogger('DrbImage')
_schema = os.path.join(os.path.dirname(__file__), 'schema.yml')


def parse_extractor(data: dict):
    for key, value in data.items():
        return __factories[key](value)


def validate_md_cortex_file(path: str) -> None:
    """
    Checks the given metadata cortex file is valid.

    Parameters:
        path (str): metadata cortex file path

    Raises:
        DrbException: If the given cortex file is not valid
    """
    with open(_schema) as f:
        schema = yaml.safe_load(f)
    f.close()

    with open(path) as file:
        for data in yaml.safe_load_all(file):
            try:
                jsonschema.validate(data, schema)
            except jsonschema.ValidationError as ex:
                file.close()
                raise DrbException(
                    f'Invalid metadata cortex file: {path}') from ex
        file.close()


def _load_image(yaml_data: dict) -> Tuple[UUID, list[Image], str]:
    uuid = UUID(yaml_data['topic'])
    names = list(yaml_data['image'].keys())
    res = []
    for name in names:
        freq = []

        if 'freq' in yaml_data['image'][name]:
            freq = yaml_data['image'][name]['freq']

        for data in yaml_data['image'][name]['source']:
            if 'extractor' in data.keys():
                extractor = parse_extractor(data['extractor'])
                res.append(Image(name=name,
                                 extractor=extractor,
                                 freq=freq,
                                 data=data)
                           )

    return uuid, res, yaml_data.get('default', None)


def _load_all_image() -> Dict[UUID, Tuple[List[Image], str]]:
    """
    Loads all metadata defined in the current Python environment
    with the entry points drb.image.
    """
    entry_point_group = 'drb.image'
    image = {}

    for ep in get_entry_points(entry_point_group):
        try:
            module = importlib.import_module(ep.value)
        except ModuleNotFoundError as ex:
            _logger.warning(f'Invalid DRB Image entry-point {ep}: {ex.msg}')
            continue

        try:
            cortex = _retrieve_cortex_file(module)
            validate_md_cortex_file(cortex)
        except (FileNotFoundError, DrbException) as ex:
            _logger.warning(ex)
            continue

        with open(cortex) as file:
            for data in yaml.safe_load_all(file):
                uuid, img, default = _load_image(data)
                image[uuid] = (img, default)
    return image


class Image:
    def __init__(self, name: str, extractor: Extractor,
                 freq: str = None, data: dict = {}):
        self._name = name
        self.extractor = extractor
        self._freq = freq
        self._data = data

    def __getattr__(self, item):
        if item in self._data.keys():
            return self._data[item]
        raise AttributeError

    @property
    def name(self) -> str:
        """
        Provide the name of the image.
        """
        return self._name

    @property
    def freq(self) -> List:
        """
        Provide the frequency of the image with a list
         of int, the default value is an empty list.
        """
        return self._freq

    @property
    def addon_data(self) -> Optional[dict]:
        """
        Provide the raw data of the image addon,
        in the dict format.
        in the dict format.
        """
        return self._data

    def node(self, node: DrbNode) -> DrbNode:  # DrbImageNode
        """
        Provides the current image as a DrbNode
        """
        return self.extractor.extract(node)


class AddonImage:
    @staticmethod
    def images(source) -> List[str]:
        """
        Returns available images list that can be generated
        Parameters:
          source (DrbNode, Topic):
        """
        _images = _load_all_image()
        res = []

        if isinstance(source, DrbNode) or isinstance(source, str):
            topic, node = resolver.resolve(source)
        elif isinstance(source, ItemClass):
            topic = source
        else:
            raise DrbException(
                f"Cannont find any image addon corresponding to {source}")

        if topic.id in _images.keys():
            for e in _images[topic.id][0]:
                res.append(e.name)
        if topic.parent_class_id is not None and \
                topic.parent_class_id in _images.keys():
            res.append(AddonImage.images(
                ItemClassLoader().get_item_class(topic.parent_class_id)
            ))

        return res

    @staticmethod
    def create(node: DrbNode,
               image_name: str = None,
               freq: int = None, **kwargs) -> Image:
        """
        Create a new image representation on the node
        Parameters:
          node (DrbNode): an image will be generated from that node
          image_name (str): (default ``None``)
          freq (int): (default ``None``)
          resolution (str): (default ``None``)
        """
        _images = _load_all_image()

        topic, node = resolver.resolve(node)

        try:
            tmp = _images[topic.id]
        except IndexError:
            raise DrbException(f"No descriptor found for node {node.name}")

        options = list(kwargs.keys())
        res = tmp[0]

        if image_name is not None:
            remove = []
            for t in res:
                if t.name != image_name:
                    remove.append(t)
            res = list(set(res) - set(remove))

        if freq is not None:
            remove = []
            freq = int(freq)
            for t in res:
                if len(t.freq) == 2:
                    if not t.freq[0] <= freq <= t.freq[1]:
                        remove.append(t)
                else:
                    remove.append(t)
            res = list(set(res) - set(remove))

        if options:
            remove = []
            for opt in options:
                for t in res:
                    try:
                        if t.__getattr__(opt) != kwargs[opt]:
                            remove.append(t)
                    except AttributeError:
                        pass
            res = list(set(res) - set(remove))

        if image_name is None and freq is None and not kwargs:
            remove = []
            if tmp[1] is not None:
                for t in res:
                    if t.name != tmp[1]:
                        remove.append(t)
                res = list(set(res) - set(remove))

        try:
            return res[0]
        except IndexError:
            raise DrbException(f'No image descriptor found for '
                               f'{image_name}, {freq}, {kwargs}')
