import pytest
from unittest.mock import MagicMock
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from CargoHubV2.app.services.item_types_service import (
    create_item_type,
    get_item_type,
    get_all_item_types,
    update_item_type,
    delete_item_type,
)
from CargoHubV2.app.models.item_types_model import ItemType
from CargoHubV2.app.schemas.item_types_schema import ItemTypeCreate, ItemTypeUpdate

SAMPLE_ITEM_TYPE = {"name": "Type Y", "description": "Test type"}

# Test create_item_type
def test_create_item_type():
    db = MagicMock()
    type_data = ItemTypeCreate(**SAMPLE_ITEM_TYPE)
    item_type = create_item_type(db, type_data.model_dump())

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(item_type)
    assert item_type.name == SAMPLE_ITEM_TYPE["name"]

def test_create_item_type_integrity_error():
    db = MagicMock()
    db.commit.side_effect = IntegrityError("mock", "params", "orig")
    type_data = ItemTypeCreate(**SAMPLE_ITEM_TYPE)

    with pytest.raises(HTTPException):
        create_item_type(db, type_data.model_dump())

    db.rollback.assert_called_once()

# Test get_item_type
def test_get_item_type_found():
    db = MagicMock()
    db.query().filter().first.return_value = ItemType(**SAMPLE_ITEM_TYPE)

    result = get_item_type(db, 1)

    db.query().filter().first.assert_called_once()
    assert result.name == SAMPLE_ITEM_TYPE["name"]

def test_get_item_type_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    result = get_item_type(db, 999)

    assert result is None
