import os

# List all your JSON files here
files = ["account.json", "product.json", "orders.json", "cart.json", "wishlist.json"]

for file_name in files:
    if os.path.exists(file_name):
        with open(file_name, "rb") as f:
            content = f.read()

        # Decode with 'utf-8-sig' to remove BOM if exists
        text = content.decode("utf-8-sig")

        # Save back as proper UTF-8
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"Fixed encoding: {file_name}")
    else:
        print(f"File not found: {file_name}")
