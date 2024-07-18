from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit

spark = SparkSession.builder.appName("ProductCategory").getOrCreate()
# Примерные данные
products_data = [
    (1, "Product A"),
    (2, "Product B"),
    (3, "Product C"),
    (4, "Product D")
]

categories_data = [
    (1, "Category 1"),
    (2, "Category 2"),
    (3, "Category 3")
]

product_category_data = [
    (1, 1),  # Product A -> Category 1
    (1, 2),  # Product A -> Category 2
    (2, 2),  # Product B -> Category 2
    (3, 3)   # Product C -> Category 3
    # Product D не имеет категорий
]

# Создание датафреймов
products_df = spark.createDataFrame(products_data, ["product_id", "product_name"])
categories_df = spark.createDataFrame(categories_data, ["category_id", "category_name"])
product_category_df = spark.createDataFrame(product_category_data, ["product_id", "category_id"])


def get_product_category_pairs_and_orphans(products_df, categories_df, product_category_df):
    # Объединяем продукты с категориями
    product_category_pairs_df = product_category_df \
        .join(products_df, "product_id") \
        .join(categories_df, "category_id") \
        .select("product_name", "category_name")

    # Находим продукты, у которых нет категорий
    products_with_categories_df = product_category_df.select("product_id").distinct()
    orphan_products_df = products_df \
        .join(products_with_categories_df, "product_id", "left_anti") \
        .select("product_name")
    
    return product_category_pairs_df, orphan_products_df


# Получаем результаты
product_category_pairs_df, orphan_products_df = get_product_category_pairs_and_orphans(products_df, categories_df, product_category_df)

# Показать результаты
print("Product - Category Pairs:")
product_category_pairs_df.show()

print("Orphan Products:")
orphan_products_df.show()
