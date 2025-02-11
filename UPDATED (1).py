import pandas as pd

# Load the dataset
file_path = "/Users/vincent/Downloads/Barret Donald CDF Test/Martinez, Niederle, Vespa - AER/data/test_for_our_data/cleaned_data_all_treatments.xlsx"
data = pd.read_excel(file_path)

# Melt the dataset to long format, retaining the 'rounds' column
long_data = pd.melt(
    data,
    id_vars=["ResponseId", "treatment"],  # Columns to keep
    value_vars=[col for col in data.columns if "choice" in col],  # Choice columns
    var_name="round",  # New column for round labels
    value_name="choices"  # New column for decisions
)

# Rename columns for clarity
long_data.rename(columns={"ResponseId": "id"}, inplace=True)

# Convert the round column to numeric
long_data["round"] = long_data["round"].str.extract(r"(\d+)").astype(float).astype("Int64")

# Sort by id and round to maintain order
long_data.sort_values(by=["id", "round"], inplace=True)

# Save the updated data
long_data.to_csv("long_data_with_rounds.txt", sep="\t", index=False, header=True)

# Define excluded rounds
exclude_rounds = [1, 12, 13, 14, 20, 21, 25, 29, 33, 39, 40, 44, 46, 51, 53, 54, 62, 68, 70, 71, 72]
rounds_to_average_2 = [round for round in range(21, 61) if round not in exclude_rounds][-10:]

# Filter data for treatments B and SB
b_and_sb_data = long_data[
    (long_data['treatment'].isin(['B', 'SB'])) & (long_data['round'].isin(rounds_to_average_2))
]

# Drop the 'round' column
b_and_sb_data = b_and_sb_data.drop(columns=["round"])

# Map B to 1, SB to 0
b_and_sb_data['treatment'] = b_and_sb_data['treatment'].map({'B': 1, 'SB': 0})

# Reorder and rename columns
b_and_sb_data = b_and_sb_data[['treatment', 'id', 'choices']]
b_and_sb_data.rename(columns={'choices': 'a'}, inplace=True)

# Save to a .txt file
b_and_sb_data.to_csv("data_B_vs_SB_last_10_rounds.txt", sep="\t", index=False)
print("Dataset for B and SB for the last 10 rounds of part 2 created successfully with corrected column names.")
