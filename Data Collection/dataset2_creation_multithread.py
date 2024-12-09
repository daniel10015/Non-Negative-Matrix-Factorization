import cv2
import numpy as np
import os
from concurrent.futures import ThreadPoolExecutor

def process_frame(frame, frame_index, video_title, output_folder):
    """Processes a single frame and saves it as a CSV file."""
    # Convert to RGB (OpenCV loads in BGR format)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

    # Save to CSV
    output_file = os.path.join(output_folder, f"{video_title}_frame{frame_index}.csv")
    np.savetxt(output_file, frame, delimiter=',', fmt='%.8f')
    print(f"Saved {output_file}")

def process_video_multithreaded(video_path, output_folder, num_threads=4):
    """Processes video frames concurrently using multithreading."""
    os.makedirs(output_folder, exist_ok=True)
    video_title = os.path.splitext(os.path.basename(video_path))[0]

    cap = cv2.VideoCapture(video_path)
    frame_index = 0

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Submit frame processing to thread pool
            futures.append(executor.submit(process_frame, frame, frame_index, video_title, output_folder))
            frame_index += 1

        # Wait for all threads to complete
        for future in futures:
            future.result()

    cap.release()
    print("Processing complete.")

video_file = "../friend_jazz_drumming.mov"  
output_directory = "Data/Dataset2"  
process_video_multithreaded(video_file, output_directory, num_threads=16)
