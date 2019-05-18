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
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=5, choices=[(tag, tag.value) for tag in StateChoice],  blank=True, null=True)

    # length in miles
    distance = models.FloatField()

    TrackTypeChoices = (
        (1, 'Short Track'),
        (2, 'Intermediate'),
        (3, 'Superspeedway'),
        (4, 'Road Course')
    )
    type = models.IntegerField(TrackTypeChoices)

    def __str__(self):
        return self.name


class Race(models.Model):
    # name of the race
    name = models.CharField(max_length=200)

    # track race occurred at
    track = models.ForeignKey('Track', related_name='races', on_delete=models.CASCADE)

    # race length in miles. This is how far
    # they actually ran; shortened, scheduled,
    # or extended
    distance = models.IntegerField(blank=True, null=True)

    # the race scheduled distance
    scheduled_distance = models.FloatField(blank=True, null=True)

    # the number of laps run.
    laps_run = models.IntegerField(blank=True, null=True)

    # the scheduled amount of laps to run
    scheduled_laps = models.IntegerField(blank=True, null=True)

    # distance of each individual lap
    lap_distance = models.FloatField(blank=True, null=True)

    # race length in time
    length = models.TimeField(blank=True, null=True)

    # date of race
    date = models.DateField(blank=True, null=True)

    # surface of the track
    SurfaceChoices = (
        ('P', 'Paved'),
        ('R', 'Road'),
        ('D', 'Dirt')
    )
    surface = models.CharField(max_length=2, choices=SurfaceChoices, blank=True, null=True)

    def __str__(self):
        return f'{self.date} {self.name}'

    @property
    def leaders(self):
        """simple method to return every driver who led a lap"""
        return set(Leader.objects.filter(race=self).select_related('driver').values_list('driver__name', flat=True))


class Driver(models.Model):
    name = models.CharField(max_length=100)

    date_born = models.DateField(blank=True, null=True)

    home = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name


class RaceResult(models.Model):
    race = models.ForeignKey('Race', on_delete=models.CASCADE)
    driver = models.ForeignKey('Driver', related_name='drivers', on_delete=models.CASCADE)

    starting_position = models.IntegerField()
    finishing_position = models.IntegerField()

    sponsor = models.CharField(max_length=100, blank=True, null=True)
    owner = models.ForeignKey('Owner',  blank=True, null=True, on_delete=models.CASCADE)

    CarChoices = (
        (1, 'Ford'),
        (2, 'Chevrolet'),
        (3, 'Toyota'),
        (4, 'Dodge'),
        (5, 'Pontiac'),
        (6, 'Plymouth'),
        (7, 'Mercury'),
        (8, 'Oldsmobile'),
        (9, 'Matador')
    )
    car = models.IntegerField(choices=CarChoices, blank=True, null=True)

    number = models.CharField(max_length=10, blank=True, null=True)

    laps_completed = models.IntegerField(blank=True, null=True)

    StatusChoices = (
        (1, 'Running'),
        (2, 'Crash'),
        (3, 'Mechanical'),
        (4, 'Parked')

    )
    status = models.IntegerField(choices=StatusChoices, blank=True, null=True)

    def __str__(self):
        return f'{self.race} -- {self.driver} P:{self.finishing_position}'

    @property
    def car_make(self):
        for cm in self.CarChoices:
            if self.car == cm[0]:
                return cm[1]
        return None

    @property
    def running_status(self):
        for status in self.StatusChoices:
            if self.status == status[0]:
                return status[1]
        return None


class Leader(models.Model):
    from_lap = models.IntegerField()
    to_lap = models.IntegerField()
    driver = models.ForeignKey('Driver', related_name='laps_lead', on_delete=models.CASCADE)
    race = models.ForeignKey('race', related_name='leaders', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.race} {self.driver} from {self.from_lap} to {self.to_lap}'

    @property
    def laps_lead(self):
        return (self.to_lap - self.from_lap) + 1


class Caution(models.Model):
    from_lap = models.IntegerField()
    to_lap = models.IntegerField()
    reason = models.CharField(max_length=100, blank=True, null=True)
    free_pass = models.IntegerField(blank=True, null=True)
    race = models.ForeignKey('race', related_name='cautions', on_delete=models.CASCADE)

    def __str__(self):
        return f'Caution for {self.reason} from {self.from_lap} to {self.to_lap}'


class Owner(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
