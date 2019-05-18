from django.core.management.base import BaseCommand

from analytics.models import Race, Driver, Track, RaceResult, Owner, Leader, Caution, StateChoice
from racing_reference.scraper import Scraper
from racing_reference.api.driver import Driver as racer
from racing_reference.api.race import Race as rr_race

import datetime
import re
import pandas as pd
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

        start = datetime.datetime.now()

        # Base scraper object
        s = Scraper()

        # regex used later to search for the
        # car owner and sponsor in the results
        owner_re = re.compile(r"^([\w\s/',.&-]+)([\w\s().,-]+)?$")

        current_year = datetime.datetime.now().year
        for year in range(2008, current_year):

            print(f"Begin populating {year} racing season")
            season = s.get_season(year)

            for race in season.itertuples():
                # create a racing reference race
                # scraper to data not available
                # in the season race data
                rr = rr_race(year, race.name)

                print(f"{race.name} -- {rr.race_date}")

                # build race data
                formatted_race_date = datetime.datetime.strptime(race.date, '%m/%d/%y')
                formatted_race_date = formatted_race_date.strftime("%Y-%m-%d")
                race_data = {
                    'name': race.name,
                    'date': formatted_race_date,
                    'distance': race.distance,
                    'scheduled_distance': rr.scheduled_distance,
                    'laps_run': rr.laps_run,
                    'scheduled_laps': rr.scheduled_laps,
                    'lap_distance': race.lap_distance,
                    'surface': race.surface,
                    'length': rr.length,
                }

                # get or create the track next then add
                # it to the race data.
                print(f"Get or Create {race.track}.")
                location = rr.location.strip().split(', ')

                city = location[0]
                state = location[1]

                state_value = StateChoice[state].value
                track_data = {
                    'name': race.track,
                    'city': city,
                    'state': state_value,
                    'distance': rr.lap_distance
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

                track, created = Track.objects.get_or_create(**track_data)
                race_data.update({'track': track})
                print(f"{track} successfully added.")

                # now create the race
                r, created = Race.objects.get_or_create(**race_data)
                print(f"{r} successfully added.")

                print(f"Adding {r} drivers and results")

                # object describing the drivers of the race.
                race_drivers = {}

                # with the race created the we can now create results
                for index, row in rr.results.iterrows():
                    # get the driver instance to create a model
                    rr_d = racer(row['Driver'])

                    print(f"Working Driver {row['Driver']}")

                    driver_data = {
                        'name': row['Driver'],
                        'home': rr_d.hometown
                    }

                    if rr_d.birth_date:
                        driver_data.update({'date_born': rr_d.birth_date.strftime("%Y-%m-%d")})

                    driver, created = Driver.objects.get_or_create(**driver_data)
                    driver_note = 'created' if created else 'fetched'
                    print(f"Successfully {driver_note} {driver}")

                    if not pd.isnull(row['Sponsor / Owner']):
                        spowner = owner_re.match(row['Sponsor / Owner'])
                        if spowner:
                            spowner_groups = spowner.groups()
                            if spowner_groups[1]:
                                sponsor = spowner_groups[0]
                                owner = spowner_groups[1]
                            else:
                                sponsor = None
                                owner = spowner_groups[0]

                            # create the owner real quick
                            owner, created = Owner.objects.get_or_create(name=owner)
                            owner_note = 'created' if created else 'fetched'
                            print(f'Successfully {owner_note} {owner}')
                    else:
                        print("No owner data, continuing")

                    # next go ahead create the results.
                    result_data = {
                        'race': r,
                        'driver': driver,
                        'sponsor': sponsor,
                        'owner': owner,
                        'starting_position': row['St'],
                        'finishing_position': row['Fin'],
                        'number': row['#'],
                        'laps_completed': row['Laps']
                    }

                    cars = RaceResult.CarChoices
                    car_choice = 1
                    for c in cars:
                        make = c[1]
                        if row['Car'].find(make) > -1:
                            car_choice = c[0]
                            break

                    # set the statuses
                    status = row['Status']
                    if status == 'running':
                        status_choice = 1
                    elif status == 'crash':
                        status_choice = 2
                    elif status == 'parked':
                        status_choice = 4
                    else:
                        status_choice = 3

                    result_data.update({
                        'car': car_choice,
                        'status': status_choice
                    })
                    result = RaceResult.objects.get_or_create(**result_data)
                    race_drivers.update({driver.name: driver.pk})
                print("Complete adding race results")

                # next add the cautions and leaders.
                print("Begin adding race leaders")
                leader_table = rr.lap_leader_breakdown()
                for index, row in leader_table.iterrows():
                    driver_id = race_drivers.get(row['Leader'], None)
                    if driver_id:
                        leader = Leader.objects.get_or_create(
                            driver_id=driver_id,
                            race=r,
                            from_lap=row['From'],
                            to_lap=row['To']
                        )
                print("Completed adding lap leaders")

                print("Begin adding caution flags")
                caution_table = rr.flag_breakdown('yellow')
                if caution_table is not None:
                    for index, row in caution_table.iterrows():
                        caution_data = {
                            'from_lap': row['from_lap'],
                            'to_lap': row['to_lap'],
                            'race': r
                        }

                        for x in ['reason', 'free_pass']:
                            if not pd.isnull(row[x]):
                                if x == 'free_pass':
                                    try:
                                        value = int(row[x].replace('#', ''))
                                    except Exception as e:
                                        value = None
                                else:
                                    value = row[x]
                                caution_data.update({x: value})

                        caution = Caution.objects.create(
                            **caution_data
                        )
                print("Complete adding caution flags.")

                print(f"{race.name} -- {rr.race_date} data is complete.")

            print(f"Completed with {year} racing season.")

        print("Completed upload of nascar common era.")
        end = datetime.datetime.now() - start
        print(f"Completion time {end}")

