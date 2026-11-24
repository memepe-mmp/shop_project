from locust import HttpUser, between, task


class CatalogUser(HttpUser):
    wait_time = between(0.5, 1.5)

    @task(3)
    def list_products(self):
        self.client.get("/")

    @task(1)
    def filter_category_and_price(self):
        self.client.get("/?category=1&status=in_stock&min_price=1000&sort=newest", name="/?filters")

    @task(1)
    def search_product(self):
        self.client.get("/?q=товар", name="/?q")