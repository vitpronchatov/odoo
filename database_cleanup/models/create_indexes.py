# Copyright 2017 Therp BV <http://therp.nl>
# Copyright 2021 Camptocamp <https://camptocamp.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
# pylint: disable=consider-merging-classes-inherited
from odoo import fields, models

from ..identifier_adapter import IdentifierAdapter


class CreateIndexesLine(models.TransientModel):
    _inherit = "cleanup.purge.line"
    _name = "cleanup.create_indexes.line"
    _description = "Cleanup Create Indexes line"

    purged = fields.Boolean("Created")
    wizard_id = fields.Many2one("cleanup.create_indexes.wizard")
    field_id = fields.Many2one("ir.model.fields", required=True)

    def purge(self):
        for field in self.mapped("field_id"):
            model = self.env[field.model]
            name = f"{model._table}__{field.name}_index"
            self.env.cr.execute(
                "create index %s ON %s (%s)",
                (
                    IdentifierAdapter(name, quote=False),
                    IdentifierAdapter(model._table),
                    IdentifierAdapter(field.name),
                ),
            )
            self.env.cr.execute("analyze %s", (IdentifierAdapter(model._table),))
        self.write(
            {
                "purged": True,
            }
        )


class CreateIndexesWizard(models.TransientModel):
    _inherit = "cleanup.purge.wizard"
    _name = "cleanup.create_indexes.wizard"
    _description = "Create indexes"

    purge_line_ids = fields.One2many(
        "cleanup.create_indexes.line",
        "wizard_id",
    )

    def find(self):
        res = list()
        for field in self.env["ir.model.fields"].search(
            [
                ("index", "=", True),
            ]
        ):
            if field.model not in self.env.registry:
                continue
            model = self.env[field.model]
            name = f"{model._table}__{field.name}_index"
            self.env.cr.execute(
                "select indexname from pg_indexes "
                "where indexname=%s and tablename=%s",
                (name, model._table),
            )
            if self.env.cr.rowcount:
                continue

            self.env.cr.execute(
                "select a.attname "
                "from pg_attribute a "
                "join pg_class c on a.attrelid=c.oid "
                "join pg_tables t on t.tablename=c.relname "
                "where attname=%s and c.relname=%s",
                (
                    field.name,
                    model._table,
                ),
            )
            if not self.env.cr.rowcount:
                continue

            res.append(
                (
                    0,
                    0,
                    {
                        "name": f"{field.model}.{field.name}",
                        "field_id": field.id,
                    },
                )
            )
        return res
