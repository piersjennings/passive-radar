import datetime
from OSGridConverter import latlong2grid
from math import log10, floor

class Transmitter():
    def __init__(self, lat, long, frequency, estimate):
        self.lat = self.roundSigFig(lat, 10)
        self.long = self.roundSigFig(long, 10)
        self.frequency = frequency
        self.estimate = estimate
        self.name = ""
        self.classification = ""
        self.grid_ref = latlong2grid(self.lat, self.long)
        self.transmission_number = 1
        self.date_added = datetime.datetime.now()
        self.date_last_transmission = self.date_added
        self.uid = ""

        if self.estimate == 1:
            self.updateClassification()
    
    def updateTransmissionNumber(self):
        self.transmission_number += 1
        if self.estimate == 1:
            self.updateClassification()
    
    def updateClassification(self):
        if self.transmission_number <= 20:
            self.classification = "Section"
        elif self.transmission_number <= 40:
            self.classification = "Platoon"
        elif self.transmission_number <= 60:
            self.classification = "Company HQ"
        elif self.transmission_number <= 100:
            self.classification = "Battalion HQ"
        elif self.transmission_number > 100:
            self.classification = "Regiment HQ"
    
    def roundSigFig(self, x, sig):
        return round(x, sig-int(floor(log10(abs(x))))-1)
    
    def addMarker(self, marker):
        self.marker = marker

