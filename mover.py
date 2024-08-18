import os
import shutil
import pandas as pd

# folder paths
train_annotations_dir_1 = 'train_annotations'
train_annotations_dir_2 = 'train_annotations_2'
combined_annotations_dir = 'combined_annotations'

# Create the combined_annotations directory if it doesn't exist
if not os.path.exists(combined_annotations_dir):
    os.makedirs(combined_annotations_dir)

# Function to move files from source to destination
def move_files(source_dir, destination_dir):
    for file_name in os.listdir(source_dir):
        source_file = os.path.join(source_dir, file_name)
        destination_file = os.path.join(destination_dir, file_name)
        shutil.move(source_file, destination_file)
    print(f"Moved all files from {source_dir} to {destination_dir}")

# Move files from both annotation directories
move_files(train_annotations_dir_1, combined_annotations_dir)
move_files(train_annotations_dir_2, combined_annotations_dir)

# Combine the train_labels CSV files
train_labels_1 = 'train_labels.csv'
train_labels_2 = 'train_labels_2.csv'
combined_labels = 'combined_data.csv'

# Read the CSV files into pandas dataframes
df1 = pd.read_csv(train_labels_1)
df2 = pd.read_csv(train_labels_2)

# Combine the dataframes
combined_df = pd.concat([df1, df2])

# Save the combined dataframe into a new CSV file
combined_df.to_csv(combined_labels, index=False)

print(f"Combined {train_labels_1} and {train_labels_2} into {combined_labels}")
