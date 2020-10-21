{
    'name': 'Sale Proposal',
    'version': '1.0',
    'description': """Sale Proposal""",
    'depends': ['sale','mail','website','portal','sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_proposal_view.xml',
        'views/sale_proposal_portal_template.xml',
        'data/sequence.xml',
        'data/mail_template.xml',
        'report/report.xml',
        'report/report_template.xml',

    ],
    'installable': True,
}