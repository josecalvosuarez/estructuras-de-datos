# compare_files.py
#
# Writes the same dataset as a text file and as a binary file, then compares
# file size and write/read speed. Run it as-is:
#
#   python compare_files.py

import os
import struct
import time

RECORD_COUNT = 10_000_000
TEXT_FILE = "sensor_readings.txt"
BINARY_FILE = "sensor_readings.bin"

# Each record is one sensor reading: an integer id + a float value.
# 'i' = 4-byte int, 'd' = 8-byte double -> every binary record is 12 bytes,
# no matter how big the numbers get. A text record's size depends on how
# many digits the numbers happen to have.
RECORD_FORMAT = "id"
RECORD_SIZE = struct.calcsize(RECORD_FORMAT)


def generate_records(count):
    # Dividing by 3 produces long, non-terminating decimals (e.g. 333333.3333333333)
    # for most ids, which is exactly the kind of float that looks compact in binary
    # but expands to many characters once converted to text.
    return [(i, i / 3) for i in range(count)]


def write_text(records, filename):
    start = time.perf_counter()
    with open(filename, "w") as f:
        for record_id, value in records:
            f.write(f"{record_id},{value}\n")
    return time.perf_counter() - start


def read_text(filename):
    start = time.perf_counter()
    records = []
    with open(filename, "r") as f:
        for line in f:
            record_id, value = line.strip().split(",")
            records.append((int(record_id), float(value)))
    return records, time.perf_counter() - start


def write_binary(records, filename):
    start = time.perf_counter()
    with open(filename, "wb") as f:
        for record_id, value in records:
            f.write(struct.pack(RECORD_FORMAT, record_id, value))
    return time.perf_counter() - start


def read_binary(filename):
    start = time.perf_counter()
    records = []
    with open(filename, "rb") as f:
        while chunk := f.read(RECORD_SIZE):
            records.append(struct.unpack(RECORD_FORMAT, chunk))
    return records, time.perf_counter() - start


def report(label, filename, write_time, read_time):
    size = os.path.getsize(filename)
    print(f"{label}")
    print(f"  File size:  {size:,} bytes")
    print(f"  Write time: {write_time:.3f} s")
    print(f"  Read time:  {read_time:.3f} s")


def main():
    print(f"Generating {RECORD_COUNT:,} records...\n")
    records = generate_records(RECORD_COUNT)

    text_write_time = write_text(records, TEXT_FILE)
    _, text_read_time = read_text(TEXT_FILE)
    report("Text file (.txt)", TEXT_FILE, text_write_time, text_read_time)

    print()

    binary_write_time = write_binary(records, BINARY_FILE)
    _, binary_read_time = read_binary(BINARY_FILE)
    report("Binary file (.bin)", BINARY_FILE, binary_write_time, binary_read_time)

    text_size = os.path.getsize(TEXT_FILE)
    binary_size = os.path.getsize(BINARY_FILE)
    print(f"\nBinary file is {text_size / binary_size:.1f}x smaller than the text file.")
    print(f"Binary write was {text_write_time / binary_write_time:.1f}x faster; "
          f"binary read was {text_read_time / binary_read_time:.1f}x faster.")


if __name__ == "__main__":
    main()
