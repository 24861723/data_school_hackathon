import csv
import os

def clean_pothole_data(csv_path, annotations_dir):
    # Read the CSV file
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)

    print(f"Initial number of rows in CSV: {len(rows)}")

    # Get the list of txt files in the annotations directory
    txt_files = set(f for f in os.listdir(annotations_dir) if f.endswith('.txt'))
    txt_ids = set(f.split('.')[0][1:] for f in txt_files)  # Remove 'p' prefix

    print(f"Number of txt files: {len(txt_files)}")

    # Remove duplicates and entries without corresponding txt files
    seen_ids = set()
    filtered_rows = []
    removed_rows = []

    for row in rows:
        if row[0] in txt_ids and row[0] not in seen_ids:
            filtered_rows.append(row)
            seen_ids.add(row[0])
        else:
            removed_rows.append(row)

    print(f"\nNumber of rows after filtering: {len(filtered_rows)}")
    print(f"Number of rows removed from CSV: {len(removed_rows)}")

    # Write the filtered data back to the CSV file
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(filtered_rows)

    print(f"Removed {len(removed_rows)} rows (duplicates or without matching txt files).")

    # Final check
    final_txt_files = set(f for f in os.listdir(annotations_dir) if f.endswith('.txt'))
    final_csv_rows = len(filtered_rows)

    if len(final_txt_files) == final_csv_rows:
        print(f"Success! Number of txt files ({len(final_txt_files)}) matches number of CSV rows ({final_csv_rows}).")
    else:
        print(f"Warning: Mismatch still exists. txt files: {len(final_txt_files)}, CSV rows: {final_csv_rows}")

    # If there's still a mismatch, print the differences
    if len(final_txt_files) != final_csv_rows:
        final_csv_ids = set(row[0] for row in filtered_rows)
        final_txt_ids = set(f.split('.')[0][1:] for f in final_txt_files)
        print("CSV rows not in txt files:", final_csv_ids - final_txt_ids)
        print("Txt files not in CSV rows:", final_txt_ids - final_csv_ids)

if __name__ == "__main__":
    csv_path = "combined_data.csv"  # Update this path if necessary
    annotations_dir = "combined_annotations"  # Update this path if necessary
    clean_pothole_data(csv_path, annotations_dir)