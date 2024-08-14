import cv2
import numpy as np
import os
from tqdm import tqdm
import json
from skimage.metrics import structural_similarity as ssim

def is_blurry(frame, threshold=100.0):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()
    return variance < threshold

def compute_correlation(frame1, frame2, resize_dims=None):
    gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    
    if resize_dims:
        gray1 = cv2.resize(gray1, resize_dims)
        gray2 = cv2.resize(gray2, resize_dims)
    
    return ssim(gray1, gray2)

def save_frame(frame, output_dir, index, augment=False):
    frame_filename = f"{index:04d}.jpg"
    frame_path = os.path.join(output_dir, frame_filename)
    cv2.imwrite(frame_path, frame)
    
    if augment:
        flipped_frame = cv2.flip(frame, 1)
        flipped_filename = f"{index:04d}_flipped.jpg"
        flipped_path = os.path.join(output_dir, flipped_filename)
        cv2.imwrite(flipped_path, flipped_frame)
        return frame_filename, flipped_filename
    return frame_filename

def process_video(video_path, output_dir, blur_threshold=100.0, correlation_threshold=None, resize_dims=None, augment=False):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    cap = cv2.VideoCapture(video_path)
    prev_frame = None
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    metadata = []
    
    for i in tqdm(range(frame_count), desc=f'Processing {os.path.basename(video_path)}'):
        ret, frame = cap.read()
        if not ret:
            break
        
        if resize_dims:
            frame = cv2.resize(frame, resize_dims)
        
        if is_blurry(frame, blur_threshold):
            continue
        
        if prev_frame is not None and correlation_threshold is not None:
            correlation = compute_correlation(prev_frame, frame, resize_dims=resize_dims)
            if correlation > correlation_threshold:
                continue
        
        frame_filename = save_frame(frame, output_dir, i, augment)
        metadata.append({
            'frame': frame_filename,
            'index': i
        })
        
        prev_frame = frame
    
    cap.release()
    
    with open(os.path.join(output_dir, 'metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=4)
    
    print(f"Processing complete. Extracted frames saved to {output_dir}.")

def process_videos_in_folder(folder_path, output_folder, blur_threshold=100.0, correlation_threshold=None, resize_dims=None, augment=False):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for filename in tqdm(os.listdir(folder_path), desc='Processing videos'):
        video_path = os.path.join(folder_path, filename)
        if os.path.isfile(video_path) and filename.lower().endswith(('.mp4', '.avi', '.mov')):
            video_output_dir = os.path.join(output_folder, os.path.splitext(filename)[0])
            process_video(video_path, video_output_dir, blur_threshold, correlation_threshold, resize_dims, augment)

if __name__ == "__main__":
    # Example configuration
    input_folder = 'videos'  # Set this to your input folder path
    output_folder = 'processed_videos'  # Set this to your output folder path
    
    # Set the parameters as needed
    blur_threshold = 100.0
    correlation_threshold = 0.2  # Set to None to skip correlation computation
    resize_dims = (640, 480)  # Set to None for no resizing
    augment = False  # Set to True to enable augmentation

    process_videos_in_folder(input_folder, output_folder, 
                             blur_threshold=blur_threshold,
                             correlation_threshold=correlation_threshold,
                             resize_dims=resize_dims,
                             augment=augment)
