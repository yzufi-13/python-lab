import os
import hashlib
def _resolve_path(path: str) -> str:
    """
    Tries to make the file path usable across environments.
    If the given path doesn't exist, tries basename in current directory.
    """
    if os.path.isfile(path):
        return path
    base = os.path.basename(path)
    if os.path.isfile(base):
        return base
    return path
def generate_file_hashes(*file_paths):
    results = {}
    for raw_path in file_paths:
        path = _resolve_path(raw_path)
        try:
            sha256 = hashlib.sha256()
            with open(path, "rb") as f:
                for chunk in iter(lambda: f.read(1024 * 1024), b""):
                    sha256.update(chunk)
            results[raw_path] = sha256.hexdigest()
        except FileNotFoundError:
            print(f"Помилка: файл не знайдено -> {raw_path}")
        except OSError as e:
            print(f"Помилка читання файлу -> {raw_path}. Деталі: {e}")
    return results
if __name__ == "__main__":
    hashes = generate_file_hashes("/mnt/data/apache_logs.txt")
    print("2) Hashes:", hashes)

