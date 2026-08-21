import uuid
import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from product.models import Product, ProductImage, ProductVariant, Category

WATCH_CATEGORIES = [
    "Men's Watches",
    "Women's Watches",
    "Smart Watches",
    "Luxury Watches",
    "Sports Watches",
]


class Command(BaseCommand):
    help = 'Seed watch products with variants, images, and specs'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding watch catalog...')
        self.create_categories()
        self.create_products()
        self.stdout.write(self.style.SUCCESS('Done. Watch catalog seeded.'))

    def create_categories(self):
        self.categories = {}
        for name in WATCH_CATEGORIES:
            cat, _ = Category.objects.get_or_create(
                name=name,
                defaults={'slug': slugify(name)}
            )
            self.categories[name] = cat

    def create_products(self):
        products_data = [
            # Men's Watches
            {'name': 'Seiko Prospex Diver', 'category': "Men's Watches", 'price': 449.99, 'desc': 'Automatic dive watch with 200m water resistance and Lumibrite markers.'},
            {'name': 'Tissot PRX Powermatic 80', 'category': "Men's Watches", 'price': 329.99, 'desc': 'Integrated-bracelet automatic with an 80-hour power reserve.'},
            {'name': 'Citizen Eco-Drive Promaster', 'category': "Men's Watches", 'price': 279.99, 'desc': 'Solar-powered pilot watch that never needs a battery.'},
            {'name': 'Hamilton Khaki Field', 'category': "Men's Watches", 'price': 359.99, 'desc': 'Rugged military-inspired automatic with a clean dial.'},
            {'name': 'Orient Bambino Version 8', 'category': "Men's Watches", 'price': 159.99, 'desc': 'Affordable automatic dress watch with a domed crystal.'},

            # Women's Watches
            {'name': 'Cartier Ballon Bleu', 'category': "Women's Watches", 'price': 1299.99, 'desc': 'Iconic rounded case with a sapphire cabochon crown.'},
            {'name': 'Michael Kors Parker', 'category': "Women's Watches", 'price': 179.99, 'desc': 'Fashion-forward chronograph with a crystal-set bezel.'},
            {'name': 'Fossil Jacqueline', 'category': "Women's Watches", 'price': 129.99, 'desc': 'Minimalist leather-strap watch with a slim profile.'},
            {'name': 'Casio Sheen', 'category': "Women's Watches", 'price': 89.99, 'desc': 'Sleek stainless-steel watch with a scratch-resistant face.'},
            {'name': 'Omega Constellation', 'category': "Women's Watches", 'price': 1499.99, 'desc': 'Luxury ladies watch with a signature star dial.'},

            # Smart Watches
            {'name': 'Apple Watch Series 9', 'category': 'Smart Watches', 'price': 399.99, 'desc': 'Advanced health sensing with the brilliant Always-On Retina display.'},
            {'name': 'Samsung Galaxy Watch 6', 'category': 'Smart Watches', 'price': 329.99, 'desc': 'Wear OS smartwatch with body composition tracking.'},
            {'name': 'Garmin Fenix 7', 'category': 'Smart Watches', 'price': 699.99, 'desc': 'Multisport GPS watch with solar charging and maps.'},
            {'name': 'Fitbit Sense 2', 'category': 'Smart Watches', 'price': 249.99, 'desc': 'Stress and heart-health tracking with a 6-day battery.'},
            {'name': 'Amazfit GTR 4', 'category': 'Smart Watches', 'price': 199.99, 'desc': 'Stylish AMOLED smartwatch with 14-day battery life.'},

            # Luxury Watches
            {'name': 'Rolex Submariner Date', 'category': 'Luxury Watches', 'price': 9499.99, 'desc': 'Legendary dive watch in 904L steel with a ceramic bezel.'},
            {'name': 'Omega Speedmaster Professional', 'category': 'Luxury Watches', 'price': 6299.99, 'desc': 'The Moonwatch: hand-wound chronograph with a hesalite crystal.'},
            {'name': 'Tag Heuer Carrera', 'category': 'Luxury Watches', 'price': 4299.99, 'desc': 'Motorsport heritage chronograph with a tachymeter scale.'},
            {'name': 'Breitling Navitimer', 'category': 'Luxury Watches', 'price': 7299.99, 'desc': 'Pilot chronograph with the iconic circular slide rule.'},
            {'name': 'Patek Philippe Nautilus', 'category': 'Luxury Watches', 'price': 28999.99, 'desc': 'Grail sports watch with a horizontally embossed dial.'},

            # Sports Watches
            {'name': 'Garmin Forerunner 265', 'category': 'Sports Watches', 'price': 449.99, 'desc': 'AMOLED running watch with full triathlon metrics.'},
            {'name': 'Casio G-Shock Mudmaster', 'category': 'Sports Watches', 'price': 329.99, 'desc': 'Shock-resistant field watch with mud and dust resistance.'},
            {'name': 'Suunto 9 Peak', 'category': 'Sports Watches', 'price': 549.99, 'desc': 'Slim outdoor watch with barometric altitude and navigation.'},
            {'name': 'Polar Vantage V3', 'category': 'Sports Watches', 'price': 599.99, 'desc': 'Recovery-focused multisport watch with AMOLED display.'},
            {'name': 'Coros Apex 2', 'category': 'Sports Watches', 'price': 399.99, 'desc': 'Lightweight adventure watch with dual-frequency GPS.'},
        ]

        variant_templates = {
            "Men's Watches": [
                {'type': 'case size', 'values': ['38mm', '40mm', '42mm', '44mm'], 'stocks': [12, 15, 10, 8]},
                {'type': 'dial color', 'values': ['Black', 'Blue', 'White', 'Green'], 'stocks': [15, 12, 10, 8]},
            ],
            "Women's Watches": [
                {'type': 'case size', 'values': ['28mm', '32mm', '36mm'], 'stocks': [15, 12, 10]},
                {'type': 'dial color', 'values': ['Rose Gold', 'Silver', 'White', 'Black'], 'stocks': [12, 10, 8, 8]},
            ],
            'Smart Watches': [
                {'type': 'case size', 'values': ['41mm', '45mm'], 'stocks': [15, 12]},
                {'type': 'connectivity', 'values': ['GPS', 'GPS + Cellular'], 'stocks': [12, 10]},
            ],
            'Luxury Watches': [
                {'type': 'case size', 'values': ['40mm', '42mm', '44mm'], 'stocks': [8, 6, 5]},
                {'type': 'dial color', 'values': ['Black', 'Blue', 'Silver', 'Champagne'], 'stocks': [8, 6, 5, 4]},
            ],
            'Sports Watches': [
                {'type': 'case size', 'values': ['42mm', '46mm', '50mm'], 'stocks': [12, 10, 8]},
                {'type': 'band', 'values': ['Silicone', 'Rubber', 'Nylon'], 'stocks': [12, 10, 8]},
            ],
        }

        spec_templates = {
            "Men's Watches": {'movement': ['Automatic', 'Quartz', 'Solar'], 'case material': ['Stainless Steel', 'Titanium'], 'water resistance': ['50m', '100m', '200m'], 'strap': ['Leather', 'Stainless Steel', 'Silicone']},
            "Women's Watches": {'movement': ['Quartz', 'Automatic'], 'case material': ['Stainless Steel', 'Rose Gold'], 'water resistance': ['30m', '50m'], 'strap': ['Leather', 'Stainless Steel']},
            'Smart Watches': {'display': ['AMOLED', 'OLED', 'Retina'], 'battery life': ['18 hrs', '36 hrs', '7 days', '14 days'], 'connectivity': ['Bluetooth', 'GPS', 'LTE'], 'sensors': ['Heart Rate', 'SpO2', 'GPS']},
            'Luxury Watches': {'movement': ['Automatic', 'Manual Wind'], 'case material': ['Stainless Steel', '18k Gold', 'Platinum'], 'water resistance': ['50m', '100m', '300m'], 'complication': ['Chronograph', 'Date', 'Moonphase']},
            'Sports Watches': {'display': ['MIP', 'AMOLED'], 'battery life': ['14 days', '21 days', '30 days'], 'gps': ['Multi-band', 'Dual-frequency'], 'durability': ['Shock Resistant', 'Dive Rated', 'MIL-STD-810']},
        }

        for i, p in enumerate(products_data):
            slug = slugify(p['name'])
            if Product.objects.filter(slug=slug).exists():
                slug = f"{slug}-{i}"

            product = Product.objects.create(
                name=p['name'],
                slug=slug,
                category=self.categories.get(p['category']),
                description=p['desc'],
                base_price=p['price'],
                is_active=True,
            )

            # images (deterministic real placeholders)
            for j in range(4):
                ProductImage.objects.create(
                    product=product,
                    url=f"https://picsum.photos/seed/{slug}-{j}/800/800",
                    is_primary=(j == 0),
                    sort_order=j,
                )

            # variants
            templates = variant_templates.get(p['category'], [])
            for template in templates:
                for k, value in enumerate(template['values']):
                    stock = template['stocks'][k] if k < len(template['stocks']) else 10
                    sku = f"{slug}-{slugify(template['type'])}-{slugify(value)}"
                    ProductVariant.objects.get_or_create(
                        sku=sku,
                        defaults={
                            'product': product,
                            'type': template['type'],
                            'value': value,
                            'stock': stock,
                        }
                    )

            # specs
            specs = {}
            for key, values in spec_templates.get(p['category'], {}).items():
                specs[key] = random.choice(values)
            product.specs = specs
            product.save()

            self.stdout.write(f'  [{i+1}/{len(products_data)}] Created: {product.name}')
