# -*- coding: utf-8 -*-
######################################################
#     _____                  _____      _     _      #
#    (____ \       _        |  ___)    (_)   | |     #
#     _   \ \ ____| |_  ____| | ___ ___ _  _ | |     #
#    | |  | )/ _  |  _)/ _  | |(_  / __) |/ || |     #
#    | |__/ ( ( | | | ( ( | | |__| | | | ( (_| |     #
#    |_____/ \_||_|___)\_||_|_____/|_| |_|\____|     #
#                                                    #
#    Copyright (c) 2022 Kangas Development Team      #
#    All rights reserved                             #
######################################################

import io
import json
import logging
import math
import urllib

import numpy as np
import PIL.Image
from matplotlib import cm

from .._typing import IO, Any, Optional, Sequence, Union
from .base import Asset
from .utils import (
    _verify_box,
    convert_tensor_to_numpy,
    download_filename,
    flatten,
    generate_image,
    get_file_extension,
    image_to_fp,
    is_valid_file_path,
    rescale_array,
)

LOGGER = logging.getLogger(__name__)


class Image(Asset):
    """
    An Image asset.
    """

    ASSET_TYPE = "Image"

    def __init__(
        self,
        data=None,
        name=None,
        format="png",
        scale=1.0,
        shape=None,
        colormap=None,
        minmax=None,
        channels="last",
        metadata=None,
        source=None,
        unserialize=False,
        color_order="rgb",
    ):
        """
        Logs the image.

        Args:
            data: Required if source not given. data is one of the following:
                - a path (string) to an image
                - a file-like object containing an image
                - a numpy matrix
                - a TensorFlow tensor
                - a PyTorch tensor
                - a list or tuple of values
                - a PIL Image
            name: String - Optional. A custom name to be displayed on the dashboard.
                If not provided the filename from the `data` argument will be
                used if it is a path.
            format: Optional. String. Default: 'png'. If the data is
                actually something that can be turned into an image, this is the
                format used. Typical values include 'png' and 'jpg'.
            scale: Optional. Float. Default: 1.0. If the data is actually
                something that can be turned into an image, this will be the new
                scale of the image.
            shape: Optional. Tuple. Default: None. If the data is actually
                something that can be turned into an image, this is the new shape
                of the array. Dimensions are (width, height) or (width, height, colors)
                where `colors` is 3 (RGB) or 1 (grayscale).
            colormap: Optional. String. If the data is actually something
                that can be turned into an image, this is the colormap used to
                colorize the matrix.
            minmax: Optional. (Number, Number). If the data is actually
                something that can be turned into an image, this is the (min, max)
                used to scale the values. Otherwise, the image is autoscaled between
                (array.min, array.max).
            channels: Optional. Default 'last'. If the data is
                actually something that can be turned into an image, this is the
                setting that indicates where the color information is in the format
                of the 2D data. 'last' indicates that the data is in (rows, columns,
                channels) where 'first' indicates (channels, rows, columns).
            color_order: Optional. Default 'rgb'. The color order of the incoming
                image data. Only applied when data is an array and color_order is
                "bgr".
        """
        super().__init__(source)
        if unserialize:
            # A function that takes the object to lookup
            self._unserialize = unserialize
            return
        if self.source is not None:
            filename = self.source
            self._log_metadata(
                name=name,
                filename=filename,
                extension=get_file_extension(filename),
            )
            if metadata:
                self._log_metadata(**metadata)

            return

        if data is None:
            raise TypeError("data cannot be None")

        file_like, size = _image_data_to_file_like_object(
            data,
            name,
            format,
            scale,
            shape,
            colormap,
            minmax,
            channels,
            self.metadata,
            color_order,
        )
        self.metadata["image"] = {"width": size[0], "height": size[1]}
        self.asset_data = file_like.read()
        if name:
            self.metadata["filename"] = name
            self.metadata["extension"] = get_file_extension(name)
        if metadata:
            self.metadata.update(metadata)

    def to_pil(self):
        """
        Return the image as a Python Image Library (PIL) image.

        Example:
        ```python
        >>> import kangas as kg
        >>> image = kg.Image("filename.jpg").to_pil()
        >>> image.show()
        ```
        """
        if self.source is not None:
            asset_data = self._get_asset_data_from_source(self.source)
        else:
            asset_data = self.asset_data
        return generate_image(asset_data)

    def _get_asset_data_from_source(self, asset_source):
        # Get the asset_data for an image source
        url_data = urllib.request.urlopen(asset_source)
        with io.BytesIO() as fp:
            fp.write(url_data.read())
            image = PIL.Image.open(fp)
            if image.mode == "CMYK":
                image = image.convert("RGB")
            asset_data = image_to_fp(image, "png").read()
        return asset_data

    def show(self):
        """
        Show the image.
        """
        return self.to_pil().show()

    def convert_to_source(self, filename=None):
        """
        A PNG filename to save the loaded image.

        Under development.
        """
        import PIL

        if self.source is not None:
            print("Skipping %s as it is already a source asset" % self.asset_id)
            return

        filename = filename if filename else "%s.png" % self.asset_id

        fp = io.BytesIO(self.asset_data)
        im = PIL.Image.open(fp)
        im.save(filename)

        sfilename = "file://%s" % filename
        self.source = sfilename
        self.asset_data = json.dumps({"source": sfilename})
        self.metadata["source"] = sfilename
        self.metadata["filename"] = filename
        self.metadata["extension"] = "png"

    def _init_annotations(self, layer_name):
        if not isinstance(layer_name, str):
            raise Exception("layer_name must be a string")

        if "annotations" not in self.metadata:
            # Structure:
            # {"annotations": [
            #    {"name": "LAYER-NAME",
            #     "data":
            #       {
            #         "label": [],
            #         "boxes": [] | "points": [] | "mask": mask,
            #         "score": score,
            #         "id": "some-id",
            #         "metadata": {},
            #       }
            # }
            self.metadata["annotations"] = []
        if "labels" not in self.metadata:
            self.metadata["labels"] = {}

        layer = self._get_layer(self.metadata["annotations"], layer_name)
        if layer is None:
            self.metadata["annotations"].append({"name": layer_name, "data": []})

    def _get_layer(self, annotations, layer_name):
        for layer in annotations:
            if layer["name"] == layer_name:
                return layer
        return None

    def _update_annotations(self, layer_name, data):
        layer = self._get_layer(self.metadata["annotations"], layer_name)
        layer["data"].append(data)

        label = data["label"]
        if label not in self.metadata["labels"]:
            self.metadata["labels"][label] = 1
        else:
            self.metadata["labels"][label] += 1

    def add_regions(
        self,
        label=None,
        *regions,
        score=None,
        layer_name="(uncategorized)",
        id=None,
        **metadata
    ):
        """
        Add polygon regions to an image.

        Args:
            layer_name: (str) the layer for the label and regions
            label: (str) the label for the regions
            regions: list or tuples of at least 3 points
            score: (optional, number) a score associated
               with the region.
            id: (optional, str) an id associated
               with the region.

        Example:
        ```python
        >>> image = Image()
        >>> image.add_regions("Predictions", "car", [(x1, y1), ...], [(x2, y2), ...])
        ```
        """
        if not isinstance(layer_name, str):
            raise Exception("layer_name must be a string")

        if not isinstance(label, str):
            raise Exception("label must be a string")

        self._init_annotations(layer_name)
        self._update_annotations(
            layer_name,
            {
                "label": label,
                "points": list(regions),
                "boxes": None,
                "score": score,
                "id": id,
                "metadata": metadata,
            },
        )
        return self

    def add_bounding_boxes(
        self,
        label=None,
        *boxes,
        score=None,
        layer_name="(uncategorized)",
        id=None,
        **metadata
    ):
        """
        Add bounding boxes to an image.

        Args:
            layer_name: (str) the layer for the label and bounding boxes
            label: (str) the label for the regions
            boxes: list or tuples of exactly 2 points (top-left, bottom-right),
                or 4 ints (x, y, width, height)
            score: (optional, number) a score associated with the region.
            id: (optional, str) an id associated
               with the region.

        Example:
        ```python
        >>> image = Image()
        >>> box1 = [(x1, y1), (x2, y2)]
        >>> box2 = [x, y, width, height]
        >>> image.add_bounding_boxes("Truth", "Person", box1, box2, score=0.99)
        >>> image.add_bounding_boxes("Prediction", "Person", box1, score=0.4)
        ```
        """
        if not isinstance(layer_name, str):
            raise Exception("layer_name must be a string")

        if not isinstance(label, str):
            raise Exception("label must be a string")

        self._init_annotations(layer_name)
        self._update_annotations(
            layer_name,
            {
                "label": label,
                "boxes": [_verify_box(box) for box in boxes],
                "points": None,
                "score": score,
                "id": id,
                "metadata": metadata,
            },
        )
        return self

    def add_bounding_box(
        self,
        label=None,
        box=None,
        score=None,
        layer_name="(uncategorized)",
        id=None,
        **metadata
    ):
        """
        Add a bounding box to an image.

        Args:
            layer_name: (str) the layer for the label and bounding boxes
            label: (str) the label for the regions
            box: exactly 2 points (top-left, bottom-right),
                or 4 ints (x, y, width, height)
            score: (optional, number) a score associated with the region.
            id: (optional, str) an id associated
               with the region.

        Example:
        ```python
        >>> image = Image()
        >>> box = [(x1, y1), (x2, y2)]
        >>> image.add_bounding_box("Truth", "Person", box, 0.56)
        ```
        """
        if not isinstance(layer_name, str):
            raise Exception("layer_name must be a string")

        if not isinstance(label, str):
            raise Exception("label must be a string")

        self._init_annotations(layer_name)
        self._update_annotations(
            layer_name,
            {
                "label": label,
                "boxes": [_verify_box(box)],
                "points": None,
                "score": score,
                "id": id,
                "metadata": metadata,
            },
        )
        return self

    def add_mask(
        self,
        label_map=None,
        image=None,
        score=None,
        layer_name="(uncategorized)",
        id=None,
        **metadata
    ):
        """
        Add a mask to an image.

        Args:
            layer_name: (str) the layer for the label
            label_map: (str) the label for the regions
            image: (Image) a DataGrid Image instance of the mask
            score: (optional, number) a score associated with the region.
            id: (optional, str) an id associated
               with the region.

        Under development.

        Example:
        ```python
        >>> image = Image()
        >>> image.add_mask("Predictions", "attention", {0: "person"}, Image(MASK))
        >>> image.add_mask("Ground Truth", "attention", {0: "person"}, Image(MASK))
        ```
        """
        if not isinstance(layer_name, str):
            raise Exception("layer_name must be a string")

        if not isinstance(image, Image):
            raise ValueError(
                "Image.add_mask() requires a layer_name, label_map, and mask image"
            )

        self._init_annotations(layer_name)
        self._update_annotations(
            layer_name,
            {
                "label": label_map,
                "mask": image,
                "boxes": None,
                "points": None,
                "score": score,
                "id": id,
                "metadata": metadata,
            },
        )
        return self

    def add_annotations(
        self,
        text=None,
        anchor=None,
        *points,
        score=None,
        layer_name="(uncategorized)",
        id=None,
        **metadata
    ):
        """
        Add an annotation to an image.

        Under development.

        Example:
        ```python
        >>> image = Image()
        >>> image.add_annotations("General", "Tumors", (50, 50), (100, 100), (200, 200), ...)
        ```
        """
        if not isinstance(layer_name, str):
            raise Exception("layer_name must be a string")

        if not isinstance(text, str):
            raise Exception("text must be a string")

        self._init_annotations(layer_name)
        self._update_annotations(
            layer_name,
            {
                "label": text,
                "annotation": [list(anchor), list(points)],
                "score": score,
                "id": id,
                "metadata": metadata,
            },
        )
        return self


def _image_data_to_file_like_object(
    image_data,
    file_name,
    image_format,
    image_scale,
    image_shape,
    image_colormap,
    image_minmax,
    image_channels,
    metadata,
    color_order,
):
    # type: (Union[IO[bytes], Any], Optional[str], str, float, Optional[Sequence[int]], Optional[str], Optional[Sequence[float]], str, Optional[Any]) -> Union[IO[bytes], None, Any]
    """
    Ensure that the given image_data is converted to a file_like_object ready
    to be uploaded
    """
    ## Conversion from standard objects to image
    ## Allow file-like objects, numpy arrays, etc.

    image_data = download_filename(image_data)

    if is_valid_file_path(image_data):
        metadata["extension"] = get_file_extension(image_data)
        metadata["filename"] = image_data
        file_contents = open(image_data, "rb")
        image = PIL.Image.open(image_data)
        return file_contents, image.size
    elif hasattr(image_data, "numpy"):  # pytorch tensor
        array = convert_tensor_to_numpy(image_data)
        results = _array_to_image_fp_size(
            array,
            image_format,
            image_scale,
            image_shape,
            image_colormap,
            image_minmax,
            image_channels,
            color_order,
        )
        return results
    elif hasattr(image_data, "eval"):  # tensorflow tensor
        array = image_data.eval()
        results = _array_to_image_fp_size(
            array,
            image_format,
            image_scale,
            image_shape,
            image_colormap,
            image_minmax,
            image_channels,
            color_order,
        )
        return results
    elif isinstance(image_data, PIL.Image.Image):  # PIL.Image
        # If CMYK, then needs a conversion:
        if image_data.mode == "CMYK":
            image_data = image_data.convert("RGB")
        ## filename tells us what format to use:
        if file_name is not None and "." in file_name:
            _, image_format = file_name.rsplit(".", 1)
        results = image_to_fp(image_data, image_format), image_data.size
        return results
    elif image_data.__class__.__name__ == "ndarray":  # numpy array
        results = _array_to_image_fp_size(
            image_data,
            image_format,
            image_scale,
            image_shape,
            image_colormap,
            image_minmax,
            image_channels,
            color_order,
        )
        return results
    elif hasattr(image_data, "read"):  # file-like object
        return image_data
    elif isinstance(image_data, (tuple, list)):  # list or tuples
        array = np.array(image_data)
        results = _array_to_image_fp_size(
            array,
            image_format,
            image_scale,
            image_shape,
            image_colormap,
            image_minmax,
            image_channels,
            color_order,
        )
        return results
    else:
        LOGGER.error("invalid image file_type: %s", type(image_data))
        return None


def _array_to_image_fp_size(
    array,
    image_format,
    image_scale,
    image_shape,
    image_colormap,
    image_minmax,
    image_channels,
    color_order,
):
    # type: (Any, str, float, Optional[Sequence[int]], Optional[str], Optional[Sequence[float]], str) -> Optional[IO[bytes]]
    """
    Convert a numpy array to an in-memory image
    file pointer.
    """
    if isinstance(color_order, str) and color_order.lower() == "bgr":
        array = array[..., ::-1].copy()
    image = _array_to_image(
        array, image_scale, image_shape, image_colormap, image_minmax, image_channels
    )
    if not image:
        return None
    return image_to_fp(image, image_format), image.size


def _array_to_image(
    array,
    image_scale=1.0,
    image_shape=None,
    image_colormap=None,
    image_minmax=None,
    image_channels=None,
    mode=None,
):
    # type: (Any, float, Optional[Sequence[int]], Optional[str], Optional[Sequence[float]], Optional[str], Optional[str]) -> Optional[Any]
    """
    Convert a numpy array to an in-memory image.
    """
    array = np.array(array)

    ## Handle image transformations here
    ## End up with a 0-255 PIL Image
    if image_minmax is not None:
        minmax = image_minmax
    else:  # auto minmax
        flatten_array = flatten(array)
        min_array = min(flatten_array)
        max_array = max(flatten_array)
        if min_array == max_array:
            min_array = min_array - 0.5
            max_array = max_array + 0.5
        min_array = math.floor(min_array)
        max_array = math.ceil(max_array)
        minmax = [min_array, max_array]

    ## if a shape is given, try to reshape it:
    if image_shape is not None:
        try:
            ## array shape is opposite of image size(width, height)
            if len(image_shape) == 2:
                array = array.reshape(image_shape[1], image_shape[0])
            elif len(image_shape) == 3:
                array = array.reshape(image_shape[1], image_shape[0], image_shape[2])
            else:
                raise Exception(
                    "invalid image_shape: %s; should be 2D or 3D" % image_shape
                )
        except Exception:
            LOGGER.info("WARNING: invalid image_shape; ignored", exc_info=True)

    if image_channels == "first" and len(array.shape) == 3:
        array = np.moveaxis(array, 0, -1)
    ## If 3D, but last array is flat, make it 2D:
    if len(array.shape) == 3:
        if array.shape[-1] == 1:
            array = array.reshape((array.shape[0], array.shape[1]))
        elif array.shape[0] == 1:
            array = array.reshape((array.shape[1], array.shape[2]))
    elif len(array.shape) == 1:
        ## if 1D, make it 2D:
        array = np.array([array])

    ### Ok, now let's colorize and scale
    if image_colormap is not None:
        ## Need to be in range (0,1) for colormapping:
        array = rescale_array(array, minmax, (0, 1), "float")
        try:
            cm_hot = cm.get_cmap(image_colormap)
            array = cm_hot(array)
        except Exception:
            LOGGER.info("WARNING: invalid image_colormap; ignored", exc_info=True)
        ## rescale again:
        array = rescale_array(array, (0, 1), (0, 255), "uint8")
        ## Convert to RGBA:
        image = PIL.Image.fromarray(array, "RGBA")
    else:
        ## Rescale (0, 255)
        array = rescale_array(array, minmax, (0, 255), "uint8")
        image = PIL.Image.fromarray(array)

    if image_scale != 1.0:
        image = image.resize(
            (int(image.size[0] * image_scale), int(image.size[1] * image_scale))
        )

    ## Put in a standard mode:
    if mode:
        image = image.convert(mode)
    elif image.mode not in ["RGB", "RGBA"]:
        image = image.convert("RGB")
    return image
