from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

# Підключення до MongoDB
client = MongoClient(
    "mongodb+srv://mongodbuser:password@cluster0.mlqna.mongodb.net/",
    server_api=ServerApi('1')
)

# Вибір бази даних і колекції
db = client.book
cats_collection = db.cats

# Вставка початкових даних
result_one = cats_collection.insert_one(
    {
        "name": "barsik",
        "age": 3,
        "features": ["ходить в капці", "дає себе гладити", "рудий"],
    }
)
print(f"Inserted ID: {result_one.inserted_id}")

result_many = cats_collection.insert_many(
    [
        {
            "name": "Lama",
            "age": 2,
            "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
        },
        {
            "name": "Liza",
            "age": 4,
            "features": ["ходить в лоток", "дає себе гладити", "білий"],
        },
    ]
)
print(f"Inserted IDs: {result_many.inserted_ids}")

# Функція для читання всіх записів
def read_all():
    try:
        print("All records:")
        for el in cats_collection.find({}):
            print(el)
    except Exception as e:
        print(f"Error reading records: {e}")

# Функція для пошуку кота за ім'ям
def find_by_name():
    try:
        name = input("Enter the name of the cat to search: ")
        cat = cats_collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print(f"No cat found with name {name}")
    except Exception as e:
        print(f"Error finding cat: {e}")

# Функція для оновлення віку кота
def update_age():
    try:
        name = input("Enter the name of the cat to update: ")
        new_age = int(input("Enter the new age: "))
        result = cats_collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.matched_count > 0:
            print(f"Updated age for cat: {name}")
        else:
            print(f"No cat found with name {name}")
    except Exception as e:
        print(f"Error updating age: {e}")

# Функція для додавання нової характеристики
def update_feature():
    try:
        name = input("Enter the name of the cat to update: ")
        new_feature = input("Enter the new feature to add: ")
        result = cats_collection.update_one({"name": name}, {"$push": {"features": new_feature}})
        if result.matched_count > 0:
            print(f"Added feature to cat: {name}")
        else:
            print(f"No cat found with name {name}")
    except Exception as e:
        print(f"Error updating feature: {e}")

# Функція для видалення кота за ім'ям
def delete():
    try:
        name = input("Enter the name of the cat to delete: ")
        result = cats_collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"Deleted cat: {name}")
        else:
            print(f"No cat found with name {name}")
    except Exception as e:
        print(f"Error deleting cat: {e}")

# Функція для видалення всіх записів
def delete_all():
    try:
        result = cats_collection.delete_many({})
        print(f"Deleted {result.deleted_count} records.")
    except Exception as e:
        print(f"Error deleting all records: {e}")

# Виклик функцій для перевірки
if __name__ == "__main__":
    # Викликайте функції тут для тестування
    read_all()
    find_by_name()
    update_age()
    update_feature()
    # delete()
    # delete_all()
