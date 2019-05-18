from django.contrib import admin
from analytics.models import Track, Race, RaceResult, Driver, Leader, Caution, Owner

# Register your models here.
admin.site.register(Track)
admin.site.register(Race)
admin.site.register(RaceResult)
admin.site.register(Driver)
admin.site.register(Leader)
admin.site.register(Caution)
admin.site.register(Owner)