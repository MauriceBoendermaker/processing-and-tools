import pytest
from unittest.mock import MagicMock
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from CargoHubV2.app.services.item_lines_service import (
    create_item_line,
    get_item_line,
    get_all_item_lines,
    update_item_line,
    delete_item_line,
)
from CargoHubV2.app.models.item_lines_model import ItemLine
from CargoHubV2.app.schemas.item_lines_schema import ItemLineCreate, ItemLineUpdate

SAMPLE_ITEM_LINE = {"name": "Line X", "description": "Test line"}

# Test create_item_line
def test_create_item_line():
    db = MagicMock()
    line_data = ItemLineCreate(**SAMPLE_ITEM_LINE)
    line = create_item_line(db, line_data.model_dump())

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(line)
    assert line.name == SAMPLE_ITEM_LINE["name"]

def test_create_item_line_integrity_error():
    db = MagicMock()
    db.commit.side_effect = IntegrityError("mock", "params", "orig")
    line_data = ItemLineCreate(**SAMPLE_ITEM_LINE)

    with pytest.raises(HTTPException):
        create_item_line(db, line_data.model_dump())

    db.rollback.assert_called_once()

# Test get_item_line
def test_get_item_line_found():
    db = MagicMock()
    db.query().filter().first.return_value = ItemLine(**SAMPLE_ITEM_LINE)

    result = get_item_line(db, 1)

    db.query().filter().first.assert_called_once()
    assert result.name == SAMPLE_ITEM_LINE["name"]

def test_get_item_line_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    result = get_item_line(db, 999)

    assert result is None
