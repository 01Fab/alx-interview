import re
import sys

total_size = 0
status_codes = {
    "200": 0,
    "301": 0,
    "400": 0,
    "401": 0,
    "403": 0,
    "404": 0,
    "405": 0,
    "500": 0,
}
lines_processed = 0

try:
    for line in sys.stdin:
        lines_processed += 1
        match = re.search(r"(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - \[(?P<date>.*)\] \"GET /projects/260 HTTP/1.1\" (?P<status_code>\d{3}) (?P<file_size>\d+)", line)
        if match:
            try:
                file_size = int(match.group("file_size"))
                total_size += file_size
                status_codes[match.group("status_code")] += 1
            except ValueError:
                pass  # Ignore invalid file sizes

        if lines_processed % 10 == 0:
            print("File size:", total_size)
            for code in sorted(status_codes):
                count = status_codes[code]
                if count > 0:
                    print(f"{code}: {count}")

except KeyboardInterrupt:
    print("File size:", total_size)
    for code in sorted(status_codes):
        count = status_codes[code]
        if count > 0:
            print(f"{code}: {count}")
