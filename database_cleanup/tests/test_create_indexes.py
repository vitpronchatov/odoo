# Copyright 2021 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.tests.common import tagged

from .common import Common, environment


# Use post_install to get all models loaded more info: odoo/odoo#13458
@tagged("post_install", "-at_install")
class TestCreateIndexesLine(Common):
    def setUp(self):
        super().setUp()
        with environment() as env:
            # delete some index and check if our module recreated it
            env.cr.execute("drop index res_partner__name_index")

    def test_deleted_index(self):
        with environment() as env:
            wizard = env["cleanup.create_indexes.wizard"].create({})
            wizard.purge_all()
            env.cr.execute(
                "select indexname from pg_indexes where "
                "indexname='res_partner__name_index' and tablename='res_partner' "
            )
            self.assertEqual(env.cr.rowcount, 1)
