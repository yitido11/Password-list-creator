import random
import string
import time
from pathlib import Path
import shutil
import os
import sys

# --------------------------
# Terminal colors
# --------------------------
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

# --------------------------
# Clear terminal function
# --------------------------
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# --------------------------
# Header function
# --------------------------
def print_header():
    print(f"{Colors.OKGREEN}{Colors.BOLD}Wordlist Generator by Yitido{Colors.ENDC}\n")

# --------------------------
# Step 1: Target size or word count
# --------------------------
clear_screen()
print_header()
while True:
    target_input = input("Enter wordlist size (GB) or word count (e.g., 5G or 1000000K): ").strip().upper()
    if target_input.endswith('G'):
        TARGET_SIZE_GB = float(target_input[:-1])
        target_bytes = TARGET_SIZE_GB * 1024**3
        target_words = None
        break
    elif target_input.endswith('K'):
        target_words = int(target_input[:-1])
        target_bytes = None
        TARGET_SIZE_GB = None
        break
    else:
        print(f"{Colors.WARNING}Invalid input format. Use 'G' for GB or 'K' for number of words. Example: 5G or 1000000K{Colors.ENDC}")

# --------------------------
# Step 2: Words to use
# --------------------------
clear_screen()
print_header()
words_input = input("Enter words to use, separated by commas (e.g., cat,car,house,book): ").strip()
seeds = [w.strip() for w in words_input.split(",") if w.strip()]
if not seeds:
    raise SystemExit(f"{Colors.FAIL}Error: You must enter at least one word!{Colors.ENDC}")

# --------------------------
# Step 3: Minimum and maximum extra character length
# --------------------------
clear_screen()
print_header()
while True:
    try:
        MIN_LEN = int(input("Minimum additional character length (e.g., 8): ").strip())
        MAX_LEN = int(input("Maximum additional character length (e.g., 16): ").strip())
        if MIN_LEN <= 0 or MAX_LEN < MIN_LEN:
            print(f"{Colors.WARNING}Invalid values. Ensure MIN <= MAX and MIN > 0.{Colors.ENDC}")
        else:
            break
    except ValueError:
        print(f"{Colors.WARNING}Please enter numeric values only.{Colors.ENDC}")

# --------------------------
# Character pools
# --------------------------
letters = string.ascii_letters
digits = string.digits
special_chars = "!@#$%^&*()-_=+[]{};:,.<>?/"
all_chars = letters + digits + special_chars
REPORT_EVERY = 100000  # Report progress every X words

# --------------------------
# Output file
# --------------------------
downloads = Path.home() / "storage" / "downloads"
downloads.mkdir(parents=True, exist_ok=True)
out_path = downloads / "wordlist_generated.txt"

# --------------------------
# Disk-based writing and AFK mode progress
# --------------------------
bytes_written = 0
counter = 0
start_time = time.time()

def print_progress_bar(fraction, length=30):
    filled = int(length * fraction)
    bar = '█' * filled + '-' * (length - filled)
    print(f"{Colors.OKBLUE}[{bar}] {fraction*100:.2f}%{Colors.ENDC}")

# --------------------------
# Wordlist generation loop
# --------------------------
with out_path.open("w", encoding="utf-8") as f:
    while True:
        # Check target
        if target_words and counter >= target_words:
            break
        if target_bytes and bytes_written >= target_bytes:
            break

        # Generate word
        base = random.choice(seeds)
        mixed_word = "".join(random.choice([c.lower(), c.upper()]) for c in base)
        extra_len = random.randint(MIN_LEN, MAX_LEN)
        extra = "".join(random.choice(all_chars) for _ in range(extra_len))
        combined = random.choice([mixed_word + extra, extra + mixed_word, mixed_word, extra])

        # Write to file
        f.write(combined + "\n")
        bytes_written += len(combined.encode('utf-8')) + 1
        counter += 1

        # Status report
        if counter % REPORT_EVERY == 0:
            elapsed = time.time() - start_time
            speed = bytes_written / elapsed if bytes_written else 1
            if target_bytes:
                remaining_bytes = max(target_bytes - bytes_written, 0)
                eta_sec = remaining_bytes / speed
            else:
                avg_bytes_per_word = bytes_written / counter
                remaining_words = target_words - counter
                eta_sec = remaining_words * avg_bytes_per_word / speed
            eta_min = eta_sec / 60
            fraction_done = (bytes_written / target_bytes) if target_bytes else (counter / target_words)
            
            # AFK mode: clear screen and single-page view
            clear_screen()
            print_header()
            print(f"{Colors.OKCYAN}Generated words: {counter}{Colors.ENDC}")
            print(f"{Colors.OKCYAN}Approximate file size: {(bytes_written/1024/1024/1024 if bytes_written else 0):.2f} GB{Colors.ENDC}")
            print(f"{Colors.OKCYAN}Estimated remaining time: {eta_min:.1f} minutes{Colors.ENDC}")
            print_progress_bar(fraction_done)

print(f"{Colors.OKGREEN}✓ Wordlist successfully generated: {out_path} ({'approx. '+str(TARGET_SIZE_GB)+' GB' if TARGET_SIZE_GB else str(target_words)+' words'}){Colors.ENDC}")
