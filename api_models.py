from typing import List,Optional

from pydantic import BaseModel


class FinalPrice(BaseModel):
    value: float

class MinimumPrice(BaseModel):
    final_price: FinalPrice

class PriceRange(BaseModel):
    minimum_price: MinimumPrice

class NutritionDetail(BaseModel):
    nutritional_item: Optional[str] = "N/A"
    amount: Optional[str] = "N/A"
    percent_dv: Optional[str] = "N/A"

class Nutrition(BaseModel):
    serving_size: Optional[str] = "N/A"
    calories_per_serving: Optional[str] = "N/A"
    servings_per_container: Optional[str] = "N/A"
    details: Optional[List[NutritionDetail]]

class Product(BaseModel):
    name: str
    retail_price: float=0
    nutrition: Optional[List[Nutrition]]

class PageInfo(BaseModel):
    current_page: int
    page_size: int
    total_pages: int

class Products(BaseModel):
    items: List[Product]
    total_count: int
    page_info: PageInfo

class Data(BaseModel):
    products: Products

class ApiResponse(BaseModel):
    data: Data
