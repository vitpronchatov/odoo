# -*- coding: utf-8 -*-
{
    'name': "Ukraine - Accounting VAT support",
    'summary': """Облік ПДВ для України""",
    'description': """
        Цей модуль дає можливість вести облік виданих
        та отриманих податкових накладних.

        Конфліктує з модулем: base_vat
    """,
    'author': "ERP Ukraine",
    'website': "https://erp.co.ua",
    'category': 'Localization/Account Charts',
    'version': '1.4',
    # 'price': 200.00,
    # 'currency': 'EUR',
    'depends': ['account',
                'om_account_accountant',
                ],
    'data': [
        'templates/templates.xml',
        'security/ir.model.access.csv',
        'wizard/account_single_tax_invoice_export_wizard.xml',
        'views/account_tax_invoice_view.xml',
        'views/account_tax_invoice_workflow.xml',
        'views/account_spr_sti_view.xml',
        'views/company_view.xml',
        'views/product_view.xml',
        'views/partner_view.xml',
        'views/account_invoice_view.xml',
        'wizard/account_tax_invoice_export_wizard.xml',
        'wizard/account_tax_invoice_import_wizard.xml',
        'data/account.sprsti.csv',
        'data/taxinvoice_paymeth_data.xml',
        'data/account.taxinvoice.contrtype.csv',
        'data/out_taxinvoice_sequence.xml'
    ],
    'installable': True,
}
