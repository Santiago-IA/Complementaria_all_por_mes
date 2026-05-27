# test/process/test_shared.py
import pytest
from process.shared import get_class_name

def test_get_class_name():

    module_name = "entity.example_entity"
    expected = "ExampleEntity"
    assert get_class_name(module_name.replace("_", " ")) == expected

    module_name = "entity.some example"
    expected = "SomeExample"
    assert get_class_name(module_name.replace("_", " ")) == expected

