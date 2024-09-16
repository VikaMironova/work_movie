import os
import re
import subprocess
from collections import defaultdict

# Укажите пути к входным и выходным директориям
INPUT_PATH = ''
OUTPUT_DIR = ''


def gather_sequences(base_path):
    sequences = defaultdict(list)

    # Обновленное регулярное выражение для захвата различных форматов имен файлов
    for root, _, files in os.walk(base_path):
        for filename in files:
            # Регулярное выражение для различных форматов
            match = re.match(r'(.+?)[_.\s](\d{3,8})\.jpg$', filename)
            if match:
                sequence_name = match.group(1).strip()  # Убираем лишние пробелы
                frame_num = int(match.group(2))
                sequences[sequence_name].append(os.path.join(root, filename))

    return sequences


def create_video_from_sequence(sequence_name, sequence_files, output_dir):
    if not sequence_files:
        return

    input_file_list = os.path.join(output_dir, f"{sequence_name}_input.txt")
    with open(input_file_list, 'w') as f:
        for file_path in sorted(sequence_files):
            f.write(f"file '{file_path}'\n")

    output_file = os.path.join(output_dir, f"{sequence_name}.mov")
    cmd = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', input_file_list,
        '-c:v', 'mjpeg',
        '-q:v', '3',
        '-r', '24',
        output_file
    ]

    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while creating video for {sequence_name}: {e.stderr.decode()}")
    finally:
        os.remove(input_file_list)


def main(input_path, output_dir):
    sequences = gather_sequences(input_path)
    for sequence_name, sequence_files in sequences.items():
        create_video_from_sequence(sequence_name, sequence_files, output_dir)


if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    main(INPUT_PATH, OUTPUT_DIR)