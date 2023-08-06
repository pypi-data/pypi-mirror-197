
import os
import sys

import pytest
from reproj import reproj
from shapely.geometry import shape



EXAMPLES = os.path.join(os.path.dirname(os.path.abspath(__file__)), "examples")
polygons = os.path.join(EXAMPLES, "polygons.shp")


@pytest.fixture
def example_shape():
    # https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry
    return shape({"type": "LineString", "coordinates": [(3, 1), (1, 3), (4, 4)]})


@pytest.fixture
def example_feature():
    # https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry
    return {"type": "Feature", "geometry": shape({"type": "LineString", "coordinates": [(3, 1), (1, 3), (4, 4)]}), "properties": {"id": 1}}


def test_reproj_point(point):
    assert reproj(point, 4326, 32630) == ???


def test_reproj_line(line):
    assert reproj(line, 4326, 32630) == ???


def test_reproj_polygon(polygon):
    assert reproj(polygon, 4326, 32630) == ???


def test_reproj_multipolygon(multipolygon):
    assert reproj(multipolygon, 4326, 32630) == ???


def test_bad_build_distance_array(example_raster_array):
    with pytest.raises(TypeError):
        reproj(???)

    with pytest.raises(ValueError):
        reproj(???)

    with pytest.raises(Exception):
        reproj(???)
