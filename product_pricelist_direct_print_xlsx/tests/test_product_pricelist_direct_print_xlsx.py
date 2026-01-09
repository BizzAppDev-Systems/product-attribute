# Copyright 2017 Carlos Dauden <carlos.dauden@tecnativa.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests.common import tagged

from odoo.addons.base.tests.common import BaseCommon


@tagged("post_install", "-at_install")
class TestProductPricelistDirectPrintXLSX(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Pricelist for test",
                "item_ids": [
                    (
                        0,
                        0,
                        {
                            "applied_on": "3_global",
                            "percent_price": 5.00,
                            "compute_price": "percentage",
                        },
                    )
                ],
            }
        )
        cls.wiz_obj = cls.env["product.pricelist.print"]
        # Create partner, category, and product
        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})
        cls.category = cls.env["product.category"].create({"name": "Test Category"})
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "list_price": 100,
                "standard_price": 80,
                "categ_id": cls.category.id,
            }
        )

    def test_report(self):
        wiz = self.wiz_obj.with_context(
            active_model="product.pricelist",
            active_id=self.pricelist.id,
        ).create({})
        report_xlsx = self.env["ir.actions.report"]._render(
            "product_pricelist_direct_print_xlsx.report", wiz.ids
        )
        self.assertGreaterEqual(len(report_xlsx[0]), 1)
        self.assertEqual(report_xlsx[1], "xlsx")

    def test_report_with_products_and_options(self):
        """
        Test XLSX report generation. Ensures the report includes product data
        and wizard display options.
        """
        self.pricelist.item_ids[0].write({"product_id": self.product.id})
        wiz = self.wiz_obj.with_context(
            active_model="product.pricelist",
            active_id=self.pricelist.id,
        ).create(
            {
                "show_pricelist_name": True,
                "show_internal_category": True,
                "show_standard_price": True,
                "show_sale_price": True,
                "show_product_uom": True,
                "summary": "Test summary",
                "partner_id": self.partner.id,
            }
        )
        report = self.env["ir.actions.report"]._render(
            "product_pricelist_direct_print_xlsx.report",
            wiz.ids,
        )
        self.assertEqual(
            report[1],
            "xlsx",
            "Report renderer should return XLSX as output format",
        )
        self.assertGreater(
            len(report[0]),
            100,
            "Generated XLSX file should not be empty and must contain data rows",
        )
