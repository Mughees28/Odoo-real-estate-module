{
    'name': "Real-Estate Management",
    'version': '1.0',
    'depends': ['base'],
    'author': "Mughees",
    'category': 'Category',
    'description': """
        This is a test module of Real-Estate Management!
        Written for the Odoo Quickstart Tutorial.
    """,

    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_menus_tags_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_menus.xml',
        'views/estate_menus_type_views.xml',
        'views/inherited_view.xml'

    ],
    'installable': True,
    'auto_install': False,
}
