from dataclasses import dataclass

@dataclass
class ProductModel:
    id: int | None
    model_name: str
    barcode_prefix: str
