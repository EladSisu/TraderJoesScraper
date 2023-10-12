import asyncio
import csv
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

import aiohttp

from api_models import ApiResponse, Data, Product

TJ_URL = 'https://www.traderjoes.com/api/graphql'
# Hard coded values for nutritional values are taken from the api schema. 
CSV_HEADER = ['Name', 'Price', 'Calories', 'Total Fat', 'Saturated Fat', 'Trans Fat', 'Cholesterol', 'Sodium', 'Total Carbohydrate', 'Dietary Fiber', 'Total Sugars', 'Protein', 'Vitamin D', 'Calcium', 'Iron', 'Potassium']
async def fetch(session,body):
        async with session.post(TJ_URL,json=body) as resp:
            return await resp.json()

class Scrapper:
  def __init__(self,session) -> None:
    self.session = session

  def get_req_body(self,pg_number:int,pg_size:int=200) ->Dict[Any,Any]:
    # Hard coded request to TJ graphql api to fetch product data.
    return {
  "operationName": "SearchProducts",
  "variables": {
    "storeCode": "TJ",
    "availability": "1",
    "published": "1",
    "categoryId": 2,
    "currentPage": pg_number,
    "pageSize": pg_size
  },
 "query": "query SearchProduct($sku: String, $storeCode: String = \"TJ\", $published: String = \"1\", $currentPage: Int, $pageSize: Int) { products(filter: {sku: {eq: $sku}, store_code: {eq: $storeCode}, published: {eq: $published}}, currentPage: $currentPage, pageSize: $pageSize) { items { name retail_price nutrition { display_sequence panel_id panel_title serving_size calories_per_serving servings_per_container details { display_seq nutritional_item amount percent_dv } } } total_count page_info { current_page page_size total_pages } } }"
}

  async def fetch_page_data(self,pg_number)->Data:
    json_data = await fetch(self.session,self.get_req_body(pg_number))
    return ApiResponse.model_validate(json_data).data
    
  async def get_all_data(self) -> List[Product]:
    first_pg = await self.fetch_page_data(0)
    if first_pg.products.page_info.total_pages == 1 :
       return first_pg.products.items
    items = first_pg.products.items
    tasks = []
    # fetch all other pages in parallel.
    for i in range(2,first_pg.products.page_info.total_pages+1):
      tasks.append(self.fetch_page_data(i))
    data = await asyncio.gather(*tasks)
    for pg_data in data:
       items.extend(pg_data.products.items)
    return items
       

@dataclass 
class CsvWriter:
  items: List[Product]

  def __call__(self):
    # create a csv file represents a weatherdata
    data = [self.get_item_row_values(item) for item in self.items]
    current_date = datetime.today().strftime('%Y-%m-%d')
    file_name = f"tj_products_{current_date}.csv"
    with open(file_name,'w',newline='') as csvfile:
        spamwriter = csv.writer(csvfile,delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(CSV_HEADER)
        for d in data:
            spamwriter.writerow(d)

  def get_item_nutrition_mapping(self,item:Product):
       if item.nutrition and item.nutrition[0].details:
          return {d.nutritional_item:d.amount for d in  item.nutrition[0].details}
       return {}
  
  def get_item_row_values(self,item:Product):
       # returns array with all req CSV_HEADER values:
       #['Name', 'Price', 'Calories', 'Total Fat', 'Saturated Fat', 'Trans Fat', 'Cholesterol', 'Sodium', 'Total Carbohydrate', 'Dietary Fiber', 'Total Sugars', 'Protein', 'Vitamin D', 'Calcium', 'Iron', 'Potassium']
       nutrition_values = self.get_item_nutrition_mapping(item)
       calories = item.nutrition[0].calories_per_serving if item.nutrition else -1
       values = [item.name,item.retail_price,calories]
       for i in CSV_HEADER[3:]:
          values.append(nutrition_values.get(i,"N/A"))
       return values
    
async def main():
   async with aiohttp.ClientSession() as session:
    data = await Scrapper(session).get_all_data()
    CsvWriter(data)()


if __name__ == "__main__":
    asyncio.run(main())