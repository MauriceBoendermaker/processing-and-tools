import pytest
from unittest.mock import MagicMock, patch
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
    mock_query = db.query.return_value
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = [
        ItemLine(**SAMPLE_ITEM_LINE),
        ItemLine(name="Line B", description="Another test line"),
    ]

    with patch("CargoHubV2.app.services.item_lines_service.apply_sorting", return_value=mock_query) as mock_sorting:
        results = get_all_item_lines(db, offset=0, limit=100, sort_by="name", order="asc")

        mock_sorting.assert_called_once_with(mock_query, ItemLine, "name", "asc")
        db.query.assert_called_once_with(ItemLine)
        mock_query.offset.assert_called_once_with(0)
        mock_query.limit.assert_called_once_with(100)
        mock_query.all.assert_called_once()

        assert len(results) == 2
        assert results[0].name == SAMPLE_ITEM_LINE["name"]



def test_get_all_item_lines_empty():
    db = MagicMock()
    mock_query = db.query.return_value
    mock_query.offset.return_value = mock_query
    mock_query.limit.return_value = mock_query
    mock_query.all.return_value = []

    with patch("CargoHubV2.app.services.item_lines_service.apply_sorting", return_value=mock_query) as mock_sorting:
        results = get_all_item_lines(db, offset=0, limit=100, sort_by="name", order="asc")

        mock_sorting.assert_called_once_with(mock_query, ItemLine, "name", "asc")
        db.query.assert_called_once_with(ItemLine)
        mock_query.offset.assert_called_once_with(0)
        mock_query.limit.assert_called_once_with(100)
        mock_query.all.assert_called_once()

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


def test_delete_item_line_found():
    db = MagicMock()
    mock_item_line = ItemLine(**SAMPLE_ITEM_LINE)
    db.query().filter().first.return_value = mock_item_line

    result = delete_item_line(db, 1)

    assert result is True
    assert mock_item_line.is_deleted is True  # Ensure is_deleted was updated
    db.commit.assert_called_once()
    db.delete.assert_not_called()  # Ensure hard delete was not called



def test_delete_item_line_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    result = delete_item_line(db, 999)

    assert result is False
