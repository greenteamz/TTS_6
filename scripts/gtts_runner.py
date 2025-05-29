import os
from gtts import gTTS
import time

STORY_DIR = "stories_text"
OUTPUT_DIR = "gtts"
COUNT_FILE = "processed_count.txt"
STORIES_PER_RUN = 10

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Read processed count
if os.path.exists(COUNT_FILE):
    with open(COUNT_FILE, "r") as f:
        start_idx = int(f.read().strip())
else:
    start_idx = 0

# Collect files
all_files = sorted([f for f in os.listdir(STORY_DIR) if f.endswith(".txt")])
to_process = all_files[start_idx : start_idx + STORIES_PER_RUN]

success_count = 0

for i, filename in enumerate(to_process, start=start_idx + 1):
    txt_path = os.path.join(STORY_DIR, filename)
    base_name = os.path.splitext(filename)[0]
    mp3_path = os.path.join(OUTPUT_DIR, f"{base_name}.mp3")

    #with open(txt_path, "r", encoding="utf-8") as f:
     #   text = f.read().strip()

    with open(txt_path, "r", encoding="utf-8") as f:
        text = f.read().replace('\n', ' ').strip()
    
    # Add closing watermark and disclaimer
    closing_note = (
        " comment பண்ணுங்க.                                                                                    "
        "This video is part of an artistic Tamil audio series that explores the emotional and psychological depth "
        "of human relationships through narrated fiction. All characters and events are fictional and intended for "
        "mature literary appreciation."
    )
    
    text += closing_note

    try:
        tts = gTTS(text=text, lang='ta')
        tts.save(mp3_path)
        success_count += 1
        print(f"✅ Converted: {filename} to {mp3_path}")
    except Exception as e:
        print(f"❌ Error processing {filename}: {e}")
        success_count += 1
        break  # ❗ Stop further processing on any failure

    time.sleep(10)

# Update count
with open(COUNT_FILE, "w") as f:
    f.write(str(start_idx + success_count))
    print(f"✅ Count: {start_idx} + {success_count}")
