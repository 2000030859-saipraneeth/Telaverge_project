import gender_guesser.detector as gender

def get_gender(name):
    d = gender.Detector()
    return d.get_gender(name)

# Example usage
name = "IBTIHAJ AHMED"
gender = get_gender(name)
print(f"The gender of {name} is {gender}.")

