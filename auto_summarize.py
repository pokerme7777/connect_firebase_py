import os
import pandas as pd
import json
import gradio as gr

def generate_dataframe():
    # Define the base folder path (adjust this path if needed)
    base_folder = "/home/mai/fke/fkee/firebase/firebase_key/inspectionCases"

    # List to hold each record as a dictionary
    records = []

    # Loop over each folder inside the base folder (each should be a timestamp folder)
    for timestamp in os.listdir(base_folder):
        timestamp_path = os.path.join(base_folder, timestamp)
        if not os.path.isdir(timestamp_path):
            continue

        # Check if there are subdirectories inside the timestamp folder
        subdirs = [d for d in os.listdir(timestamp_path) if os.path.isdir(os.path.join(timestamp_path, d))]
        if subdirs:
            # If subdirectories exist, treat each one as a 'class'
            for subdir in subdirs:
                class_folder = os.path.join(timestamp_path, subdir)
                files = os.listdir(class_folder)
                # Identify image files (you can add more extensions if needed)
                image_files = [f for f in files if f.lower().endswith((".jpg", ".jpeg", ".png"))]
                # Identify description text files
                desc_files = [f for f in files if f.lower().endswith(".txt")]
                # Read and join the contents of all description files
                descriptions = []
                for dfile in sorted(desc_files):
                    file_path = os.path.join(class_folder, dfile)
                    with open(file_path, "r", encoding="utf-8") as f:
                        descriptions.append(f.read().strip())
                full_description = "\n".join(descriptions)
                # Create a record for each image file
                for img in image_files:
                    record = {
                        "timestamp": timestamp,
                        "class": subdir,
                        "image_name": img,
                        "description": full_description
                    }
                    records.append(record)
        else:
            # If there are no subdirectories, use 'none' as the class label
            files = os.listdir(timestamp_path)
            image_files = [f for f in files if f.lower().endswith((".jpg", ".jpeg", ".png"))]
            desc_files = [f for f in files if f.lower().endswith(".txt")]
            descriptions = []
            for dfile in sorted(desc_files):
                file_path = os.path.join(timestamp_path, dfile)
                with open(file_path, "r", encoding="utf-8") as f:
                    descriptions.append(f.read().strip())
            full_description = "\n".join(descriptions)
            for img in image_files:
                record = {
                    "timestamp": timestamp,
                    "class": "none",
                    "image_name": img,
                    "description": full_description
                }
                records.append(record)

    # Create a Pandas DataFrame from the records
    df = pd.DataFrame(records)

    # Save the DataFrame as a JSONL file
    output_file = "output.jsonl"
    with open(output_file, "w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            json_line = json.dumps(row.to_dict(), ensure_ascii=False)
            f.write(json_line + "\n")

    print("JSONL file has been created:", output_file)

    return df

# Create a Gradio interface with no input components (a simple button)
# and a DataFrame output to visualize the generated table.
iface = gr.Interface(
    fn=generate_dataframe,
    inputs=[],  # No inputs needed
    outputs=gr.DataFrame(label="Generated Table"),
    title="Auto-Summary for Safety Inspection Cases",
    description="Click the button to generate and visualize the DataFrame (Report)."
)

if __name__ == "__main__":
    iface.launch()