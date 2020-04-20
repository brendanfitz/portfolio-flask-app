sex_map = {'male': 0, 'female': 1}
embarked_map = {'C': 0, 'Q': 1, 'S': 2}
title_map = {
   'Army': 0,
   'Master': 1,
   'Medical': 2,
   'Miss': 3,
   'Mr': 4,
   'Mrs': 5,
   'Navy': 6,
   'Rare': 7,
   'Religious': 8
}
age_le = {'Unknown': 0, 'adult': 1, 'child': 2, 'senior': 3, 'young_child': 4}


def fare_label(fare):
    if fare <= 7.91:
        return 0
    elif fare <= 14.454:
        return 1
    elif fare <= 31.0:
        return 2
    else:
        return 3

def age_label(age):
    print(type(age))
    if age < 12:
        return 4
    elif age < 18:
        return 2
    elif age < 50:
        return 1
    elif age < 100:
        return 3
    else:
        return 0

def is_alone(family_size):
    if family_size > 0:
        return 0
    return 1
