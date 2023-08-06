# -*- coding: utf-8 -*-
import decimal
#  Developed by CQ Inversiones SAS. Copyright ©. 2019 - 2022. All rights reserved.
#  Desarrollado por CQ Inversiones SAS. Copyright ©. 2019 - 2022. Todos los derechos reservado

# ****************************************************************
# IDE:          PyCharm
# Developed by: macercha
# Date:         11/12/22 5:33 PM
# Project:      CFHL Transactional Backend
# Module Name:  price
# Description:
# ****************************************************************
from datetime import datetime
from django.conf import settings
from zibanu.django.db import models


class Price(models.Manager):
    """
    Default manager class for Price model.
    """

    @staticmethod
    def calc_price(price: float, factor: int):
        """
        Static method to calculate price factor based
        :param price: base price
        :param factor: factor to calculate
        :return: calculated price
        """
        if factor > 0:
            factor_multiplier = decimal.Decimal(settings.COFFEE_PRICE_BASE_FACTOR / factor)
            price = decimal.Decimal(price)
            price = round(factor_multiplier * price)
        return price

    def get_by_product(self, product_id: int, date_to_search: datetime):
        """
        Get a product prices list for a specific product and datetime.
        :param product_id: product id to search price
        :param date_to_search: datetime to search price
        :return: Price queryset with match records, if it does not match records, return an empty queryset.
        """
        queryset = self.get_queryset().filter(product_id__exact=product_id, date_from__lte=date_to_search,
                                              date_to__gte=date_to_search)
        return queryset

    def get_price_by_product_date(self, product_id: int, date_from: datetime, date_to: datetime) -> models.QuerySet:
        """
        Get a price record filtered by product, date_from and date_to exactly
        :param product_id: roduct id to search
        :param date_from: date from range
        :param date_to: date end range
        :return: Price queryset with match records, if it does not exist any match record, return an empty queryset
        """
        queryset = self.get_queryset().filter(product_id__exact=product_id, date_from__exact=date_from,
                                              date_to__exact=date_to)
        return queryset

    def get_products_price_by_date(self, date_to_search: datetime, product_list: list = None) -> models.QuerySet:
        """
        Get a list of price records from Price entity for a specific datetime
        :param date_to_search: date time to search price list.
        :param product_list: list of oasis product id for filter
        :return: Price queryset with set of match records, if it does not exist any match record, return an empty
        queryset.
        """
        # TODO: Remove at release.
        if settings.DEBUG:
            date_to_search = datetime(2022, 12, 14, 12, 00)

        qs = self.get_queryset().filter(date_from__lte=date_to_search, date_to__gte=date_to_search)
        if product_list is not None:
            qs = qs.filter(product__product_id__in=product_list)
        return qs

