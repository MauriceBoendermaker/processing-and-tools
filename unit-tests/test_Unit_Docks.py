import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from sqlalchemy.orm import Session
from CargoHubV2.app.services.docks_service import (
    create_dock,
    get_all_docks,
    get_dock_by_id,
    update_dock,
    delete_dock,
)
from CargoHubV2.app.models.docks_model import Dock
from CargoHubV2.app.schemas.docks_schema import DockCreate, DockUpdate


class TestDockService(unittest.TestCase):
    def setUp(self):
        # Mock session
        self.db = MagicMock(spec=Session)

        # Example dock data
        self.dock_data = {
            "warehouse_id": 1,
            "code": "DCK001",
            "status": "free",
            "description": "Test Dock",
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
            "is_deleted": False
        }
        self.dock = Dock(**self.dock_data)

    # Tests

    def test_create_dock(self):
        self.db.add = MagicMock()
        self.db.commit = MagicMock()

        dock_create = DockCreate(**self.dock_data)
        new_dock = create_dock(self.db, dock_create)

        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.assertEqual(new_dock.code, self.dock_data["code"])
        self.assertEqual(new_dock.warehouse_id, self.dock_data["warehouse_id"])

    def test_get_all_docks(self):
        # Mock query result
        self.db.query.return_value.filter.return_value.all.return_value = [self.dock]

        docks = get_all_docks(self.db, offset=0, limit=10, sort_by="id", order="asc")
        self.assertEqual(len(docks), 1)
        self.assertEqual(docks[0].code, "DCK001")

    def test_get_dock_by_id(self):
        self.db.query.return_value.filter.return_value.first.return_value = self.dock

        result = get_dock_by_id(self.db, 1)
        self.assertEqual(result.code, "DCK001")

    def test_update_dock(self):
        self.db.query.return_value.filter.return_value.first.return_value = self.dock
        self.db.commit = MagicMock()

        dock_update = DockUpdate(status="occupied", description="Updated Dock")
        updated_dock = update_dock(self.db, 1, dock_update)

        self.db.commit.assert_called_once()
        self.assertEqual(updated_dock.status, "occupied")
        self.assertEqual(updated_dock.description, "Updated Dock")

    def test_delete_dock(self):
        self.db.query.return_value.filter.return_value.first.return_value = self.dock
        self.db.commit = MagicMock()

        result = delete_dock(self.db, 1)

        self.db.commit.assert_called_once()
        self.assertTrue(self.dock.is_deleted)
        self.assertIn("Dock with ID", result["detail"])


if __name__ == "__main__":
    unittest.main()
