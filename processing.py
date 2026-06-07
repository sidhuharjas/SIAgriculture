import shutil
from pathlib import Path

def process_dataset():
    # Define paths based on your repo structure
    base_dir = Path("videos")
    output_dir = Path("postprocessed")
    
    # Create the postprocessed directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    if not base_dir.exists():
        print(f"Error: Could not find the '{base_dir}' directory.")
        return

    # Iterate through the video directories (VideoOneShorten, etc.)
    for video_dir in base_dir.iterdir():
        if not video_dir.is_dir():
            continue
            
        video_name = video_dir.name
        frames_dir = video_dir / "frames"
        
        if not frames_dir.exists():
            print(f"Skipping {video_name} - no 'frames' directory found.")
            continue
            
        print(f"Processing {video_name}...")
        
        # Create a matching output directory for this video
        out_video_dir = output_dir / video_name
        out_video_dir.mkdir(parents=True, exist_ok=True)
        
        # Iterate through batches sequentially
        for batch_dir in sorted(frames_dir.iterdir()):
            if not batch_dir.is_dir() or not batch_dir.name.startswith("batch_"):
                continue
                
            batch_name = batch_dir.name
            
            # Iterate through frames and copy them over
            for frame_file in sorted(batch_dir.glob("*.png")):
                # Prefix with batch name to avoid overwriting 
                new_filename = f"{batch_name}_{frame_file.name}"
                dest_path = out_video_dir / new_filename
                
                shutil.copy2(frame_file, dest_path)
                
    print(f"\nSuccess! All frames have been flattened and copied to the '{output_dir}' directory.")

if __name__ == "__main__":
    process_dataset()