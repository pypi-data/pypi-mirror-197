import time

from parsing_steps import SimpleParsingStep


class ParseMainPage(SimpleParsingStep):
    """
    input_data is main page url.
    input_data = "https://domain.com/"
    """

    def download(self, url):
        time.sleep(0.1)
        return '<html>...<a href="https://domain.com/category/15/"></a>...</html>'

    def get_category_urls(self, html_data):
        """Plug"""
        return [f"https://domain/category/{num}/" for num in range(15, 16)]

    def parse(self, input_data):
        url = input_data
        html_data = self.download(url)

        for category_url in self.get_category_urls(html_data):
            yield ParseListStep({"url": category_url})


class ParseListStep(SimpleParsingStep):
    """
    input_data from previous step.
    input_data = {
        "url": "https://domain.com/category/<id>/"
    }
    """

    def download(self, url):
        time.sleep(0.1)
        if "?page=2" in url:
            return "<html>...</html>"
        return '<html>...<a href="https://domain.com/category/15/?page=2"></a>...</html>'

    def get_item_urls(self, html_data):
        """Plug"""
        return [f"https://domain/category/15/item/{num}/" for num in range(10)]

    def exists_next_page(self, html_data):
        return "?page=" in html_data

    def parse(self, input_data):
        print(f"category_url: {input_data.get('url')}")
        #  here you get data from html, through bs4 or something else.
        html_data = self.download(input_data.get("url"))

        for item_url in self.get_item_urls(html_data):
            yield ParseDetailsStep(
                input_data={"url": item_url},
                inherited_data={  # optional part
                    "category_id": 15,
                    "page": 1 if self.exists_next_page(html_data) else 2
                }
            )

        if self.exists_next_page(html_data):
            # get this data from html
            next_page_url = "https://domain.com/category/15/?page=2"
            yield ParseListStep(
                input_data={"url": next_page_url}
            )


class ParseDetailsStep(SimpleParsingStep):
    """
    input_data from previous step.
    input_data = {
        "url": "https://domain/category/15/item/{num}/"
    }
    """

    def download_and_format(self, url):
        """plug"""
        time.sleep(0.2)
        num = int(list(filter(None, str(url).split("/")))[-1])  # returns num
        page = int(self.inherited_data.get("page"))
        return {
            "id": page*10 + int(num),
            "name": f"product_{page*10 + num}",
            "price": num*10,
        }

    def parse(self, input_data):
        product_data = self.download_and_format(input_data.get("url"))
        yield SaveStep(product_data)


class SaveStep(SimpleParsingStep):
    """
    input_data from previous step.
    input_data = {
        "id": 12345,
        "name": "product",
        "price": 16.50,
    }
    """

    def save_to_db(self, data_as_dict):
        self.inherited_data = self.inherited_data or dict()
        data_as_dict.update(self.inherited_data)
        print(data_as_dict)

    def parse(self, input_data):
        self.save_to_db(input_data)


if __name__ == "__main__":
    first_step = ParseMainPage(input_data="https://domain.com/")
    first_step.perform()  # start scraping
