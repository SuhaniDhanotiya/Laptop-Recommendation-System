import pandas as pd

df = pd.read_csv("laptops.csv")

# Budget SCore
def budget_score(user_budget , laptop_price):

    difference = abs(user_budget - laptop_price)

    if difference <= 5000:
        return 30

    elif difference <= 10000:
        return 25

    elif difference <= 20000:
        return 15

    else:
        return 5

# RAM Score
def ram_score(user_ram, laptop_ram):

    if user_ram == laptop_ram:
        return 20

    elif laptop_ram > user_ram:
        return 18

    elif user_ram - laptop_ram <= 8:
        return 10

    else:
        return 0

# Storage Score
def storage_score(user_storage, laptop_storage):

    if laptop_storage >= user_storage:
        return 15

    elif user_storage - laptop_storage <= 256:
        return 8

    else:
        return 0

# Processor Ranking
processor_rank = {
    "celeron": 1,
    "pentium": 2,
    "core i3": 3,
    "ryzen 3": 3,
    "core i5": 4,
    "ryzen 5": 4,
    "core i7": 5,
    "ryzen 7": 5,
    "core ultra 7": 6,
    "core i9": 6,
    "ryzen 9": 6,
    "m1": 5,
    "m2": 6,
    "m3": 7,
    "other": 0
}

    # Ranking Score
def processor_score(user_processor, laptop_processor):

    user_rank = processor_rank.get(user_processor.lower(), 0)
    laptop_rank = processor_rank.get(laptop_processor.lower(), 0)

    if laptop_rank >= user_rank:
        return 25

    elif user_rank - laptop_rank == 1:
        return 15

    else:
        return 5

    # Rating Score
def rating_score(rating):

    if rating >= 80:
        return 10

    elif rating >= 70:
        return 8

    elif rating >= 60:
        return 6

    else:
        return 3

# Total Score
def total_score(user_budget, user_ram, user_storage, user_processor, laptop):

    score = 0

    score += budget_score(user_budget , laptop["Price"])
    score += ram_score(user_ram, laptop["ram_memory"])
    score += storage_score(user_storage, laptop["primary_storage_capacity"])
    score += processor_score(user_processor, laptop["processor_tier"])
    score += rating_score(laptop["Rating"])

    return score

# Recommend Laptops
def recommend_laptops(user_budget, user_ram, user_storage, user_processor):

    scores = []

    for _, laptop in df.iterrows():

        score = total_score(
            user_budget,
            user_ram,
            user_storage,
            user_processor,
            laptop
        )

        scores.append(score)

    result = df.copy()

    result["Match Score"] = scores

    result = result.sort_values(
        by="Match Score",
        ascending=False
    )

    return result.head(5)


top5 = recommend_laptops(
    60000,
    16,
    512,
    "core i5"
)

print(top5)