from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import FloatField, TimeField, BooleanField, SubmitField
from wtforms.validators import number_range
import conditions
from Enums import settingNames
import math, time
class SettingsForm(FlaskForm):

    def __floatToTime(number):
        dMins,hrs = math.modf(number)
        mins = int(dMins*60)        
        return datetime(year=1, month=1, day=1,hour=int(hrs),minute=mins,second=0,microsecond=0)

    manualOverride = BooleanField("Sterowanie ręczne", default=conditions.manualOverride)
    weekendOpeningTime = TimeField("Weekendowy czas otwarcia", default=__floatToTime(conditions.weekendOpeningTime))
    weekendClosingTime = TimeField("Weekendowy czas zamknięcia", default=__floatToTime(conditions.weekendClosingTime))
    weekdayOpeningTime = TimeField("Tygodniowy czas otwarcia", default=__floatToTime(conditions.weekdayOpeningTime))
    weekdayClosingTime = TimeField("Tygodniowy czas zamknięcia", default=__floatToTime(conditions.weekdayClosingTime))
    closeBelowThisTemp = FloatField("Zamknij poniżej temperatury [°C]", validators=[number_range(min=6,max=35)], default = conditions.closeBelowThisTemp)
    openAboveThisHumidity = FloatField("Otwórz powyżej wilgotności [%]", validators=[number_range(min=0,max=100)], default = conditions.openAboveThisHumidity)
    submit = SubmitField('Zatwierdź')

    def run(self):        
        self.manualOverride = BooleanField("Sterowanie ręczne", default=conditions.manualOverride)
        self.weekendOpeningTime = TimeField("Weekendowy czas otwarcia", default=__floatToTime(conditions.weekendOpeningTime))
        self.weekendClosingTime = TimeField("Weekendowy czas zamknięcia", default=__floatToTime(conditions.weekendClosingTime))
        self.weekdayOpeningTime = TimeField("Tygodniowy czas otwarcia", default=__floatToTime(conditions.weekdayOpeningTime))
        self.weekdayClosingTime = TimeField("Tygodniowy czas zamknięcia", default=__floatToTime(conditions.weekdayClosingTime))
        self.closeBelowThisTemp = FloatField("Zamknij poniżej temperatury [°C]", validators=[number_range(min=6,max=35)], default = conditions.closeBelowThisTemp)
        self.openAboveThisHumidity = FloatField("Otwórz powyżej wilgotności [%]", validators=[number_range(min=0,max=100)], default = conditions.openAboveThisHumidity)
    