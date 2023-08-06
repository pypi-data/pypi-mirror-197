import numpy

from gdshoplib.apps.crm.orders import Order
from gdshoplib.services.notion.notion import Notion


class Statistic:
    def avg_price(cls):
        params = Order.list_filter(filter_type="complited")
        notion = Notion(caching=True)
        return numpy.average(
            [order.price for order in Order.query(notion=notion, params=params)]
        )
