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

SAMPLE_ITEM_LINE = {"name": "Line A", "description": "Test line"}

# Test create_item_line
def test_create_item_line():
    db = MagicMock()
    line_data = ItemLineCreate(**SAMPLE_ITEM_LINE)
    line = create_item_line(db, line_data.model_dump())

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(line)
    assert line.name == SAMPLE_ITEM_LINE["name"]


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

# Test get_all_item_lines
def test_get_all_item_lines():
    db = MagicMock()
    
    # Mock the full chain of method calls
    db.query.return_value.offset.return_value.limit.return_value.all.return_value = [
        ItemLine(**SAMPLE_ITEM_LINE),
        ItemLine(name="Line B", description="Another test line"),
    ]

    # Call the function
    results = get_all_item_lines(db)

    # Assert that the chain of calls is correct
    db.query.assert_called_once_with(ItemLine)  # Assert ItemLine is passed to query
    db.query().offset.assert_called_once_with(0)  # Assert offset is called with 0
    db.query().offset().limit.assert_called_once_with(100)  # Assert limit is called with 100
    db.query().offset().limit().all.assert_called_once()  # Assert all is called

    # Check the results
    assert len(results) == 2
    assert results[0].name == SAMPLE_ITEM_LINE["name"]


def test_get_all_item_lines_empty():
    db = MagicMock()
    db.query().all.return_value = []

    results = get_all_item_lines(db)

    db.query().all.assert_called_once()
    assert len(results) == 0

# Test update_item_line
def test_update_item_line_found():
    db = MagicMock()
    db.query().filter().first.return_value = ItemLine(**SAMPLE_ITEM_LINE)
    update_data = ItemLineUpdate(description="Updated description")

    updated_line = update_item_line(db, 1, update_data)

    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(updated_line)
    assert updated_line.description == "Updated description"

def test_update_item_line_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None
    update_data = ItemLineUpdate(description="Updated description")

    result = update_item_line(db, 999, update_data)

    assert result is None


# Test delete_item_line
def test_delete_item_line_found():
    db = MagicMock()
    db.query().filter().first.return_value = ItemLine(**SAMPLE_ITEM_LINE)

    result = delete_item_line(db, 1)

    db.delete.assert_called_once()
    db.commit.assert_called_once()
    assert result is True

def test_delete_item_line_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    result = delete_item_line(db, 999)

    assert result is False
