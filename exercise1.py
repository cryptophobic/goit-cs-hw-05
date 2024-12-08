import asyncio
import os
import shutil
from pathlib import Path
import logging
from argparse import ArgumentParser


# Ініціалізація логування
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def copy_file(src_file: Path, dst_folder: Path):
    """
    Асинхронно копіює файл у підпапку на основі його розширення.
    """
    try:
        # Створюємо підпапку для файлів відповідного типу, якщо вона не існує
        extension_folder = dst_folder / (src_file.suffix.lstrip('.') or 'no_extension')
        extension_folder.mkdir(parents=True, exist_ok=True)

        # Копіюємо файл
        dst_file = extension_folder / src_file.name
        shutil.copy2(src_file, dst_file)
        logging.info(f"Копіювання завершено: {src_file} -> {dst_file}")
    except Exception as e:
        logging.error(f"Помилка при копіюванні {src_file}: {e}")


async def read_folder(src_folder: Path, dst_folder: Path):
    """
    Асинхронно читає всі файли у вихідній папці та копіює їх у відповідні підпапки.
    """
    tasks = []
    try:
        for root, _, files in os.walk(src_folder):
            for file in files:
                src_file = Path(root) / file
                tasks.append(copy_file(src_file, dst_folder))

        await asyncio.gather(*tasks)
        logging.info("Сортування файлів завершено.")
    except Exception as e:
        logging.error(f"Помилка при читанні папки {src_folder}: {e}")


def main():
    # Налаштування аргументів командного рядка
    parser = ArgumentParser(description="Скрипт для сортування файлів за розширенням")
    parser.add_argument("--src", type=str, help="Шлях до вихідної папки")
    parser.add_argument("--dst", type=str, help="Шлях до цільової папки")

    args = parser.parse_args()

    src_folder = Path(args.src)
    dst_folder = Path(args.dst)

    if not src_folder.exists() or not src_folder.is_dir():
        logging.error(f"Вихідна папка {src_folder} не існує або не є директорією.")
        return

    dst_folder.mkdir(parents=True, exist_ok=True)

    # Запускаємо асинхронну обробку
    asyncio.run(read_folder(src_folder, dst_folder))


if __name__ == "__main__":
    main()
