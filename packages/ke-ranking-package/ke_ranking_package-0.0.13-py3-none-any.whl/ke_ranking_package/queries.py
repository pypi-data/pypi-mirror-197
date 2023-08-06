# url-ы изображений товаров для визуализации
get_images = """SELECT sku_group.id as sku_group_id, 
                       product_id, title,
                       image.id image_id, 
                       key, 
                       url_prefix 
                FROM sku_group
                LEFT JOIN image ON sku_group.image_id = image.id
                LEFT JOIN product ON sku_group.product_id = product.id
                WHERE sku_group.id IN %(sku_group_ids)s"""

# сессии с заказом из таблицы атрибуции
get_session_with_orders = """SELECT query, 
                                    session_id,
                                    order_item_id,
                                    sku_sku_group_id ordered_sku_group_id, 
                                    order_created_at
                             FROM marts.order_items_attribution oia
                             LEFT JOIN marts.order_items oi ON oia.order_item_id=oi.order_item_id
                             WHERE product_list_type='SEARCH_RESULTS'
                             AND last_atc_platform=%(platform)s
                             AND order_created_at >= %(start_date)s AND order_created_at <= %(end_date)s
                             AND query!=''"""
