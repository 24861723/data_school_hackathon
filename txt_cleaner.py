import os
import time

def clean_txt_files(directory):
    # Get all txt files in the directory
    txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]
    
    print(f"Total number of txt files: {len(txt_files)}")

    removed_files = 0
    failed_to_remove = []

    for filename in txt_files:
        filepath = os.path.join(directory, filename)
        
        try:
            with open(filepath, 'r') as file:
                lines = file.readlines()
                
                # Check if the file has at least two lines and the second line starts with '1'
                if len(lines) < 2 or not lines[1].strip().startswith('1'):
                    try:
                        os.remove(filepath)
                        removed_files += 1
                        print(f"Removed: {filename}")
                    except PermissionError:
                        print(f"Permission denied: Could not remove {filename}")
                        failed_to_remove.append(filename)
                    except Exception as e:
                        print(f"Error removing {filename}: {str(e)}")
                        failed_to_remove.append(filename)
        except Exception as e:
            print(f"Error reading {filename}: {str(e)}")

    print(f"\nTotal files removed: {removed_files}")
    print(f"Remaining files: {len(txt_files) - removed_files}")
    
    if failed_to_remove:
        print(f"\nFailed to remove {len(failed_to_remove)} files:")
        for file in failed_to_remove:
            print(file)
        
        retry = input("\nWould you like to retry removing these files? (y/n): ")
        if retry.lower() == 'y':
            print("Waiting for 5 seconds before retrying...")
            time.sleep(5)
            retry_clean_txt_files(directory, failed_to_remove)

def retry_clean_txt_files(directory, files_to_remove):
    removed_files = 0
    still_failed = []

    for filename in files_to_remove:
        filepath = os.path.join(directory, filename)
        try:
            os.remove(filepath)
            removed_files += 1
            print(f"Successfully removed on retry: {filename}")
        except Exception as e:
            print(f"Still unable to remove {filename}: {str(e)}")
            still_failed.append(filename)

    print(f"\nAdditional files removed on retry: {removed_files}")
    if still_failed:
        print(f"Files still not removed: {len(still_failed)}")
        for file in still_failed:
            print(file)

if __name__ == "__main__":
    # Set this to the directory containing your txt files
    annotations_dir = "combined_annotations"
    clean_txt_files(annotations_dir)