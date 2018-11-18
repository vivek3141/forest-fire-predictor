# This is a collection of functions including functions for the Canadian Fire Weather Index
# as well as 5 equations from (Lawson et al 1997) necessary to convert the Duff Moisture Code to
# an actual moisture percent value.
#
# FWI Functions:
#
# FFMC - takes temperature, relative humidity, wind speed, rain, and a previous FFMC value to produce the current FFMC value
#      - FFMC(17,42,25,0,85) = 87.692980092774448
#
# DMC - takes temperature, relative humidity, rainfall, previous DMC value, latitude, and current month to produce the current DMC value
#    - DMC(17,42,0,6,45.98,4) = 8.5450511359999997
#
# DC - takes temperature, rain, the previous DC value, latititude, and current month to produce the current DC value
#   - DC(17,0,15,45.98,4) = 19.013999999999999
#
# ISI - takes the wind speed and current FFMC value to produce the current ISI value
#    - ISI(25,87.692980092774448) = 10.853661073655068
#
# BUI - takes the current DMC and DC values to produce the current BUI value
#    - BUI(8.5450511359999997,19.013999999999999) = 8.4904265358371838
#
# FWI - takes the current ISI and BUI values to produce the current FWI value
#    - FWI(10.853661073655068,8.4904265358371838) = 10.096371392382368
#
# calcFWI - this function returns the current FWI value given all of the input values:
#              month, temperature, relative humidity, wind speed, rain, previous FFMC, DMC, DC, and latitude
#        - calcFWI(4,17,42,25,0,85,6,15,45.98) = 10.096371392382368
#
#
#
# Lawson equations:
#
# All of these equations take the current DMC and DC values and return moisture content as a % value
#
# LawsonEq1 - DMC National Standard and Coastal B.C. CWH (2.5-4 cm)^2
#          - LawsonEq1(8.5450511359999997)  = 250.7553985454235
#
# LawsonEq2 - Southern Interior B.C.3 (2-4 cm)^2
#          - LawsonEq2(8.5450511359999997)  = 194.93023948344205
#
# LawsonEq3 - Southern Yukon - Pine/White Spruce
#                             Feather moss, Sphagnum and Undifferentiated duff (2-4 cm)^2
#          - LawsonEq3(8.5450511359999997)  = 442.82109267231488
#
# LawsonEq4 - Southern Yukon - Pine/White Spruce
#                             Reindeer lichen (2-4 cm)^2
#          - LawsonEq4(8.5450511359999997)  = 746.02210402093272
#
# LawsonEq5 - Southern Yukon - White Spruce
#                             White spruce/feather moss (2-4 cm)^2
#          - LawsonEq5(8.5450511359999997)  = 853.2397847094652


import math


class InvalidLatitude(Exception):
    """Exception to handle variables not covered by DataDict"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value) + " is not a valid Latitude."


def FFMC(TEMP, RH, WIND, RAIN, FFMCPrev):
    '''Calculates today's Fine Fuel Moisture Code
    PARAMETERS
    ----------
    TEMP is the 12:00 LST temperature in degrees celsius
    RH is the 12:00 LST relative humidity in %
    WIND is the 12:00 LST wind speed in kph
    RAIN is the 24-hour accumulated rainfall in mm, calculated at 12:00 LST
    FFMCPrev is the previous day's FFMC
    USAGE:
    FFMC(17,42,25,0,85) = 87.692980092774448'''

    RH = min(100.0, RH)
    mo = 147.2 * (101.0 - FFMCPrev) / (59.5 + FFMCPrev)

    if RAIN > .5:
        rf = RAIN - .5

        if mo <= 150.0:
            mr = mo + \
                 42.5 * rf * math.exp(-100.0 / (251.0 - mo)) * (1.0 - math.exp(-6.93 / rf))
        else:

            mr = mo + \
                 42.5 * rf * math.exp(-100.0 / (251.0 - mo)) * (1.0 - math.exp(-6.93 / rf)) + \
                 0.0015 * pow(mo - 150.0, 2) * pow(rf, .5)

        if mr > 250.0:
            mr = 250.0

        mo = mr

    ed = 0.942 * pow(RH, 0.679) + \
         11.0 * math.exp((RH - 100.0) / 10.0) + 0.18 * (21.1 - TEMP) * (1.0 - math.exp(-0.115 * RH))

    if mo > ed:
        ko = 0.424 * (1.0 - pow(RH / 100.0, 1.7)) + \
             0.0694 * pow(WIND, .5) * (1.0 - pow(RH / 100.0, 8))

        kd = ko * 0.581 * math.exp(0.0365 * TEMP)

        m = ed + (mo - ed) * pow(10.0, -kd)

    else:
        ew = 0.618 * pow(RH, 0.753) + \
             10.0 * math.exp((RH - 100.0) / 10.0) + \
             0.18 * (21.1 - TEMP) * (1.0 - math.exp(-0.115 * RH))
        if mo < ew:
            k1 = 0.424 * (1.0 - pow((100.0 - RH) / 100.0, 1.7)) + \
                 0.0694 * pow(WIND, .5) * (1.0 - pow((100.0 - RH) / 100.0, 8))

            kw = k1 * 0.581 * math.exp(0.0365 * TEMP)

            m = ew - (ew - mo) * pow(10.0, -kw)
        else:
            m = mo
    return 59.5 * (250.0 - m) / (147.2 + m)


def DMC(TEMP, RH, RAIN, DMCPrev, LAT, MONTH):
    '''Calculates today's Duff Moisture Code
    PARAMETERS
    ----------
    TEMP is the 12:00 LST temperature in degrees celsius
    RH is the 12:00 LST relative humidity in %
    RAIN is the 24-hour accumulated rainfall in mm, calculated at 12:00 LST
    DMCPrev is the prevvious day's DMC
    Lat is the latitude in decimal degrees of the location for which calculations are being made
    Month is the month of Year (1..12) for the current day's calculations.
    USAGE:
    DMC(17,42,0,6,45.98,4) = 8.5450511359999997'''

    RH = min(100.0, RH)
    if RAIN > 1.5:
        re = 0.92 * RAIN - 1.27

        mo = 20.0 + math.exp(5.6348 - DMCPrev / 43.43)

        if DMCPrev <= 33.0:
            b = 100.0 / (0.5 + 0.3 * DMCPrev)
        else:
            if DMCPrev <= 65.0:
                b = 14.0 - 1.3 * math.log(DMCPrev)
            else:
                b = 6.2 * math.log(DMCPrev) - 17.2

        mr = mo + 1000.0 * re / (48.77 + b * re)

        pr = 244.72 - 43.43 * math.log(mr - 20.0)

        if pr > 0.0:
            DMCPrev = pr
        else:
            DMCPrev = 0.0

    if TEMP > -1.1:
        d1 = DayLength(LAT, MONTH)

        k = 1.894 * (TEMP + 1.1) * (100.0 - RH) * d1 * 0.000001

    else:
        k = 0.0

    return DMCPrev + 100.0 * k


def DC(TEMP, RAIN, DCPrev, LAT, MONTH):
    '''Calculates today's Drought Code Parameters:
    TEMP is the 12:00 LST temperature in degrees celsius
    RAIN is the 24-hour accumulated rainfall in mm, calculated at 12:00 LST
    DCPrev is the previous day's DC
    LAT is the latitude in decimal degrees of the location for which calculations are being made
    MONTH is the month of Year (1..12) for the current day's calculations.
    DC(17,0,15,45.98,4) = 19.013999999999999'''

    if RAIN > 2.8:
        rd = 0.83 * RAIN - 1.27
        Qo = 800.0 * math.exp(-DCPrev / 400.0)
        Qr = Qo + 3.937 * rd
        Dr = 400.0 * math.log(800.0 / Qr)

        if Dr > 0.0:
            DCPrev = Dr
        else:
            DCPrev = 0.0

    Lf = DryingFactor(LAT, MONTH - 1)

    if TEMP > -2.8:
        V = 0.36 * (TEMP + 2.8) + Lf
    else:
        V = Lf

    if V < 0.0:
        V = 0.0

    D = DCPrev + 0.5 * V

    return D


def ISI(WIND, FFMC):
    '''Calculates today's Initial Spread Index
    PARAMETERS
    ----------
    WIND is the 12:00 LST wind speed in kph
    FFMC is the current day's FFMC
    USAGE:
    ISI(25,87.692980092774448) = 10.853661073655068'''

    fWIND = math.exp(0.05039 * WIND)

    m = 147.2 * (101.0 - FFMC) / (59.5 + FFMC)

    fF = 91.9 * math.exp(-0.1386 * m) * (1.0 + pow(m, 5.31) / 49300000.0)

    return 0.208 * fWIND * fF


def BUI(DMC, DC):
    '''Calculates today's Buildup Index
    PARAMETERS
    ----------
    DMC is the current day's Duff Moisture Code
    DC is the current day's Drought Code
    USAGE:
    BUI(8.5450511359999997,19.013999999999999) = 8.4904265358371838'''

    if DMC <= 0.4 * DC:
        U = 0.8 * DMC * DC / (DMC + 0.4 * DC)
    else:
        U = DMC - (1.0 - 0.8 * DC / (DMC + 0.4 * DC)) * \
            (0.92 + pow(0.0114 * DMC, 1.7))

    return max(U, 0.0)


def FWI(ISI, BUI):
    '''Calculates today's Fire Weather Index
    PARAMETERS
    ----------
    ISI is the current day's ISI
    BUI is the current day's BUI
    USAGE:
    FWI(10.853661073655068,8.4904265358371838) = 10.096371392382368'''

    if BUI <= 80.0:
        fD = 0.626 * pow(BUI, 0.809) + 2.0
    else:
        fD = 1000.0 / (25.0 + 108.64 * math.exp(-0.023 * BUI))

    B = 0.1 * ISI * fD

    if B > 1.0:
        S = math.exp(2.72 * pow(0.434 * math.log(B), 0.647))
    else:
        S = B

    return S


def DryingFactor(Latitude, Month):
    LfN = [-1.6, -1.6, -1.6, 0.9, 3.8, 5.8, 6.4, 5.0, 2.4, 0.4, -1.6, -1.6]
    LfS = [6.4, 5.0, 2.4, 0.4, -1.6, -1.6, -1.6, -1.6, -1.6, 0.9, 3.8, 5.8]

    if Latitude > 0:
        retVal = LfN[Month]
    elif Latitude <= 0.0:
        retVal = LfS[Month]

    return retVal


def DayLength(Latitude, MONTH):
    '''Approximates the length of the day given month and latitude'''

    DayLength46N = [6.5, 7.5, 9.0, 12.8, 13.9, 13.9, 12.4, 10.9, 9.4, 8.0, 7.0, 6.0]
    DayLength20N = [7.9, 8.4, 8.9, 9.5, 9.9, 10.2, 10.1, 9.7, 9.1, 8.6, 8.1, 7.8]
    DayLength20S = [10.1, 9.6, 9.1, 8.5, 8.1, 7.8, 7.9, 8.3, 8.9, 9.4, 9.9, 10.2]
    DayLength40S = [11.5, 10.5, 9.2, 7.9, 6.8, 6.2, 6.5, 7.4, 8.7, 10.0, 11.2, 11.8]

    retVal = None

    if Latitude <= 90 and Latitude > 33:
        retVal = DayLength46N[MONTH - 1]
    elif Latitude <= 33 and Latitude > 0.0:
        retVal = DayLength20N[MONTH - 1]
    elif Latitude <= 0.0 and Latitude > -30.0:
        retVal = DayLength20S[MONTH - 1]
    elif Latitude <= -30.0 and Latitude >= -90.0:
        retVal = DayLength40S[MONTH - 1]

    if retVal == None:
        raise InvalidLatitude(Latitude)

    return retVal


def calcFWI(MONTH, TEMP, RH, WIND, RAIN, FFMCPrev, DMCPrev, DCPrev, LAT):
    '''Calculates today's FWI
    PARAMETERS
    ----------
    MONTH is the numeral month, from 1 to 12
    TEMP is the 12:00 LST temperature in degrees celsius
    RH is the 12:00 LST relative humidity in %
    WIND is the 12:00 LST wind speed in kph
    RAIN is the 24-hour accumulated rainfall in mm, calculated at 12:00 LST
    FFMCPrev is the previous day's FFMC
    DMCPrev is the previous day's DCM
    DCPrev is the previous day's DC
    LAT is the latitude in decimal degrees of the location for which calculations are being made
    USAGE:
    calcFWI(4,17,42,25,0,85,6,15,45.98) = 10.096371392382368'''

    ffmc = FFMC(TEMP, RH, WIND, RAIN, FFMCPrev)
    dmc = DMC(TEMP, RH, RAIN, DMCPrev, LAT, MONTH)
    dc = DC(TEMP, RAIN, DCPrev, LAT, MONTH)
    isi = ISI(WIND, ffmc)
    bui = BUI(dmc, dc)
    fwi = FWI(isi, bui)

    return fwi


def LawsonEq1(DMC):
    '''National Standard and Best-fit Non-linear Regression Equations
    Linking DMC to Forest Floor Moisture Content in
    Coastal B.C., Southern Interior B.C. and Southern Yukon
    DMC National Standard and Coastal B.C. CWH (2.5-4 cm)^2
    USAGE:
    LawsonEq1(8.5450511359999997)  = 250.7553985454235'''

    return math.exp((DMC - 244.7) / -43.4) + 20.0


def LawsonEq2(DMC):
    '''National Standard and Best-fit Non-linear Regression Equations
    Linking DMC to Forest Floor Moisture Content in
    Coastal B.C., Southern Interior B.C. and Southern Yukon
    Southern Interior B.C.3 (2-4 cm)^2
    USAGE:
    LawsonEq2(8.5450511359999997)  = 194.93023948344205'''
    return math.exp((DMC - 223.9) / -41.7) + 20.0


def LawsonEq3(DMC):
    '''National Standard and Best-fit Non-linear Regression Equations
    Linking DMC to Forest Floor Moisture Content in
    Coastal B.C., Southern Interior B.C. and Southern Yukon
    Southern Yukon - Pine/White Spruce
    Feather moss, Sphagnum and Undifferentiated duff (2-4 cm)^2
    USAGE:
    LawsonEq3(8.5450511359999997)  = 442.82109267231488'''
    return math.exp((DMC - 157.3) / -24.6) + 20


def LawsonEq4(DMC):
    '''National Standard and Best-fit Non-linear Regression Equations
    Linking DMC to Forest Floor Moisture Content in
    Coastal B.C., Southern Interior B.C. and Southern Yukon
    Southern Yukon - Pine/White Spruce
    Reindeer lichen (2-4 cm)^2
    USAGE:
    LawsonEq4(8.5450511359999997)  = 746.02210402093272'''
    return math.exp((DMC - 106.7) / -14.9) + 20.0


def LawsonEq5(DMC):
    '''National Standard and Best-fit Non-linear Regression Equations
    Linking DMC to Forest Floor Moisture Content in
    Coastal B.C., Southern Interior B.C. and Southern Yukon
    Southern Yukon - White Spruce
    White spruce/feather moss (2-4 cm)^2
    USAGE:
    LawsonEq5(8.5450511359999997)  = 853.2397847094652'''

    return math.exp((DMC - 149.6) / -20.9)
