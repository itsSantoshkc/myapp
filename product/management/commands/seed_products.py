import uuid
import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from product.models import Product, ProductImage, ProductVariant, Category

class Command(BaseCommand):
    help = 'Seed 100 products with variants, images, and specs'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')
        self.create_categories()
        self.create_products()
        self.stdout.write(self.style.SUCCESS('Done. 100 products seeded.'))

    def create_categories(self):
        structure = {
            'Electronics': ['CPUs', 'GPUs', 'Motherboards', 'RAM', 'Storage'],
            'Cooling': ['Air Coolers', 'Liquid Coolers', 'Case Fans'],
            'Peripherals': ['Keyboards', 'Mice', 'Monitors', 'Headsets'],
            'Cases & Power': ['PC Cases', 'Power Supplies'],
            'Networking': ['Routers', 'Network Cards', 'Switches'],
        }

        self.categories = {}
        for parent_name, children in structure.items():
            parent, _ = Category.objects.get_or_create(
                name=parent_name,
                defaults={'slug': slugify(parent_name)}
            )
            for child_name in children:
                child, _ = Category.objects.get_or_create(
                    name=child_name,
                    defaults={'slug': slugify(child_name), 'parent': parent}
                )
                self.categories[child_name] = child

    def create_products(self):
        products_data = [
            # CPUs
            {'name': 'AMD Ryzen 9 7950X', 'category': 'CPUs', 'price': 699.99, 'desc': '16-core, 32-thread desktop processor with 5.7GHz boost clock.'},
            {'name': 'AMD Ryzen 9 7900X', 'category': 'CPUs', 'price': 449.99, 'desc': '12-core, 24-thread processor with PCIe 5.0 support.'},
            {'name': 'AMD Ryzen 7 7700X', 'category': 'CPUs', 'price': 349.99, 'desc': '8-core Zen 4 processor with 105W TDP.'},
            {'name': 'AMD Ryzen 5 7600X', 'category': 'CPUs', 'price': 249.99, 'desc': '6-core budget champion with 5.3GHz boost.'},
            {'name': 'Intel Core i9-14900K', 'category': 'CPUs', 'price': 589.99, 'desc': '24-core hybrid architecture with 6GHz boost.'},
            {'name': 'Intel Core i7-14700K', 'category': 'CPUs', 'price': 409.99, 'desc': '20-core processor with unlocked multiplier.'},
            {'name': 'Intel Core i5-14600K', 'category': 'CPUs', 'price': 299.99, 'desc': '14-core mid-range powerhouse.'},
            {'name': 'Intel Core i5-13400F', 'category': 'CPUs', 'price': 179.99, 'desc': '10-core budget processor without integrated graphics.'},
            {'name': 'AMD Ryzen 5 5600X', 'category': 'CPUs', 'price': 149.99, 'desc': 'Previous gen 6-core value king.'},
            {'name': 'AMD Threadripper 7960X', 'category': 'CPUs', 'price': 1399.99, 'desc': '24-core HEDT processor for workstations.'},

            # GPUs
            {'name': 'NVIDIA RTX 4090', 'category': 'GPUs', 'price': 1599.99, 'desc': 'Flagship Ada Lovelace GPU with 24GB GDDR6X.'},
            {'name': 'NVIDIA RTX 4080 Super', 'category': 'GPUs', 'price': 999.99, 'desc': '16GB GDDR6X with DLSS 3.5 support.'},
            {'name': 'NVIDIA RTX 4070 Ti Super', 'category': 'GPUs', 'price': 799.99, 'desc': '16GB GDDR6X, excellent 4K performance.'},
            {'name': 'NVIDIA RTX 4070 Super', 'category': 'GPUs', 'price': 599.99, 'desc': '12GB GDDR6X for high refresh 1440p gaming.'},
            {'name': 'NVIDIA RTX 4060 Ti', 'category': 'GPUs', 'price': 399.99, 'desc': '8GB GDDR6 mainstream Ada GPU.'},
            {'name': 'AMD RX 7900 XTX', 'category': 'GPUs', 'price': 949.99, 'desc': '24GB GDDR6 RDNA 3 flagship.'},
            {'name': 'AMD RX 7900 XT', 'category': 'GPUs', 'price': 749.99, 'desc': '20GB RDNA 3 with AV1 encode.'},
            {'name': 'AMD RX 7800 XT', 'category': 'GPUs', 'price': 499.99, 'desc': '16GB RDNA 3 for 1440p gaming.'},
            {'name': 'AMD RX 7600', 'category': 'GPUs', 'price': 269.99, 'desc': '8GB budget RDNA 3 card.'},
            {'name': 'Intel Arc A770', 'category': 'GPUs', 'price': 329.99, 'desc': '16GB GDDR6 with XeSS upscaling.'},

            # Motherboards
            {'name': 'ASUS ROG Maximus Z790 Hero', 'category': 'Motherboards', 'price': 629.99, 'desc': 'Premium Z790 ATX board with DDR5 and PCIe 5.0.'},
            {'name': 'MSI MEG Z790 ACE', 'category': 'Motherboards', 'price': 549.99, 'desc': 'High-end Z790 with 10Gbps LAN.'},
            {'name': 'Gigabyte Z790 Aorus Master', 'category': 'Motherboards', 'price': 499.99, 'desc': 'ATX Z790 with 20+1 power phases.'},
            {'name': 'ASUS TUF Gaming X670E-Plus', 'category': 'Motherboards', 'price': 249.99, 'desc': 'AMD X670E mid-range with PCIe 5.0.'},
            {'name': 'MSI MAG B650 Tomahawk', 'category': 'Motherboards', 'price': 189.99, 'desc': 'B650 ATX board with Wi-Fi 6E.'},
            {'name': 'ASRock B760M Pro RS', 'category': 'Motherboards', 'price': 129.99, 'desc': 'Budget mATX Intel B760 board.'},
            {'name': 'Gigabyte B550 Aorus Pro', 'category': 'Motherboards', 'price': 159.99, 'desc': 'AMD B550 ATX with dual M.2.'},
            {'name': 'ASUS Prime X670-P', 'category': 'Motherboards', 'price': 219.99, 'desc': 'Entry X670 for AM5 platform.'},
            {'name': 'MSI Pro Z790-A Max', 'category': 'Motherboards', 'price': 299.99, 'desc': 'Z790 with Wi-Fi 7 support.'},
            {'name': 'ASRock X670E Taichi', 'category': 'Motherboards', 'price': 449.99, 'desc': 'Flagship X670E with 10Gbps dual LAN.'},

            # RAM
            {'name': 'Corsair Dominator Titanium 64GB DDR5', 'category': 'RAM', 'price': 249.99, 'desc': 'DDR5-6000 CL30 dual channel kit.'},
            {'name': 'G.Skill Trident Z5 RGB 32GB DDR5', 'category': 'RAM', 'price': 139.99, 'desc': 'DDR5-6400 high performance kit.'},
            {'name': 'Kingston Fury Beast 32GB DDR5', 'category': 'RAM', 'price': 109.99, 'desc': 'DDR5-5200 value DDR5 kit.'},
            {'name': 'Corsair Vengeance 32GB DDR4', 'category': 'RAM', 'price': 69.99, 'desc': 'DDR4-3200 CL16 reliable kit.'},
            {'name': 'G.Skill Ripjaws V 16GB DDR4', 'category': 'RAM', 'price': 44.99, 'desc': 'DDR4-3600 budget kit.'},
            {'name': 'TeamGroup T-Force Delta 64GB DDR5', 'category': 'RAM', 'price': 189.99, 'desc': 'DDR5-6000 RGB kit with EXPO support.'},
            {'name': 'Crucial Pro 96GB DDR5', 'category': 'RAM', 'price': 299.99, 'desc': 'DDR5-5600 high capacity kit.'},
            {'name': 'Kingston Fury Renegade 32GB DDR5', 'category': 'RAM', 'price': 149.99, 'desc': 'DDR5-6400 CL32 performance kit.'},
            {'name': 'Patriot Viper Steel 16GB DDR4', 'category': 'RAM', 'price': 39.99, 'desc': 'DDR4-3200 budget DDR4.'},
            {'name': 'Corsair Dominator Platinum 32GB DDR4', 'category': 'RAM', 'price': 89.99, 'desc': 'DDR4-3600 premium RGB kit.'},

            # Storage
            {'name': 'Samsung 990 Pro 2TB NVMe', 'category': 'Storage', 'price': 169.99, 'desc': 'PCIe 4.0 NVMe with 7450MB/s read.'},
            {'name': 'WD Black SN850X 2TB', 'category': 'Storage', 'price': 149.99, 'desc': 'PCIe 4.0 NVMe optimized for gaming.'},
            {'name': 'Seagate FireCuda 530 2TB', 'category': 'Storage', 'price': 159.99, 'desc': 'PCIe 4.0 with 7300MB/s read speed.'},
            {'name': 'Crucial T700 2TB PCIe 5.0', 'category': 'Storage', 'price': 249.99, 'desc': 'First gen PCIe 5.0 NVMe, 12400MB/s read.'},
            {'name': 'Samsung 870 EVO 4TB SATA', 'category': 'Storage', 'price': 299.99, 'desc': 'High capacity SATA SSD for mass storage.'},
            {'name': 'Seagate Barracuda 8TB HDD', 'category': 'Storage', 'price': 139.99, 'desc': '7200RPM hard drive for bulk storage.'},
            {'name': 'WD Red Pro 12TB NAS HDD', 'category': 'Storage', 'price': 259.99, 'desc': 'NAS-optimized hard drive with 3D Active Balance.'},
            {'name': 'Kingston NV3 1TB NVMe', 'category': 'Storage', 'price': 59.99, 'desc': 'Budget PCIe 4.0 NVMe for everyday use.'},
            {'name': 'Sabrent Rocket 4 Plus 4TB', 'category': 'Storage', 'price': 399.99, 'desc': 'High capacity PCIe 4.0 NVMe.'},
            {'name': 'Corsair MP600 Pro LPX 2TB', 'category': 'Storage', 'price': 179.99, 'desc': 'Low profile PCIe 4.0 for PS5 and laptops.'},

            # Air Coolers
            {'name': 'Noctua NH-D15', 'category': 'Air Coolers', 'price': 99.99, 'desc': 'Dual tower flagship with two NF-A15 fans.'},
            {'name': 'be quiet! Dark Rock Pro 4', 'category': 'Air Coolers', 'price': 89.99, 'desc': 'Silent dual tower with 250W TDP rating.'},
            {'name': 'Thermalright Peerless Assassin 120', 'category': 'Air Coolers', 'price': 39.99, 'desc': 'Budget dual tower that rivals premium coolers.'},
            {'name': 'DeepCool AK620', 'category': 'Air Coolers', 'price': 49.99, 'desc': 'Dual tower with 6 heatpipes and 260W TDP.'},
            {'name': 'Scythe Fuma 3', 'category': 'Air Coolers', 'price': 54.99, 'desc': 'Asymmetric dual tower for RAM clearance.'},

            # Liquid Coolers
            {'name': 'ARCTIC Liquid Freezer III 360', 'category': 'Liquid Coolers', 'price': 99.99, 'desc': '360mm AIO with pump integrated into cold plate.'},
            {'name': 'Corsair iCUE H150i Elite Capellix', 'category': 'Liquid Coolers', 'price': 179.99, 'desc': '360mm AIO with RGB pump head.'},
            {'name': 'NZXT Kraken Elite 360', 'category': 'Liquid Coolers', 'price': 249.99, 'desc': '360mm AIO with LCD display on pump head.'},
            {'name': 'be quiet! Pure Loop 2 FX 240', 'category': 'Liquid Coolers', 'price': 119.99, 'desc': '240mm AIO with ARGB fans.'},
            {'name': 'Lian Li Galahad II 360', 'category': 'Liquid Coolers', 'price': 159.99, 'desc': '360mm AIO with Infinity Mirror pump.'},

            # Case Fans
            {'name': 'Noctua NF-A12x25 PWM', 'category': 'Case Fans', 'price': 29.99, 'desc': 'Premium 120mm fan with AAO frame.'},
            {'name': 'be quiet! Silent Wings 4 140mm', 'category': 'Case Fans', 'price': 24.99, 'desc': 'Ultra-silent 140mm PWM fan.'},
            {'name': 'Corsair LL120 RGB 3-Pack', 'category': 'Case Fans', 'price': 69.99, 'desc': '120mm fans with dual light loop RGB.'},
            {'name': 'Lian Li UNI Fan SL-Infinity 120', 'category': 'Case Fans', 'price': 34.99, 'desc': '120mm ARGB fan with daisy-chain connector.'},
            {'name': 'Arctic P14 PWM PST 5-Pack', 'category': 'Case Fans', 'price': 39.99, 'desc': 'Value 140mm fans with PST hub sharing.'},

            # Keyboards
            {'name': 'Keychron Q1 Pro', 'category': 'Keyboards', 'price': 199.99, 'desc': 'Wireless 75% aluminum keyboard with Gateron G Pro switches.'},
            {'name': 'Logitech MX Mechanical', 'category': 'Keyboards', 'price': 169.99, 'desc': 'Wireless full-size with Tactile Quiet switches.'},
            {'name': 'Ducky One 3 SF', 'category': 'Keyboards', 'price': 109.99, 'desc': '65% hot-swap keyboard with Cherry MX switches.'},
            {'name': 'ASUS ROG Strix Scope II', 'category': 'Keyboards', 'price': 139.99, 'desc': 'Full-size gaming keyboard with ROG NX switches.'},
            {'name': 'Corsair K100 RGB', 'category': 'Keyboards', 'price': 229.99, 'desc': 'Full-size with OPX optical-mechanical switches.'},

            # Mice
            {'name': 'Logitech G Pro X Superlight 2', 'category': 'Mice', 'price': 159.99, 'desc': 'Ultra-light wireless mouse at 60g with HERO 25K sensor.'},
            {'name': 'Razer DeathAdder V3 Pro', 'category': 'Mice', 'price': 149.99, 'desc': 'Ergonomic wireless with Focus Pro 30K sensor.'},
            {'name': 'Zowie EC2-C', 'category': 'Mice', 'price': 69.99, 'desc': 'Wired ergonomic esports mouse, plug and play.'},
            {'name': 'Pulsar X2V2', 'category': 'Mice', 'price': 79.99, 'desc': 'Symmetrical ultra-light at 55g.'},
            {'name': 'SteelSeries Aerox 5 Wireless', 'category': 'Mice', 'price': 139.99, 'desc': '9-button wireless mouse with TrueMove Air sensor.'},

            # Monitors
            {'name': 'LG 27GP850-B', 'category': 'Monitors', 'price': 349.99, 'desc': '27" 1440p 165Hz Nano IPS gaming monitor.'},
            {'name': 'Samsung Odyssey G7 32"', 'category': 'Monitors', 'price': 499.99, 'desc': '32" 1440p 240Hz curved VA panel.'},
            {'name': 'ASUS ROG Swift PG279QM', 'category': 'Monitors', 'price': 699.99, 'desc': '27" 1440p 240Hz Fast IPS with G-Sync.'},
            {'name': 'Dell Alienware AW3423DWF', 'category': 'Monitors', 'price': 899.99, 'desc': '34" QD-OLED ultrawide 165Hz.'},
            {'name': 'BenQ MOBIUZ EX2710Q', 'category': 'Monitors', 'price': 379.99, 'desc': '27" 1440p 165Hz IPS with HDRi.'},

            # Headsets
            {'name': 'SteelSeries Arctis Nova Pro Wireless', 'category': 'Headsets', 'price': 349.99, 'desc': 'Premium wireless with ANC and dual battery system.'},
            {'name': 'HyperX Cloud Alpha Wireless', 'category': 'Headsets', 'price': 199.99, 'desc': '300hr battery wireless headset.'},
            {'name': 'Logitech G Pro X 2 Lightspeed', 'category': 'Headsets', 'price': 249.99, 'desc': 'Wireless esports headset with Blue VO!CE mic.'},
            {'name': 'Razer BlackShark V2 Pro', 'category': 'Headsets', 'price': 179.99, 'desc': 'Wireless with THX Spatial Audio.'},
            {'name': 'Corsair Virtuoso RGB Wireless XT', 'category': 'Headsets', 'price': 219.99, 'desc': 'Hi-Fi wireless headset with Bluetooth.'},

            # PC Cases
            {'name': 'Lian Li PC-O11 Dynamic EVO', 'category': 'PC Cases', 'price': 149.99, 'desc': 'Dual chamber ATX case with extensive water cooling support.'},
            {'name': 'Fractal Design Torrent', 'category': 'PC Cases', 'price': 189.99, 'desc': 'High airflow ATX with massive front intake.'},
            {'name': 'NZXT H9 Flow', 'category': 'PC Cases', 'price': 169.99, 'desc': 'Dual chamber mid-tower with panoramic view.'},
            {'name': 'Corsair 5000D Airflow', 'category': 'PC Cases', 'price': 174.99, 'desc': 'ATX mid-tower optimized for airflow.'},
            {'name': 'be quiet! Silent Base 802', 'category': 'PC Cases', 'price': 159.99, 'desc': 'Full tower with sound dampening panels.'},

            # Power Supplies
            {'name': 'Seasonic Prime TX-1000', 'category': 'Power Supplies', 'price': 249.99, 'desc': '1000W 80+ Titanium fully modular PSU.'},
            {'name': 'Corsair RM1000x Shift', 'category': 'Power Supplies', 'price': 199.99, 'desc': '1000W 80+ Gold with side-mounted connectors.'},
            {'name': 'be quiet! Dark Power 13 850W', 'category': 'Power Supplies', 'price': 189.99, 'desc': '850W 80+ Titanium with ATX 3.0.'},
            {'name': 'EVGA SuperNOVA 850 G7', 'category': 'Power Supplies', 'price': 149.99, 'desc': '850W 80+ Gold slim form factor.'},
            {'name': 'Fractal Design Ion+ 3 760W', 'category': 'Power Supplies', 'price': 129.99, 'desc': '760W 80+ Platinum with ATX 3.0 support.'},
        ]

        variant_templates = {
            'CPUs': [
                {'type': 'socket', 'values': ['AM5', 'LGA1700'], 'stocks': [15, 20]},
                {'type': 'tdp', 'values': ['65W', '105W', '125W', '170W'], 'stocks': [10, 12, 8, 5]},
            ],
            'GPUs': [
                {'type': 'memory', 'values': ['8GB', '12GB', '16GB', '24GB'], 'stocks': [8, 12, 10, 6]},
                {'type': 'variant', 'values': ['Founders Edition', 'OC Edition', 'Triple Fan'], 'stocks': [5, 10, 8]},
            ],
            'Motherboards': [
                {'type': 'form factor', 'values': ['ATX', 'mATX', 'ITX'], 'stocks': [15, 10, 8]},
            ],
            'RAM': [
                {'type': 'capacity', 'values': ['16GB', '32GB', '64GB'], 'stocks': [20, 15, 10]},
                {'type': 'color', 'values': ['#C0C0C0', '#000000', '#FF0000'], 'stocks': [15, 12, 8]},
            ],
            'Storage': [
                {'type': 'capacity', 'values': ['500GB', '1TB', '2TB', '4TB'], 'stocks': [20, 18, 12, 8]},
            ],
            'Air Coolers': [
                {'type': 'color', 'values': ['#C0C0C0', '#000000'], 'stocks': [15, 12]},
                {'type': 'fan size', 'values': ['120mm', '140mm'], 'stocks': [20, 15]},
            ],
            'Liquid Coolers': [
                {'type': 'size', 'values': ['240mm', '280mm', '360mm'], 'stocks': [10, 8, 12]},
                {'type': 'color', 'values': ['#000000', '#FFFFFF'], 'stocks': [15, 10]},
            ],
            'Case Fans': [
                {'type': 'size', 'values': ['120mm', '140mm'], 'stocks': [30, 25]},
                {'type': 'color', 'values': ['#000000', '#FFFFFF', '#FF0000'], 'stocks': [20, 15, 10]},
            ],
            'Keyboards': [
                {'type': 'layout', 'values': ['US', 'UK', 'ISO'], 'stocks': [15, 10, 8]},
                {'type': 'switch', 'values': ['Red', 'Blue', 'Brown', 'Silent Red'], 'stocks': [12, 10, 14, 8]},
            ],
            'Mice': [
                {'type': 'color', 'values': ['#000000', '#FFFFFF'], 'stocks': [20, 15]},
                {'type': 'connectivity', 'values': ['Wired', 'Wireless'], 'stocks': [15, 12]},
            ],
            'Monitors': [
                {'type': 'resolution', 'values': ['1080p', '1440p', '4K'], 'stocks': [10, 12, 8]},
                {'type': 'panel', 'values': ['IPS', 'VA', 'OLED'], 'stocks': [12, 10, 6]},
            ],
            'Headsets': [
                {'type': 'color', 'values': ['#000000', '#FFFFFF'], 'stocks': [15, 10]},
                {'type': 'connectivity', 'values': ['Wired', 'Wireless', 'Bluetooth'], 'stocks': [12, 10, 8]},
            ],
            'PC Cases': [
                {'type': 'color', 'values': ['#000000', '#FFFFFF'], 'stocks': [15, 10]},
                {'type': 'form factor', 'values': ['Mid Tower', 'Full Tower'], 'stocks': [12, 8]},
            ],
            'Power Supplies': [
                {'type': 'wattage', 'values': ['650W', '750W', '850W', '1000W'], 'stocks': [12, 15, 10, 8]},
                {'type': 'modular', 'values': ['Fully Modular', 'Semi Modular', 'Non Modular'], 'stocks': [10, 12, 8]},
            ],
        }

        spec_templates = {
            'CPUs': {'cores': ['6', '8', '12', '16', '24'], 'threads': ['12', '16', '24', '32', '48'], 'boost_clock': ['4.5GHz', '5.0GHz', '5.5GHz', '5.7GHz', '6.0GHz'], 'cache': ['32MB', '64MB', '96MB', '128MB']},
            'GPUs': {'vram': ['8GB', '12GB', '16GB', '24GB'], 'bus': ['128-bit', '192-bit', '256-bit', '384-bit'], 'tdp': ['115W', '200W', '285W', '350W', '450W'], 'outputs': ['3x DP 1.4, 1x HDMI 2.1']},
            'Motherboards': {'socket': ['AM5', 'LGA1700'], 'chipset': ['B650', 'X670E', 'Z790', 'B760'], 'memory_slots': ['2', '4'], 'max_memory': ['64GB', '128GB', '192GB']},
            'RAM': {'speed': ['DDR4-3200', 'DDR4-3600', 'DDR5-5200', 'DDR5-6000', 'DDR5-6400'], 'cas_latency': ['CL16', 'CL30', 'CL32', 'CL36'], 'voltage': ['1.1V', '1.25V', '1.35V', '1.4V']},
            'Storage': {'interface': ['PCIe 3.0', 'PCIe 4.0', 'PCIe 5.0', 'SATA III'], 'read_speed': ['550MB/s', '3500MB/s', '7000MB/s', '12400MB/s'], 'write_speed': ['520MB/s', '3000MB/s', '6500MB/s', '11800MB/s'], 'form_factor': ['2.5"', 'M.2 2280']},
            'Air Coolers': {'tdp_rating': ['150W', '200W', '250W', '280W'], 'height': ['155mm', '158mm', '160mm', '168mm'], 'heatpipes': ['4', '5', '6'], 'fans_included': ['1', '2']},
            'Liquid Coolers': {'radiator': ['240mm', '280mm', '360mm'], 'pump_speed': ['800-2800RPM', '800-3300RPM'], 'fan_speed': ['500-2000RPM', '400-1800RPM'], 'tubing': ['300mm', '350mm', '400mm']},
            'Case Fans': {'size': ['120mm', '140mm'], 'max_rpm': ['1200RPM', '1500RPM', '2000RPM', '2500RPM'], 'airflow': ['51.3CFM', '67.8CFM', '84.5CFM'], 'noise': ['17.8dB', '22.4dB', '28.5dB']},
            'Keyboards': {'keys': ['65', '75', '80', '100'], 'backlight': ['RGB', 'Single Color', 'None'], 'polling_rate': ['125Hz', '500Hz', '1000Hz', '8000Hz'], 'actuation': ['1.2mm', '1.5mm', '2.0mm']},
            'Mice': {'sensor': ['PMW3395', 'HERO 25K', 'Focus Pro 30K', 'TrueMove Air'], 'dpi': ['100-26000', '100-25600', '100-30000'], 'weight': ['55g', '60g', '70g', '85g', '95g'], 'buttons': ['5', '6', '9', '11']},
            'Monitors': {'size': ['24"', '27"', '32"', '34"'], 'refresh_rate': ['144Hz', '165Hz', '240Hz', '360Hz'], 'response_time': ['0.5ms', '1ms', '4ms'], 'hdr': ['HDR400', 'HDR600', 'HDR1000', 'True Black 400']},
            'Headsets': {'driver': ['40mm', '50mm'], 'frequency': ['20Hz-20kHz', '10Hz-40kHz'], 'impedance': ['32Ω', '64Ω'], 'mic_pattern': ['Cardioid', 'Bidirectional', 'Noise Cancelling']},
            'PC Cases': {'material': ['Steel', 'Aluminum', 'Tempered Glass'], 'dimensions': ['480x230x490mm', '520x240x510mm', '550x260x560mm'], 'drive_bays': ['2x 3.5", 2x 2.5"', '4x 3.5", 4x 2.5"'], 'max_gpu_length': ['360mm', '380mm', '420mm']},
            'Power Supplies': {'efficiency': ['80+ Bronze', '80+ Gold', '80+ Platinum', '80+ Titanium'], 'certification': ['ATX 2.0', 'ATX 3.0'], 'fan_size': ['120mm', '135mm', '140mm'], 'protections': ['OVP, UVP, OCP, SCP, OTP, OPP']},
        }

        image_urls = [
            'https://placehold.co/800x600/1a1a2e/ffffff?text=Product+Image',
            'https://placehold.co/800x600/16213e/ffffff?text=Product+Side',
            'https://placehold.co/800x600/0f3460/ffffff?text=Product+Detail',
            'https://placehold.co/800x600/533483/ffffff?text=Product+Box',
        ]

        for i, p in enumerate(products_data):
            slug = slugify(p['name'])
            # ensure unique slug
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

            # images
            for j, url in enumerate(image_urls):
                ProductImage.objects.create(
                    product=product,
                    url=url,
                    is_primary=(j == 0),
                    sort_order=j,
                )

            # variants
            cat_name = p['category']
            templates = variant_templates.get(cat_name, [])
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


            self.stdout.write(f'  [{i+1}/100] Created: {product.name}')