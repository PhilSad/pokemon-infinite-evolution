import scrapy
import requests

class BulbaSpider(scrapy.Spider):
    name = "bulbapedia"
    start_urls = [
        "https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number",
    ]

    def __init__(self, *args, **kwargs):
        super(BulbaSpider, self).__init__(*args, **kwargs)
        self.domain = "https://bulbapedia.bulbagarden.net"
        # self.download_delay = 1

    def parse(self, response: scrapy.http.Response):

        tables = response.xpath(
            "/html/body/div[1]/div[2]/div[1]/div[3]/div[4]/div[1]/table"
        )[1:-1]

        for table in tables:
            for row in table.xpath(".//tr")[1:]:
                yield response.follow(
                    self.domain + row.xpath(".//a/@href").get(), self.parse_pokemon_page
                )

    def parse_pokemon_page(self, response):
        table = response.xpath(
            "/html/body/div[1]/div[2]/div[1]/div[3]/div[4]/div[1]/table[2]/tbody/tr[1]/td/table/tbody"
        )
        if len(table) == 0:
            table = response.xpath("/html/body/div[1]/div/main/div[3]/div/div[1]/section[1]/table[2]")

        name = table.xpath(".//big//text()")[0].get()
        nat_idx = table.xpath(".//big//text()")[1].get()

        links = table.xpath(".//a/@href").getall()
        image_link = [link for link in links if "File:" in link][0]

        yield response.follow(self.domain + image_link, self.parse_image, cb_kwargs={"name": name, "nat_idx": nat_idx})

    def parse_image(self, response, name, nat_idx):
        full_size_link = response.xpath('//a[text()="Full-size image"]/@href').get()

        if full_size_link is None:
            full_size_link = response.xpath(
                '//div[contains(@class, "fullImageLink")]/a/img/@src'
            ).get()

        # download the image
        with open(f"images/{nat_idx}_{name}.png", "wb") as f:
            f.write(requests.get(full_size_link).content)

        yield {
            "name": name,
            "nat_idx": nat_idx,
            "image_link": full_size_link,
            "image_path": f"images/{nat_idx}_{name}.png",
        }
