import os
def _resolve_path(path: str) -> str:
    if os.path.isfile(path):
        return path
    base = os.path.basename(path)
    if os.path.isfile(base):
        return base
    return path
def filter_ips(input_file_path, output_file_path, allowed_ips):
    counts = {}
    input_path = _resolve_path(input_file_path)
    output_path = output_file_path
    try:
        with open(input_path, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                ip = line.split()[0]

                if ip in allowed_ips:
                    counts[ip] = counts.get(ip, 0) + 1
        try:
            with open(output_path, "w", encoding="utf-8") as out:
                for ip, c in sorted(counts.items(), key=lambda x: (-x[1], x[0])):
                    out.write(f"{ip} - {c}\n")
            print(f"Report saved to: {output_path}")
        except OSError as e:
            print(f"Помилка запису у вихідний файл -> {output_path}. Деталі: {e}")

    except FileNotFoundError:
        print(f"Помилка: вхідний файл не знайдено -> {input_file_path}")
    except OSError as e:
        print(f"Помилка читання вхідного файлу -> {input_file_path}. Деталі: {e}")
    return counts
if __name__ == "__main__":
    allowed_ips = [
        "83.149.9.216",
        "66.249.73.135",
        "80.91.33.133",
    ]
    counts = filter_ips(
        input_file_path="/mnt/data/apache_logs.txt",
        output_file_path="allowed_ips_report.txt",
        allowed_ips=allowed_ips
    )
    print("3) Allowed IP counts:", counts)
