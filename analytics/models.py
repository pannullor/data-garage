from django.db import models

from django.db import models

from enum import Enum


class StateChoice(Enum):
    AL = 'Alabama'
    AK = 'Alaska'
    AZ = 'Arizona'
    AR = 'Arkansas'
    CA = 'California'
    CO = 'Colorado'
    CT = 'Connecticut'
    DE = 'Delaware'
    FL = 'Florida'
    GA = 'Georgia'
    HI = 'Hawaii'
    ID = 'Idaho'
    IL = 'Illinois'
    IN = 'Indiana'
    IA = 'Iowa'
    KS = 'Kansas'
    KY = 'Kentucky'
    LA = 'Louisiana'
    ME = 'Maine'
    MD = 'Maryland'
    MA = 'Massachusetts'
    MI = 'Michigan'
    MN = 'Minnesota'
    MS = 'Mississippi'
    MO = 'Missouri'
    MT = 'Montana'
    NE = 'Nebraska'
    NV = 'Nevada'
    NH = 'New Hampshire'
    NJ = 'New Jersey'
    NM = 'New Mexico'
    NY = 'New York'
    NC = 'North Carolina'
    ND = 'North Dakota'
    OH = 'Ohio'
    OK = 'Oklahoma'
    OR = 'Oregon'
    PA = 'Pennsylvania'
    RI = 'Rhode Island'
    SC = 'South Carolina'
    SD = 'South Dakota'
    TN = 'Tennessee'
    TX = 'Texas'
    UT = 'Utah'
    VT = 'Vermont'
    VA = 'Virginia'
    WA = 'Washington'
    WV = 'West Virginia'
    WI = 'Wisconsin'
    WY = 'Wyoming'


class Track(models.Model):
    # name of the race
    name = models.CharField(max_length=200)

    # track location
    city = models.CharField(max_length=50)
    state = models.IntegerField(choices=[(tag, tag.value) for tag in StateChoice])

    # length in miles
    distance = models.FloatField()

    last_race = models.DateField()

    TrackTypeChoices = (
        (1, 'Short Track'),
        (2, 'Intermediate'),
        (3, 'Superspeedway'),
        (4, 'Road Course')
    )
    type = models.IntegerField(TrackTypeChoices)


class Race(models.Model):
    # name of the race
    name = models.CharField(max_length=200)

    # track race occurred at
    track = models.ForeignKey('Track', related_name='races', on_delete=models.CASCADE)

    # race length in miles. This is how far
    # they actually ran; shortened, scheduled,
    # or extended
    distance = models.IntegerField()

    # the race scheduled distance
    scheduled_distance = models.FloatField()

    # the number of laps run.
    laps_run = models.IntegerField()

    # the scheduled amount of laps to run
    scheduled_laps = models.IntegerField

    # distance of each individual lap
    lap_distance = models.FloatField()

    # race length in time
    length = models.TimeField()

    # date of race
    date = models.DateField()

    # total caution laps
    caution_laps = models.IntegerField(default=0)

    # total number of cautions
    caution_flags = models.IntegerField(default=0)

    # total lead changes
    lead_changes = models.IntegerField(default=0)

    # surface of the track
    SurfaceChoices = (
        ('P', 'Paved'),
        ('R', 'Road'),
        ('D', 'Dirt')
    )
    surface = models.IntegerField(choices=SurfaceChoices)


class Driver(models.Model):
    name = models.CharField(max_length=100)

    date_born = models.DateField()

    home = models.CharField(max_length=100)

    career_starts = models.IntegerField(default=0)
    career_wins = models.IntegerField(default=0)


class RaceResult(models.Model):
    race = models.ForeignKey('Race', on_delete=models.CASCADE)
    driver = models.ForeignKey('Driver', related_name='drivers', on_delete=models.CASCADE)

    starting_position = models.IntegerField()
    finishing_position = models.IntegerField()

    sponsor = models.CharField(max_length=100)
    owner = models.ForeignKey('Owner', on_delete=models.CASCADE)

    CarChoices = (
        (1, 'Ford'),
        (2, 'Chevrolet'),
        (3, 'Toyota'),
        (4, 'Dodge'),
        (5, 'Pontiac'),
        (6, 'Plymouth'),
        (7, 'Mercury'),
        (8, 'Oldsmobile')
    )
    car = models.IntegerField(choices=CarChoices)

    laps_completed = models.IntegerField()

    StatusChoices = (
        (1, 'Running'),
        (2, 'Crash'),
        (3, 'Mechanical'),
        (4, 'Parked')

    )
    status = models.CharField


class Leader(models.Model):
    from_lap = models.IntegerField()
    to_lap = models.IntegerField()
    driver = models.ForeignKey('Driver', related_name='laps_lead', on_delete=models.CASCADE)
    race = models.ForeignKey('race', related_name='leaders', on_delete=models.CASCADE)


class Caution(models.Model):
    from_lap = models.IntegerField()
    to_lap = models.IntegerField()
    reason = models.CharField(max_length=100)
    free_pass = models.IntegerField()
    race = models.ForeignKey('race', related_name='cautions', on_delete=models.CASCADE)


class Owner(models.Model):
    name = models.CharField(max_length=100)

