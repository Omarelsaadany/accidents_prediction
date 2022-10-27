# -*- coding: utf-8 -*-

from pydantic import BaseModel

class Accis_Pred(BaseModel):
    yahr: int 
    monat: int 
    '''x0_Alkoholunfälle: float
    x0_Fluchtunfälle: float
    x0_Verkehrsunfälle: float
    x1_verletzte_und_getötete: float
    x1_insgesamt: float
    x1_mit_personenschäden: float '''