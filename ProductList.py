import os
import sqlite3
from typing import List, Dict, Optional


class ProductManager:
    def __init__(self, db_name: str = "MyProduct.db"):
        self.db_name = db_name
        self.db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), db_name)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self) -> None:
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS Products (
                    productID INTEGER PRIMARY KEY AUTOINCREMENT,
                    productName TEXT NOT NULL,
                    productPrice INTEGER NOT NULL
                )
                """
            )

    def insert_product(self, product_name: str, product_price: int) -> int:
        with self.conn:
            cursor = self.conn.execute(
                "INSERT INTO Products (productName, productPrice) VALUES (?, ?)",
                (product_name, product_price),
            )
            return int(cursor.lastrowid)

    def update_product(self, product_id: int, product_name: Optional[str] = None, product_price: Optional[int] = None) -> None:
        if product_name is None and product_price is None:
            raise ValueError("수정할 값이 없습니다.")

        fields = []
        values = []
        if product_name is not None:
            fields.append("productName = ?")
            values.append(product_name)
        if product_price is not None:
            fields.append("productPrice = ?")
            values.append(product_price)

        values.append(product_id)
        with self.conn:
            self.conn.execute(
                f"UPDATE Products SET {', '.join(fields)} WHERE productID = ?",
                values,
            )

    def delete_product(self, product_id: int) -> None:
        with self.conn:
            self.conn.execute("DELETE FROM Products WHERE productID = ?", (product_id,))

    def select_products(self, product_id: Optional[int] = None) -> List[Dict[str, object]]:
        if product_id is None:
            rows = self.conn.execute("SELECT productID, productName, productPrice FROM Products ORDER BY productID").fetchall()
        else:
            rows = self.conn.execute(
                "SELECT productID, productName, productPrice FROM Products WHERE productID = ? ORDER BY productID",
                (product_id,),
            ).fetchall()

        return [
            {
                "productID": row["productID"],
                "productName": row["productName"],
                "productPrice": row["productPrice"],
            }
            for row in rows
        ]

    def count_products(self) -> int:
        row = self.conn.execute("SELECT COUNT(*) AS cnt FROM Products").fetchone()
        return int(row["cnt"])

    def create_sample_data(self, count: int = 1000) -> None:
        if self.count_products() >= count:
            return

        for i in range(1, count + 1):
            product_name = f"Product {i:04d}"
            product_price = 10000 + (i % 100) * 100
            self.insert_product(product_name, product_price)

    def close(self) -> None:
        self.conn.close()


if __name__ == "__main__":
    manager = ProductManager()
    manager.create_sample_data(1000)

    products = manager.select_products()
    print(f"DB 경로: {manager.db_path}")
    print(f"총 제품 수: {len(products)}")
    print("첫 5개 제품:")
    for product in products[:5]:
        print(product)

    manager.close()
