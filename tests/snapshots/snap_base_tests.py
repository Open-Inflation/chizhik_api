# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_active_inout active_inout'] = {
    'background': 'str',
    'banner': 'NoneType',
    'description': 'str',
    'end_timestamp': 'str',
    'image': 'str',
    'is_thematic': 'bool',
    'logo': 'NoneType',
    'pdf': 'str',
    'pdf_data': {
        'background_color': 'str',
        'banner': 'NoneType',
        'file': 'str',
        'image': 'NoneType',
        'subtitle': 'str',
        'text_color': 'str',
        'title': 'str'
    },
    'start_timestamp': 'str',
    'title': 'str',
    'title_color': 'str'
}

snapshots['test_categories_list categories_list'] = [
    {
        'children': [
            {
                'children': [
                    {
                        'children': [
                        ],
                        'depth': 'int',
                        'icon': 'NoneType',
                        'id': 'int',
                        'image': 'NoneType',
                        'is_adults': 'bool',
                        'is_inout': 'bool',
                        'name': 'str',
                        'slug': 'str'
                    }
                ],
                'depth': 'int',
                'icon': 'str',
                'id': 'int',
                'image': 'str',
                'is_adults': 'bool',
                'is_inout': 'bool',
                'name': 'str',
                'slug': 'str'
            }
        ],
        'depth': 'int',
        'icon': 'NoneType',
        'id': 'int',
        'image': 'NoneType',
        'is_adults': 'bool',
        'is_inout': 'bool',
        'name': 'str',
        'slug': 'str'
    }
]

snapshots['test_cities_list cities_list'] = {
    'count': 'int',
    'items': [
        {
            'distance': 'float',
            'fias_id': 'str',
            'has_shop': 'bool',
            'name': 'str'
        }
    ],
    'next': 'NoneType',
    'page_size': 'int',
    'previous': 'NoneType',
    'total_pages': 'int'
}

snapshots['test_download_image download_image'] = 'image downloaded'

snapshots['test_products_list products_list'] = {
    'count': 'int',
    'items': [
        {
            'categories_tree': [
                {
                    'children': [
                        {
                            'children': [
                                {
                                    'children': [
                                    ],
                                    'depth': 'int',
                                    'icon': 'NoneType',
                                    'id': 'int',
                                    'image': 'NoneType',
                                    'is_adults': 'bool',
                                    'is_inout': 'bool',
                                    'name': 'str',
                                    'slug': 'str'
                                }
                            ],
                            'depth': 'int',
                            'icon': 'str',
                            'id': 'int',
                            'image': 'str',
                            'is_adults': 'bool',
                            'is_inout': 'bool',
                            'name': 'str',
                            'slug': 'str'
                        }
                    ],
                    'depth': 'int',
                    'icon': 'NoneType',
                    'id': 'int',
                    'image': 'NoneType',
                    'is_adults': 'bool',
                    'is_inout': 'bool',
                    'name': 'str',
                    'slug': 'str'
                }
            ],
            'description': 'str',
            'id': 'int',
            'images': [
                {
                    'id': 'int',
                    'image': 'str',
                    'title': 'str'
                }
            ],
            'is_favorite': 'bool',
            'is_inout': 'bool',
            'old_price': 'NoneType',
            'plu': 'str',
            'price': 'float',
            'price_piece_unit': 'NoneType',
            'rating': 'float',
            'slug': 'str',
            'sub_title': 'str',
            'title': 'str'
        }
    ],
    'next': 'int',
    'page_size': 'int',
    'previous': 'NoneType',
    'total_pages': 'int'
}

snapshots['test_rebuild_connection rebuild_connection'] = 'connection has been rebuilt'

snapshots['test_set_debug set_debug'] = 'debug mode toggled'
