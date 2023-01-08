from apps.core.services.status import *
import asyncio
from apps.core.services.controller import Controller
from apps.dashboard.models import Category
from apps.products.serializers import InternationProduct, InternationProductSerializer


class ProductController(Controller):

    SECRET_KEY = "6042c1lmu72wiltm0li55klis23ky7"  # f24j810db0yfb14n48490l7omhanmc
    UPC_URL = "https://api.barcodelookup.com/v3/products"
    CATEGORY_DELIMITER = ">"

    def get_product_by_upc(self, upc_code) -> InternationProduct:
        url = f"https://api.barcodelookup.com/v3/products?barcode={upc_code}&formatted=y&key={self.SECRET_KEY}"
        request = requests.get(url=url)
        # print("status_code", request.status_code, type(request.status_code))
        if request.status_code == requests.codes.ok:
            data = request.json()['products'][0]
            last_item = self._category_controller(category_path=data['category'])
            data['last_child'] = last_item.strip()
            serializer = InternationProductSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return serializer.instance

    def get_upc_detail(self, upc_code):
        """
        UPC (UNIVERSAL PRODUCT CODE)
        "title": "Apple iPhone 11 Pro",
        "category": "Mobile Phones",
        "brand": "Apple",
        "upc": "190199392526",
        "color": "space gray",
        "memory": "64GB",
        "images": ["https://images.barcodelookup.com/15231/152311689-1.jpg"]
        """
        qs = InternationProduct.objects.filter(barcode_number=upc_code)
        if qs.exists():
            instance = qs.last()
        else:
            instance = self.get_product_by_upc(upc_code=upc_code)

        if instance:
            return instance.to_dict()

    def _category_controller(self, category_path):
        # Electronics > Communications > Telephony > Mobile Phones
        if self.CATEGORY_DELIMITER in category_path:
            categories = category_path.split(self.CATEGORY_DELIMITER)
            parent = None
            for category in categories:
                name = category.strip()
                qs = Category.objects.filter(name__iexact=name)
                if qs.exists():
                    parent = qs.last()
                else:
                    if parent:
                        parent = Category.objects.create(parent_id=parent.id, name=name)
                    else:
                        parent = Category.objects.create(name=name)
            return categories.pop()
        else:
            return category_path

