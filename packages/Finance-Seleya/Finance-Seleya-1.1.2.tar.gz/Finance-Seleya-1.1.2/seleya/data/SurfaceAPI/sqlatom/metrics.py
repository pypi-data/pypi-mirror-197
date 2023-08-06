# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from sqlalchemy import select, and_, outerjoin


class Metrics(object):

    def __init__(self):
        self._metrcis_table = [
            self._engine.table_model[k]
            for k in self._engine.table_model.keys() if 'esg_metrics' in k
        ]

    def _map_metrics(self,
                     metrics,
                     used_metric_tables,
                     diff_columns={'date', 'code'}):
        metrics_cols = {}
        factors = set(factors).difference({'date', 'code'})
        to_keep = factors.copy()
        for f in factors:
            for t in used_metric_tables:
                if f in t.__table__.columns:
                    metrics_cols[t.__table__.columns[f]] = t
                    to_keep.remove(f)
                    break

        if to_keep:
            raise ValueError("factors in <{0}> can't be find".format(to_keep))

        return metrics_cols

    def fetch(self, codes, begin_date, end_date, columns):
        metrics_cols = self._map_metrics(columns, self._metrcis_table)
        joined_tables = set()
        metrics_tables = list(set(metrics_cols.values()))
        if len(metrics_cols) <= 0:
            raise ValueError("factor_tables len({0})".format(
                len(metrics_tables)))

        big_table = metrics_tables[0]
        joined_tables.add(big_table.__table__.name)
        for t in set(metrics_cols.values()):
            if t.__table__.name not in joined_tables:
                big_table = outerjoin(
                    big_table, t,
                    and_(big_table.date == t.date, big_table.code == t.code,
                         t.flag == 1))
                joined_tables.add(t.__table__.name)

        clause_list = and_(
            metrics_tables[0].flag == 1, metrics_tables[0].code.in_(codes),
            metrics_tables[0].date.between(begin_date, end_date))

        query = select([metrics_tables[0].date, metrics_tables[0].code] +
                       list(metrics_cols.keys())).select_from(big_table).where(
                           clause_list)
        return self.custom(query).drop_duplicates(
            subset=['date', 'code']).replace(
                [-np.inf, np.inf], np.nan).sort_values(by=['date', 'code'])
