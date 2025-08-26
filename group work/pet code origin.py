import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("/Users/apple/Desktop/python bootcamp/210 data/pet_adoption_data.csv")

# TimeInShelterDays
print("TimeInShelterDays mean:", df["TimeInShelterDays"].mean())
print("TimeInShelterDays std:", df["TimeInShelterDays"].std())
print("TimeInShelterDays min:", df["TimeInShelterDays"].min())
print("TimeInShelterDays max:", df["TimeInShelterDays"].max())
print("\nTimeInShelterDays percentage of occurrence:")
print((df["TimeInShelterDays"].value_counts(normalize=True) * 100))

# AdoptionFee
print("AdoptionFee mean:", df["AdoptionFee"].mean())
print("AdoptionFee std:", df["AdoptionFee"].std())
print("AdoptionFee min:", df["AdoptionFee"].min())
print("AdoptionFee max:", df["AdoptionFee"].max())
print("\nAdoptionFee percentage of occurrence:")
print((df["AdoptionFee"].value_counts(normalize=True) * 100))

#Histogram
plt.hist(df["WeightKg"].dropna(), bins=20, edgecolor="black")
plt.title("Pets' Weight Distribution")
plt.xlabel("Weight (kg)")
plt.ylabel("Count")
plt.tight_layout()
plt.show()

#Scatterplot
plt.figure()
plt.scatter(df["AgeMonths"], df["AdoptionFee"], alpha=0.5)
plt.title("Age vs Adoption Fee")
plt.xlabel("AgeMonths")
plt.ylabel("Adoption Fee")
plt.tight_layout()
plt.show()

#Pivot Table
print("\nPivot Table: Average adoption fee based on pet type and wether they have previous owner (0 = No, 1 = Yes)")
pivot = pd.pivot_table(df,values="AdoptionFee",index="PetType",columns="PreviousOwner",aggfunc=np.mean)
print(pivot)

# Adoption likelihhod rate: Vaccinated vs Not Vaccinated
adopted = (df["AdoptionLikelihood"] == 1)
vaccinated = (df["Vaccinated"] == 1)
not_vaccinated = (df["Vaccinated"] == 0)
adoption_rate_vaccinated = adopted[vaccinated].mean() * 100
adoption_rate_not_vaccinated = adopted[not_vaccinated].mean() * 100
print("Adoption likelihood rate for vaccinated pet:", adoption_rate_vaccinated, "%")
print("Adoption likelihood rate for non-vaccinated pet:", adoption_rate_not_vaccinated, "%")

# Adoption likelihhod rate: Vaccinated vs Not Vaccinated & age
age_mean = df["AgeMonths"].mean()
younger = (df["AgeMonths"] < age_mean)
older_or_equal = (df["AgeMonths"] >= age_mean)

vacc_young = adopted[vaccinated & younger].mean() * 100
vacc_old = adopted[vaccinated & older_or_equal].mean() * 100
notvacc_young = adopted[not_vaccinated & younger].mean() * 100
notvacc_old = adopted[not_vaccinated & older_or_equal].mean() * 100

print("Vaccinated & Younger than average age:", vacc_young, "%")
print("Vaccinated & Older or equal to average age:", vacc_old, "%")
print("Not Vaccinated & Younger than average age:", notvacc_young, "%")
print("Not Vaccinated & Older or equal to average age:", notvacc_old, "%")