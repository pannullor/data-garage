from django.core.management.base import BaseCommand

from analytics.models import Race, Driver, Track, RaceResult, StateChoice
from racing_reference.scraper import Scraper
from racing_reference.api.driver import Driver as racer
from racing_reference.api.race import Race as rr_race

import datetime
import pprint


class Command(BaseCommand):

    def handle(self, **options):
        """
        populate the database with nascar data
        from the 1972 daytona 500 to today. This
        time is the nascar modern era and that's
        what we'll be analyzing
        :param options:
        :return:
        """

        # Base scraper object
        s = Scraper()

        current_year = datetime.datetime.now().year
        for year in range(1972, current_year):

            season = s.get_season(year)

            for race in season.itertuples():
                # create a racing reference race
                # scraper to data not available
                # in the season race data
                rr = rr_race(year, race.name)

                print(f"{race.name} -- {rr.race_date}")

                # build race data
                race_data = {
                    'name': race.name,
                    'date': race.date,
                    'distance': race.distance,
                    'scheduled_distance': rr.scheduled_distance,
                    'laps_run': rr.laps_run,
                    'scheduled_laps': rr.scheduled_laps,
                    'lap_distance': race.lap_distance,
                    'surface': race.surface,
                    'caution_flags': race.cautions,
                    'caution_laps': race.caution_laps,
                    'lead_changes': race.lead_changes,
                    'length': rr.length,
                }

                # get or create the track next then add
                # it to the race data.
                print(f"Get or Create {race.track}.")
                location = rr.location.strip().split(', ')

                city = location[0]
                state = location[1]

                race_date = rr.race_date

                # convert the race date to a datetime
                race_datetime = datetime.datetime.strptime(race_date[race_date.find(',')+2:], "%B %d, %Y")
                race_datetime = race_datetime.strftime("%m/%d/%Y")

                track_data = {
                    'name': race.track,
                    'city': city,
                    'state': getattr(StateChoice, state),
                }

                # determine the track type
                if race.surface.lower() == 'r':
                    track_data.update({'type': 4})
                else:
                    # short tracks are less than 1 miles,
                    # intermediate will be 1-2,
                    # everything else will be superspeedway
                    size = float(rr.lap_distance)
                    if size < 1:
                        track_data.update({'type': 1})
                    elif 1 <= size < 2:
                        track_data.update({'type': 2})
                    else:
                        track_data.update({'type': 3})



                pprint.pprint(race_data)
                print("\n")


        # # get the active driver list to populate.
        # active_driver_page = s.fetch_page('/active_drivers')
        # driver_table = Scraper.get_table(active_driver_page, 5)
        #
        # # if a driver drives in cup just replace any other
        # # series key with cup since we're specifically working
        # # with the cup series here
        # def find_cup(value):
        #     if value.find('Cup') > -1:
        #         return 'Cup'
        #     return value
        # driver_table['Series'] = driver_table['Series'].apply(find_cup)
        #
        # # filter the df down to cup drivers
        # driver_table = driver_table[driver_table['Series'] == 'Cup']
        #
        # for driver in driver_table.itertuples():
        #     # turn the drivers birthday into a date field
        #     date_born = datetime.datetime.strptime(driver.Born, '%m-%d-%Y').date()
        #
        #     # so for drivers with a suffix their name
        #     # is output first last, suffix. We need to
        #     # strip that formatting out.
        #     name = driver.Driver.replace('.', '').replace(',', '')
        #
        #     driver_data = {
        #         'name': name,
        #         'date_born': date_born,
        #         'home': driver.Home
        #     }
        #     d = racer(name)
        #
        #     # get the drivers stats in cup.
        #     cup_stats = d.cup_stats
        #     career_starts = cup_stats['Races'].iloc[-1]
        #     career_wins = cup_stats['Win'].iloc[-1]
        #
        #     driver_data.update(
        #         {
        #             'career_starts': career_starts,
        #             'career_wins': career_wins
        #         }
        #     )
        #
        #     d = Driver.objects.create(**driver_data)

