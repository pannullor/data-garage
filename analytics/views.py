from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.generic.base import TemplateView
from django.db.models import Count, Sum
from django.db import connection

from .models import Race, RaceResult, Leader

import datetime


class AnalyticsView(TemplateView):
    template_name = 'analytics/analytics_base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = kwargs['year']

        from_date = '{}-01-01'.format(year)
        to_date = '{}-12-31'.format(year)

        with connection.cursor() as cursor:
            cursor.execute(
               """
               select
          rx.driver_id,
          rx.driver,
          rx.avg_start,
          rx.avg_finish,
          rx.laps_completed,
          sum((l.to_lap - l.from_lap + 1)) as laps_led,
          rx.starts,
          rw.wins
        from (select
                d.id as driver_id,
                d.name as driver,
                round(avg(rr.starting_position), 2) as avg_start,
                round(avg(rr.finishing_position), 2) as avg_finish,
                sum(rr.laps_completed) as laps_completed,
                count(rr.driver_id) as starts
              from analytics_raceresult rr join analytics_race r on rr.race_id = r.id
          and r.date between %s and %s
        join analytics_driver d on rr.driver_id = d.id
          group by rr.driver_id
             ) as rx
          join(select count(rr2.driver_id) as wins, rr2.driver_id
              from analytics_raceresult rr2 join analytics_race r2 on rr2.race_id = r2.id
          and r2.date between %s and %s
          join analytics_driver d on rr2.driver_id = d.id
        where rr2.finishing_position = 1
        group by rr2.driver_id) as rw on rw.driver_id = rx.driver_id
        left join analytics_leader l on l.driver_id = rx.driver_id
          where starts >= 19
        group by rx.driver_id
        order by avg_finish, laps_led
               """, (from_date, to_date, from_date, to_date)
            )

            results = cursor.fetchall()

        context.update({
            'results': results,
            'year': year
        })
        return context
