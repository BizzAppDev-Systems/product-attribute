# Copyright 2024 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import TransactionCase


class TestProductSeasonality(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        # Create seasonality
        cls.season_summer = cls.env["seasonality"].create(
            {
                "name": "Summer",
            }
        )
        # Create product template
        cls.product = cls.env["product.template"].create(
            {
                "name": "Test Product",
                "seasonality_ids": [(6, 0, [cls.season_summer.id])],
            }
        )
        # Use existing UoM (Unit(s))
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        # Link UoM to product
        cls.product_uom = cls.env["product.uom"].create(
            {
                "barcode": "testbarcode",
                "product_id": cls.product.id,
                "uom_id": cls.uom_unit.id,
            }
        )

    def test_product_template_uom_seasonality(self):
        """Test :Product template should contain seasonality product.uom.seasonality_ids
        should reflect product.template.seasonality_ids (related field)"""
        self.assertEqual(self.season_summer.name, "Summer", "Seasonality name mismatch")
        self.assertEqual(
            self.season_summer,
            self.product.seasonality_ids,
            "Seasonality not linked to product template",
        )
        self.assertEqual(
            self.season_summer,
            self.uom_unit.product_uom_ids.seasonality_ids,
            "Seasonality not propagated to product UoM",
        )
