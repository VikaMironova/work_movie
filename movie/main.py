import os
import re
import subprocess

INPUT_PATH = '/home/vika/print/movie/source/blood_and_blood'
OUTPUT_DIR = '/home/vika/print/movie/movie/spaces/ready'


def gather_sequences(base_path):
    sequences = {
        'blood': [],
        'blood_mist': []
    }

    for root, _, files in os.walk(base_path):
        for filename in files:
            match_blood = re.match(r'blood\.(\d{3})\.jpg$', filename)
            match_blood_mist = re.match(r'blood_mist_(\d{3})\.jpg$', filename)

            if match_blood:
                frame_num = int(match_blood.group(1))
                if 1 <= frame_num <= 118:
                    sequences['blood'].append(os.path.join(root, filename))
            elif match_blood_mist:
                frame_num = int(match_blood_mist.group(1))
                if 1 <= frame_num <= 307:
                    sequences['blood_mist'].append(os.path.join(root, filename))

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