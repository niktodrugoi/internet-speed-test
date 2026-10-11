import argparse
import time

import requests


REQUESTS_COUNT = 10
CHUNK_SIZE = 64 * 1024
TIMEOUT = 60


def download_file(url):
    """Скачивает файл и возвращает время загрузки и размер данных."""
    start_time = time.perf_counter()
    downloaded_bytes = 0

    with requests.get(url, stream=True, timeout=TIMEOUT) as response:
        response.raise_for_status()

        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                downloaded_bytes += len(chunk)

    elapsed_time = time.perf_counter() - start_time

    return elapsed_time, downloaded_bytes


def main():
    parser = argparse.ArgumentParser(
        description="Измерение скорости скачивания файла"
    )
    parser.add_argument("url", help="Прямая ссылка на файл для скачивания")
    args = parser.parse_args()

    total_time = 0
    total_bytes = 0
    successful_requests = 0

    print(f"Адрес: {args.url}")
    print(f"Количество запросов: {REQUESTS_COUNT}\n")

    for number in range(1, REQUESTS_COUNT + 1):
        try:
            elapsed_time, downloaded_bytes = download_file(args.url)
        except requests.RequestException as error:
            print(f"Запрос {number:2}: ошибка — {error}")
            continue

        successful_requests += 1
        total_time += elapsed_time
        total_bytes += downloaded_bytes

        size_mb = downloaded_bytes / 1_000_000
        speed = size_mb / elapsed_time if elapsed_time > 0 else 0

        print(
            f"Запрос {number:2}: "
            f"{elapsed_time:.2f} сек., "
            f"{size_mb:.2f} МБ, "
            f"{speed:.2f} МБ/с"
        )

    print("\n--- Итоговые результаты ---")
    print(f"Успешных запросов: {successful_requests} из {REQUESTS_COUNT}")

    if successful_requests == 0:
        print("Не удалось выполнить ни одного запроса.")
        return

    average_time = total_time / successful_requests
    total_mb = total_bytes / 1_000_000
    average_speed = total_mb / total_time if total_time > 0 else 0

    print(f"Среднее время запроса: {average_time:.2f} сек.")
    print(f"Всего скачано: {total_mb:.2f} МБ")
    print(f"Общее время скачивания: {total_time:.2f} сек.")
    print(f"Средняя скорость: {average_speed:.2f} МБ/с")


if __name__ == "__main__":
    main()