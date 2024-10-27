import os
import shutil
from PIL import Image
import imagehash
from collections import defaultdict

def find_and_sort_duplicates(folder_path, duplicates_folder_path):
    # Создание папки для дубликатов, если она не существует
    if not os.path.exists(duplicates_folder_path):
        os.makedirs(duplicates_folder_path)
    
    # Словарь для хранения хэшей и списков путей к дубликатам
    hashes = {}
    duplicates = defaultdict(list)

    # Перебор файлов в указанной папке
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Проверка, является ли файл изображением
        try:
            with Image.open(file_path) as img:
                # Вычисляем хэш изображения
                img_hash = imagehash.phash(img)
                
                # Проверяем, существует ли уже такой хэш
                if img_hash in hashes:
                    # Добавляем текущий файл в список дубликатов для данного хэша
                    duplicates[img_hash].append(file_path)
                    
                    # Перемещаем файл дубликата в папку дубликатов
                    new_path = os.path.join(duplicates_folder_path, filename)
                    shutil.move(file_path, new_path)
                else:
                    hashes[img_hash] = file_path
                    duplicates[img_hash].append(file_path)  # Добавляем оригинал в список
        except (IOError, SyntaxError):
            print(f"Файл {file_path} не является изображением или поврежден.")

    # Сортировка хэшей по количеству дубликатов от большего к меньшему
    sorted_duplicates = sorted(duplicates.items(), key=lambda item: len(item[1]), reverse=True)
    
    return sorted_duplicates

# Пример использования
folder_path = r"C:\Users\denis\Pictures"  # Путь к папке с фотографиями
duplicates_folder_path = r"C:\Users\denis\Pictures\Duplicates"  # Путь к папке для дубликатов

sorted_duplicates = find_and_sort_duplicates(folder_path, duplicates_folder_path)

if sorted_duplicates:
    print("Дубликаты изображений (отсортированы по количеству):")
    for img_hash, files in sorted_duplicates:
        if len(files) > 1:  # Учитываем только хэши с дубликатами
            print(f"\nИзображение с хэшем {img_hash} имеет {len(files) - 1} дубликатов:")
            for file in files:
                print(f"  - {file}")
else:
    print("Дубликаты не найдены.")
