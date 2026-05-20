def clean_products(products):

    cleaned = []

    for p in products:

        cleaned.append({

            "product_id":
                int(
                    p["product_id"]
                ),

            "name":
                p["name"],

            "brand":
                p["brand"],

            "price":
                float(
                    p["price"]
                ),

            "inventory":
                int(
                    p["inventory"]
                ),

            "merchant_id":
                int(
                    p["merchant_id"]
                ),

            "rating":
                float(
                    p["rating"] or 0
                ),

            "image_url":
                p["image_url"],

            "in_stock":
                bool(
                    p["in_stock"]
                ),

            "city":
                p["city"],

            "latitude":
                float(
                    p["latitude"]
                ),

            "longitude":
                float(
                    p["longitude"]
                )
        })

    return cleaned