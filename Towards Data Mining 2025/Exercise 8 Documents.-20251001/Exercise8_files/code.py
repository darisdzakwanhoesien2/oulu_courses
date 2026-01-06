import pandas as pd
import scipy.io as sio
import os

# Define file paths
files = {
    "BufferFeatures": "BufferFeatures.mat",
    "participant_1_data_v2": "participant_1_data_v2.mat",
    "participant_1_feature_data": "participant_1_feature_data.mat",
    "participant_1_raw_data": "participant_1_raw_data.mat",
}

# Output directory
output_dir = "mat_to_csv"
os.makedirs(output_dir, exist_ok=True)

# Function to save .mat contents to CSV
def mat_to_csv(matfile, output_prefix):
    data = sio.loadmat(matfile)
    saved_files = []
    for key, value in data.items():
        if key.startswith("__"):  # skip metadata
            continue
        try:
            df = pd.DataFrame(value)
            output_file = os.path.join(output_dir, f"{output_prefix}_{key}.csv")
            df.to_csv(output_file, index=False)
            saved_files.append(output_file)
        except Exception as e:
            print(f"Skipping {key}: {e}")
    return saved_files

# Convert each file
all_csv_files = {}
for name, path in files.items():
    all_csv_files[name] = mat_to_csv(path, name)

all_csv_files