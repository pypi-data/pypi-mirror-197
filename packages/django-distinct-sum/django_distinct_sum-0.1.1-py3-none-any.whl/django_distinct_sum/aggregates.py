from decimal import Decimal
from typing import Optional

from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import CharField, F, Q, Value
from django.db.models.functions import Concat


class DistinctSumFunc(ArrayAgg):
    def convert_value(self, value, expression, connection) -> Decimal:
        if not value:
            value = []
        if not isinstance(value, list):
            raise ValueError('DistinctSumFunc did not get a list to sum up')
        data: dict[str, Decimal] = dict()
        for item in value:
            id, val = item.split('_')
            if id and val:
                data[id] = Decimal(val)
        new_value = Decimal(sum(data.values()))
        return new_value


def DistinctSum(id_field: str, sum_field: str, filter: Optional[Q] = None, distinct: bool = True) -> DistinctSumFunc:
    """
    Collects an array of strings to sum them up after query execution.
    Uses JOINs instead of Subqueries.

    :param id_field: ID field name
    :param sum_field: Numeric field name to sum up
    :param filter: Q filter expression to filter values inside aggregation function
    :param distinct: Only distinct values
    :return:
    """
    return DistinctSumFunc(
        Concat(
            F(id_field),
            Value('_'),
            F(sum_field),
            output_field=CharField(),
        ),
        filter=filter,
        distinct=distinct,
    )
