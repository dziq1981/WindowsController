from enum import Enum, unique

class WhatToDo(Enum):
    open = 1
    close = 2
    doNothing =3

class isWindow(Enum):
    open = "otwarte"
    close = "zamknięte"
    unknown = "nie wiadomo"