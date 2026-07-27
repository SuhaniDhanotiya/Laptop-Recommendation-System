import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import hstack
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("laptops.csv")

features = df[
    [
        "processor_brand",
        "processor_tier",
        "ram_memory",
        "primary_storage_capacity",
        "gpu_type",
        "OS"
    ]
]

# Preview (only for testing)
# print(features.head())

# Numerical features
numerical_features = df[
    [
        "ram_memory",
        "primary_storage_capacity"
    ]
]

# Feature Scaling
scaler = StandardScaler()
scaled_numerical = scaler.fit_transform( numerical_features)

# Categorical columns
categorical_columns = [
    "processor_brand",
    "processor_tier",
    "gpu_type",
    "OS"
]

# Encoder
encoder = OneHotEncoder(handle_unknown='ignore')
encoded_data = encoder.fit_transform(df[categorical_columns])


# Combine numerical + categorical data
final_features = hstack(
    [
        encoded_data,
        scaled_numerical
    ]
)

# print(final_features.shape)

# Similarity
similarity = cosine_similarity(final_features)
# print(similarity.shape)


# Similarity Based Recommendation Function
def recommend_by_index(laptop_index, n=5):

    similarity_scores = list(enumerate(similarity[laptop_index]))

    sorted_laptops = sorted(
        similarity_scores,
        key=lambda x: x[1],
        reverse=True
    )

    recommendations = sorted_laptops[1:n+1]

    result = []

    for index, score in recommendations:
        result.append({
            "Brand": df.iloc[index]["brand"],
            "Model": df.iloc[index]["Model"],
            "Price": df.iloc[index]["Price"],
            "RAM": df.iloc[index]["ram_memory"],
            "Storage": df.iloc[index]["primary_storage_capacity"],
            "Processor": df.iloc[index]["processor_tier"],
            "Similarity": round(score, 2)
        })

    return pd.DataFrame(result)


def recommend_by_input(
    processor_brand,
    processor_tier,
    ram,
    storage,
    gpu,
    os,
    n=5
):

    # Find laptops matching the user's configuration
    matched = df[
        (df["processor_brand"] == processor_brand) &
        (df["processor_tier"] == processor_tier) &
        (df["gpu_type"] == gpu) &
        (df["OS"] == os)
    ]

    # Estimate missing numerical values
    if len(matched) > 0:

        avg_cores = matched["num_cores"].mean()
        avg_threads = matched["num_threads"].mean()
        avg_display = matched["display_size"].mean()
        avg_rating = matched["Rating"].mean()
        avg_price = matched["Price"].mean()

    else:

        # Fallback if no matching laptops exist
        avg_cores = df["num_cores"].mean()
        avg_threads = df["num_threads"].mean()
        avg_display = df["display_size"].mean()
        avg_rating = df["Rating"].mean()
        avg_price = df["Price"].mean()

    # user categorical data
    user_categorical = pd.DataFrame(
        [[
            processor_brand,
            processor_tier,
            gpu,
            os
        ]],
        columns=[
            "processor_brand",
            "processor_tier",
            "gpu_type",
            "OS"
        ]
    )

    # user numerical data
    user_numerical = pd.DataFrame(
    [[
        ram,
        storage
    ]],
    columns=[
        "ram_memory",
        "primary_storage_capacity"
    ]
)
    # categorical features
    encoded_user = encoder.transform(user_categorical)

    # Scale numerical features
    scaled_user = scaler.transform(user_numerical)

    # Combine features
    user_features = hstack([
        encoded_user,
        scaled_user
    ])

    # Calculate similarity
    similarity_scores = cosine_similarity(
        user_features,
        final_features
    )[0]

    # Get top recommendations
    top_indices = similarity_scores.argsort()[::-1][:n]

    result = []

    for index in top_indices:

        result.append({
            "Brand": df.iloc[index]["brand"],
            "Model": df.iloc[index]["Model"],
            "Price": df.iloc[index]["Price"],
            "RAM": df.iloc[index]["ram_memory"],
            "Storage": df.iloc[index]["primary_storage_capacity"],
            "Processor": df.iloc[index]["processor_tier"],
            "Similarity": round(similarity_scores[index], 2)
        })

    return pd.DataFrame(result)

   