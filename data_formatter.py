import csv
import os

def clean_pothole_data(csv_path, annotations_dir):
    # Read the CSV file
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    # Get the list of txt files in the annotations directory
    txt_files = set(f for f in os.listdir(annotations_dir) if f.endswith('.txt'))

    # debug print statements
    print(f"Rows length: {len(rows)}")
    print(f"Text Files length: {len(txt_files)}")

    # Create sets for easy lookup
    csv_ids = set(row[0] for row in rows)
    txt_ids = set(f.split('.')[0][1:] for f in txt_files)  # Remove 'p' prefix

    # debug print statements
    # print(f"Text file IDs: {len(txt_ids)}")
    # print(f"CSV IDs: {len(csv_ids)}")
    
    # Filter rows that have matching txt files
    filtered_rows = [row for row in rows if row[0] in txt_ids]

    # Write the filtered data back to the CSV file
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(filtered_rows)

    print(f"Removed {len(rows) - len(filtered_rows)} rows without matching txt files.")

    # Find and remove mismatched txt files
    mismatched_txt_files = txt_ids - csv_ids
    for mismatch in mismatched_txt_files:
        file_to_remove = os.path.join(annotations_dir, f"p{mismatch}.txt")
        os.remove(file_to_remove)
        print(f"Removed mismatched file: {file_to_remove}")

    print(f"Removed {len(mismatched_txt_files)} mismatched txt files.")

    # Final check for any remaining mismatches
    remaining_txt_files = set(f.split('.')[0][1:] for f in os.listdir(annotations_dir) if f.endswith('.txt'))
    remaining_mismatches = remaining_txt_files - csv_ids

    if remaining_mismatches:
        print("Warning: There are still mismatches after cleanup:")
        for mismatch in remaining_mismatches:
            print(f"p{mismatch}.txt")
    else:
        print("All mismatches have been resolved.")

if __name__ == "__main__":
    csv_path = "combined_data.csv"  
    annotations_dir = "combined_annotations"  
    clean_pothole_data(csv_path, annotations_dir)