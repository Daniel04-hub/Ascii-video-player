import cv2
import os
import time
import numpy as np
import shutil

# High-resolution ASCII gradient (dark → light)
ASCII_CHARS = np.asarray(list(" .:-=+*#%@"))

def frame_to_ascii(frame, new_width=100):
    """Convert a single video frame to ASCII art."""
    # Resize maintaining aspect ratio for terminal
    height, width = frame.shape[:2]
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.35)
    frame = cv2.resize(frame, (new_width, new_height))

    # Convert to grayscale and enhance contrast
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    # Normalize brightness to 0–1
    norm = gray / 255.0

    # Map brightness values to ASCII chars
    indices = (norm * (len(ASCII_CHARS) - 1)).astype(int)
    ascii_frame = "\n".join(
        "".join(ASCII_CHARS[p] for p in row)
        for row in indices
    )
    return ascii_frame

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def play_ascii_video(video_path, base_width=100, fps_limit=25):
    """Play any video as ultra-clear ASCII animation."""
    if not os.path.exists(video_path):
        print(f"❌ File not found: {video_path}")
        return

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("❌ Could not open video.")
        return

    frame_delay = 1 / fps_limit

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                # loop from start
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            # dynamically fit terminal width
            term_cols, _ = shutil.get_terminal_size((100, 40))
            width = min(base_width, term_cols - 2)

            # Convert frame → ASCII
            ascii_frame = frame_to_ascii(frame, new_width=width)

            # Show frame
            clear_terminal()
            print(ascii_frame)
            time.sleep(frame_delay)

    except KeyboardInterrupt:
        print("\n🛑 Stopped by user.")
    finally:
        cap.release()

# -------------------------
# Example usage
# -------------------------
if __name__ == "__main__":
    path = r"S:\Projects\project11(ASCII video format)\husky.mp4"
    play_ascii_video(path, base_width=120, fps_limit=25)
