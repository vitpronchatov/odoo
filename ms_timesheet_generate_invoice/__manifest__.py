# -*- coding: utf-8 -*-
{
    "name": "Timesheet Generate Invoice",
    "summary": """
        Generate customer invoice based on timesheet
    """,
    "description": """

    """,
    "author": "Miftahussalam",
    "website": "https://blog.miftahussalam.com/",
    "category": "Timesheet",
    "version": "17.0.1.0.0",
    "depends": [
        "base",
        "account",
        "analytic",
        "hr_timesheet",
    ],
    "data": [
        "views/account_analytic_line_views.xml",
        "views/project_project_views.xml",
    ],
    "demo": [

    ],
    "images": [
        "static/description/images/main_screenshot.png",
    ],
    "license": "LGPL-3",
}
