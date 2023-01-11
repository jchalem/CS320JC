# project: p2
# submitter: jchalem
# partner: none
# hours: 20

from zipfile import ZipFile, ZIP_DEFLATED
from io import TextIOWrapper
import pandas as pd
import csv, io, json

class Applicant:
    def __init__(self, age, race):
        self.age = age
        self.race = set()
        for r in race:
            if r in race_lookup.keys():
                self.race.add(race_lookup[r])
            
    def __repr__(self):
        return f"Applicant({repr(self.age)}, {sorted(list(self.race))})"
    
    def lower_age(self):
        lower = self.age.replace("<", "")
        lower = lower.replace(">", "")
        lower = lower.replace("-", ",")
        lower = lower.split(",")
        # I got the following algorithm from stack exchange
        # https://stackoverflow.com/questions/1614236/in-python-how-do-i-convert-all-of-the-items-in-a-list-to-floats
        lower = [int(i) for i in lower]
        return min(lower)
    
    def __lt__(self, other):
        return self.lower_age() < other.lower_age()
    
class Loan:     
    def __init__(self, values):
        for val in ["loan_amount","property_value","interest_rate"]:
            try:
                values[val] = float(values[val])
            except:
                values[val] = -1
            #if values[val] == "NA":
            #    values[val] = -1
        self.loan_amount = values["loan_amount"]
        self.property_value = values["property_value"]
        self.interest_rate = values["interest_rate"]
        #self.loan_amount = float(values["loan_amount"])
        #self.property_value = float(values["property_value"])
        #self.interest_rate = float(values["interest_rate"])
        
        self.age = []
        self.age.append(values["applicant_age"])
        #self.races = []
        self.applicants = []
        self.race = []
        self.race += self.race_list(values, "applicant_race-")
        self.applicants.append(Applicant(self.age, self.race))
        if values["co-applicant_age"] != "9999":
            new_age = []
            new_age.append(values["co-applicant_age"])
            new_race = []
            new_race += self.race_list(values, "co-applicant_race-")
            #self.applicants.append(Applicant(self    
            self.applicants.append(Applicant(new_age, new_race))
        self.number_applicants = len(self.age)
        
    def race_list(self, values, startingterm):
        race = []
        for key in list(values.keys()):
            if key.startswith(startingterm) and values[key] != '':
                race.append(values[key])
        return race
        
    def __str__(self):
        return f"<Loan: {str(self.interest_rate)}% on ${str(self.property_value)} with {str(len(self.applicants))} applicant(s)>"
    
    def __repr__(self):
        return f"<Loan: {str(self.interest_rate)}% on ${str(self.property_value)} with {str(len(self.applicants))} applicant(s)>"
    
    def yearly_amounts(self, yearly_payment):
        # TODO: assert interest and amount are positive
        assert self.interest_rate > 0
        assert yearly_payment >= 0
        result = []
        amt = self.loan_amount

        while amt > 0:
            yield amt
            #result.append(amt)
            # TODO: add interest rate multiplied by amt to amt
            amt += (self.interest_rate)/100 * amt
            # TODO: subtract yearly payment from amt
            amt = amt - yearly_payment
        # return result

f = open('banks.json')
 
# returns JSON object as
# a dictionary
data = json.load(f)
banks = []
# Iterating through the json
# list
for i in data:
    banks.append(i)
# closing file
f.close()
banks_keys = list(banks[0].keys())

class Bank:
    def __init__(self, name):
        for i in banks:
            if i['name'] == name:
                self.name = name
                self.lei = i['lei']
                break
        wi_file = []
        self.loan = []
        with ZipFile('wi.zip') as zf:
            #df = zf.infolist()
            with zf.open("wi.csv") as f:
                reader = csv.DictReader(io.TextIOWrapper(f, 'utf-8'))
                for row in reader:
                    if row['lei'] == self.lei:
                        self.loan.append(Loan(row))
                        
    def __getitem__(self, index):
        return self.loan[index]
    
    def __len__(self):
        counter = 0
        for i in self:
            counter += 1
        return counter
        
           
race_lookup = {
    "1": "American Indian or Alaska Native",
    "2": "Asian",
    "21": "Asian Indian",
    "22": "Chinese",
    "23": "Filipino",
    "24": "Japanese",
    "25": "Korean",
    "26": "Vietnamese",
    "27": "Other Asian",
    "3": "Black or African American",
    "4": "Native Hawaiian or Other Pacific Islander",
    "41": "Native Hawaiian",
    "42": "Guamanian or Chamorro",
    "43": "Samoan",
    "44": "Other Pacific Islander",
    "5": "White",
}