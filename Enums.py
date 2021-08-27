from enum import Enum, unique

class whatToDo(Enum):
    open = 1
    close = 2
    doNothing =3

class isWindow(Enum):
    open = "otwarte"
    close = "zamknięte"
    unknown = "nie wiadomo"

class settingType(Enum):
    bool = "bool"
    floatHr="floatHr"
    floatT="floatT"
    floatH="floatH"

class settingNames(Enum):
    manualOverride= "Sterowanie ręczne"
    weekendOpeningTime="Weekendowa godzina otwarcia"
    weekendClosingTime="Weekendowa godzina zamknięcia"
    weekdayOpeningTime="Tygodniowa godzina otwarcia"
    weekdayClosingTime="Tygodniowa godzina zamknięcia"
    closeBelowThisTemp="Zamknij poniżej temperatury"
    openAboveThisHumidity="Otwórz powyżej wilgotności"