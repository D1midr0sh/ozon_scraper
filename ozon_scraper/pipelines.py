import pandas as pd


class OzonScraperPipeline:
    all_items = []

    def process_item(self, item, spider):
        self.all_items.append(item)
        return item

    def close_spider(self, spider):
        df = pd.DataFrame(self.all_items)
        with open("data.csv", "w") as f:
            df.value_counts().to_csv(f)

        print(df.value_counts())