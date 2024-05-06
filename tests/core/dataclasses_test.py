from ya_business_api.core.dataclasses import ValidatedMixin

from dataclasses import dataclass
from typing import List
from unittest.mock import patch

import pytest


@dataclass
class EmptyDataclass(ValidatedMixin):
	pass


@dataclass
class FilledDataclass(ValidatedMixin):
	a: str
	b: int
	c: List[str]


class TestValidatedMixin:
	def test___post_init__(self):
		with patch.object(EmptyDataclass, "__post_init__") as post_init_method:
			EmptyDataclass()
			post_init_method.assert_called_once()

		with patch.object(EmptyDataclass, "_validate_attrs") as validate_attrs_method:
			EmptyDataclass()
			validate_attrs_method.assert_called_once()

	def test__validate_attrs(self):
		EmptyDataclass()

		with pytest.raises(AssertionError, match="Attribute a must be of the <class 'str'> type"):
			FilledDataclass(a=1, b=2, c=[3])		# type: ignore - For testing purposes

		FilledDataclass(a="1", b=2, c=[3])		# type: ignore - For testing purposes

	def test__get_annotations_to_validate(self):
		assert set(EmptyDataclass()._get_annotations_to_validate()) == set()
		assert set(FilledDataclass(a='1', b=2, c=['3'])._get_annotations_to_validate()) == {
			('a', str),
			('b', int),
			('c', List[str]),
		}
