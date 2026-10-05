"""
Generate reproducible evaluation audio files (40 samples: 20 clean, 20 noisy)
using pure Python standard library (wave, math, struct, random).
"""

import wave
import math
import struct
import random
import json
from pathlib import Path

def generate_speech_like_wav(filename: Path, duration_sec: float = 3.5, is_noisy: bool = False, seed: int = 42):
    random.seed(seed)
    sample_rate = 16000
    num_samples = int(sample_rate * duration_sec)
    filename.parent.mkdir(parents=True, exist_ok=True)

    # Base frequencies mimicking human vocal formants (F0 ~ 130-220Hz, F1 ~ 500Hz, F2 ~ 1500Hz, F3 ~ 2500Hz)
    f0 = 160.0 + (seed % 60)
    
    with wave.open(str(filename), 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit
        wav_file.setframerate(sample_rate)

        frames = bytearray()
        for i in range(num_samples):
            t = float(i) / sample_rate
            # Syllable modulation (amplitude envelope at 3Hz)
            envelope = 0.5 * (1.0 + math.sin(2.0 * math.pi * 3.0 * t))
            
            # Harmonic voice signal
            voice = (
                0.4 * math.sin(2.0 * math.pi * f0 * t) +
                0.3 * math.sin(2.0 * math.pi * (2 * f0) * t) +
                0.2 * math.sin(2.0 * math.pi * (3 * f0) * t) +
                0.1 * math.sin(2.0 * math.pi * 1500.0 * t)
            ) * envelope

            if is_noisy:
                # Add background gaussian/white noise (SNR ~ 10-15dB)
                noise = random.uniform(-0.25, 0.25)
                # Add subway/traffic low-frequency hum (50Hz - 120Hz)
                hum = 0.15 * math.sin(2.0 * math.pi * 60.0 * t)
                sample_val = voice * 0.6 + noise * 0.3 + hum * 0.1
            else:
                # Clean speech with minimal background noise
                sample_val = voice * 0.85 + random.uniform(-0.01, 0.01)

            # Clamp to 16-bit signed integer [-32768, 32767]
            int_sample = int(max(min(sample_val, 1.0), -1.0) * 32760)
            frames.extend(struct.pack('<h', int_sample))

        wav_file.writeframes(frames)


def main():
    base_dir = Path(__file__).resolve().parent.parent
    eval_json_path = base_dir / "dataset" / "asr" / "evaluation_40.json"
    audio_dir = base_dir / "dataset" / "asr" / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)

    with open(eval_json_path, 'r', encoding='utf-8') as f:
        samples = json.load(f)

    print(f"Generating {len(samples)} evaluation audio WAV files...")
    for idx, item in enumerate(samples):
        out_file = audio_dir / item["audio_file"]
        is_noisy = (item["group"] == "noisy")
        # vary duration realistically (2.5s to 5.0s)
        duration = 3.0 + ((idx % 5) * 0.4)
        generate_speech_like_wav(out_file, duration_sec=duration, is_noisy=is_noisy, seed=idx + 100)
        item["file_path"] = str(out_file.relative_to(base_dir)).replace("\\", "/")

    # Update evaluation_40.json with local paths
    with open(eval_json_path, 'w', encoding='utf-8') as f:
        json.dump(samples, f, ensure_ascii=False, indent=2)

    print(f"Successfully generated {len(samples)} WAV files in {audio_dir}")

if __name__ == "__main__":
    main()
