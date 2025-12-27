import re
import hashlib
from collections import defaultdict
from typing import Dict, List
STATUS_RE = re.compile(r'"\s*(\d{3})\s')
IP_RE = re.compile(r'^(\d{1,3}(?:\.\d{1,3}){3})\b')
def analyze_log_file(log_file_path: str) -> Dict[int, int]:
    codes: Dict[int, int] = defaultdict(int)
    try:
        with open(log_file_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                m = STATUS_RE.search(line)
                if m:
                    code = int(m.group(1))
                    codes[code] += 1
    except FileNotFoundError:
        print(f"Помилка: файл не знайдено -> {log_file_path}")
        return {}
    except OSError as e:
        print(f"Помилка читання файлу -> {log_file_path}. Деталі: {e}")
        return {}
    return dict(codes)
def generate_file_hashes(*file_paths: str) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for path in file_paths:
        try:
            sha = hashlib.sha256()
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(1024 * 1024), b""):
                    sha.update(chunk)
            result[path] = sha.hexdigest()
        except FileNotFoundError:
            print(f"Помилка: файл не знайдено -> {path}")
        except OSError as e:
            print(f"Помилка читання файлу -> {path}. Деталі: {e}")
    return result
def filter_ips(input_file_path: str, output_file_path: str, allowed_ips: List[str]) -> Dict[str, int]:
    allowed_set = set(allowed_ips)
    counts: Dict[str, int] = defaultdict(int)
    try:
        with open(input_file_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                m = IP_RE.match(line)
                if not m:
                    continue
                ip = m.group(1)
                if ip in allowed_set:
                    counts[ip] += 1
        try:
            with open(output_file_path, "w", encoding="utf-8") as out:
                for ip in sorted(counts.keys()):
                    out.write(f"{ip} - {counts[ip]}\n")
        except OSError as e:
            print(f"Помилка запису у вихідний файл -> {output_file_path}. Деталі: {e}")
            return {}
    except FileNotFoundError:
        print(f"Помилка: вхідний файл не знайдено -> {input_file_path}")
        return {}
    except OSError as e:
        print(f"Помилка читання вхідного файлу -> {input_file_path}. Деталі: {e}")
        return {}
    return dict(counts)
if __name__ == "__main__":
    log_path = "apache_logs.txt"
    print("1) HTTP codes:", analyze_log_file(log_path))
    print("2) Hashes:", generate_file_hashes(log_path))
    allowed_ips = [
        "127.0.0.1",
        "192.168.0.1",
        "10.0.0.5",
    ]
    print("3) Allowed IP counts:", filter_ips(log_path, "allowed_ips_report.txt", allowed_ips))