import cv2, os, time, numpy as np, shutil, sys

ASCII_CHARS = np.asarray(list(" .:-=+*#%@"))

def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def rgb_to_ansi256(r, g, b):
    """Map RGB → nearest ANSI 256 color code."""
    r, g, b = int(r / 51), int(g / 51), int(b / 51)
    return 16 + (36 * r) + (6 * g) + b

def frame_to_ascii_color(frame, width=100):
    h, w = frame.shape[:2]
    aspect = h / w
    new_h = int(aspect * width * 0.55)
    frame = cv2.resize(frame, (width, new_h))

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    norm = gray / 255.0
    idx = (norm * (len(ASCII_CHARS) - 1)).astype(int)

    lines = []
    for y in range(new_h):
        row = []
        for x in range(width):
            b, g, r = frame[y, x]
            color = rgb_to_ansi256(r, g, b)
            char = ASCII_CHARS[idx[y, x]]
            row.append(f"\033[38;5;{color}m{char}\033[0m")
        lines.append("".join(row))
    return "\n".join(lines)

def play_ascii_video(video_path, base_width=100, fps=25):
    if not os.path.exists(video_path):
        print(f"File not found: {video_path}")
        return

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Could not open video.")
        return

    delay = 1 / fps
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            cols, _ = shutil.get_terminal_size((100, 40))
            width = min(base_width, cols - 2)
            ascii_img = frame_to_ascii_color(frame, width)

            clear_terminal()
            sys.stdout.write(ascii_img)
            sys.stdout.flush()
            time.sleep(delay)
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        print("\nStopped.")

if __name__ == "__main__":
    path = r"S:\Projects\project11(ASCII video format)\husky.mp4"
    play_ascii_video(path, base_width=100, fps=25)
