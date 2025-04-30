from CVD import CVDClassifier

jason: dict[str, int] = {  # Joke name
    "Sex": 1,  # 0=female, 1 = male
    "GeneralHealth": 4,  # 1-4, 4 being best health
    "PhysicalActivities": 1,  # dont change, 1=yes, 0=no
    "HadAsthma": 1,  # 0=yes, 1=no (flipped on purpose)
    "HadCOPD": 1,  # 1 = yes, 0= no
    "HadKidneyDisease": 1,  # 1 = yes, 0= no
    "HadArthritis": 0,  # 1 = yes, 0= no
    "HadDiabetes": 4,  # dont touch 1-4 scale
    "SmokerStatus": 0,  # 0=never smoke, 1=smoke
    "AgeCategory": 8,  # algorithm
    "HeightInMeters": 1.84,
    "WeightInKilograms": 70,
    "BMI": 20.7,
    "AlcoholDrinkers": 0,  # 1 = yes, 0= no
    "HaveHighCholesterol": 1,  # 1 = yes, 0= no
    "Sensory Impairments": 1,  # 1 = yes, 0= no
    "Vaccinated": 0,  # 1 = yes, 0= no
    "Mobility": 1,  # 0=good, 1=bad
}

cvd = CVDClassifier()
print(cvd.predict(jason))
