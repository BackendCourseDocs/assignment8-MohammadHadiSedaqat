from locust import HttpUser, task, between
import random

SEARCH_TERMS = [
    "python", "data", "science", "machine", "history",
    "math", "biology", "network", "deep", "learning",
    "clean", "architecture", "design", "api", "cloud"
]

AUTHOR_TERMS = [
    "Mark", "John", "David", "Michael", "Sara",
    "Emily", "Robert", "James", "Ali", "Hadi"
]

class WebUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.book_id = None
        self.create_new_book()

    def create_new_book(self):
        response = self.client.post(
            "/books",
            data={
                "title": f"Book {random.randint(1, 20050)}",
                "author": random.choice(AUTHOR_TERMS),
                "publisher": f"Publisher {random.randint(1, 100)}",
                "first_publish_year": str(random.randint(1950, 2026)),
            }
        )

        if response.status_code in (200, 201):
            self.book_id = response.json()["id"]
        else:
            print(response.text)
            self.book_id = None


    @task(1)
    def add_book(self):
        self.create_new_book()


    @task(4)
    def search_books(self):
        self.client.get("/books", params={
            "q": random.choice(SEARCH_TERMS)
        })


    @task(3)
    def search_authors(self):
        self.client.get("/authors", params={
            "q": random.choice(AUTHOR_TERMS)
        })


    @task(1)
    def update_book(self):
        if self.book_id:
            self.client.put(
                f"/books/{self.book_id}",
                json={
                    "title": f"Updated {random.randint(1,10000)}",
                    "author": random.choice(AUTHOR_TERMS),
                    "publisher": "Updated Publisher",
                    "first_publish_year": random.randint(1950, 2026),
                    "image_url": None
                },
            )


    @task(2)
    def delete_book(self):
        if self.book_id:
            self.client.delete(f"/books/{self.book_id}")
            self.create_new_book()