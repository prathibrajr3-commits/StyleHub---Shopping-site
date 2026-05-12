from django.core.management.base import BaseCommand
from store.models import Category, Product, BlogPost


PRODUCTS = [
    # Men's Shirts
    {
        "name": "Blue Stripe Oxford Shirt",
        "slug": "blue-stripe-oxford-shirt",
        "category": "shirts", "brand": "StyleHub",
        "gender": "men",
        "description": "A timeless Oxford shirt crafted from 100% premium cotton. Features a classic button-down collar, chest pocket, and a comfortable relaxed fit. Perfect for smart-casual occasions.",
        "price": "1299", "original_price": "1899",
        "image_url": "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?w=600&q=80",
        "stock": 45, "is_featured": True, "is_new_arrival": False, "rating": "4.5", "review_count": 128,
        "sizes": "S,M,L,XL,XXL",
    },
    {
        "name": "Charcoal Slim Fit Shirt",
        "slug": "charcoal-slim-fit-shirt",
        "category": "shirts", "brand": "StyleHub",
        "gender": "men",
        "description": "A refined slim-fit shirt in rich charcoal, made from wrinkle-resistant fabric. Ideal for office wear or evening outings with its subtle texture and clean silhouette.",
        "price": "1099", "original_price": "1599",
        "image_url": "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?w=600&q=80",
        "stock": 30, "is_featured": True, "is_new_arrival": False, "rating": "4.3", "review_count": 86,
        "sizes": "S,M,L,XL,XXL",
    },
    {
        "name": "Classic White Formal Shirt",
        "slug": "classic-white-formal-shirt",
        "category": "shirts", "brand": "StyleHub",
        "gender": "men",
        "description": "The white formal shirt every wardrobe needs. Made from crisp Egyptian cotton with mother-of-pearl buttons and a tailored fit that looks sharp under a blazer or standalone.",
        "price": "999", "original_price": "1499",
        "image_url": "https://images.unsplash.com/photo-1620012253295-c15cc3e65df4?w=600&q=80",
        "stock": 60, "is_featured": True, "is_new_arrival": True, "rating": "4.7", "review_count": 214,
        "sizes": "S,M,L,XL,XXL",
    },
    {
        "name": "Denim Oversized Jacket",
        "slug": "denim-oversized-jacket",
        "category": "shirts", "brand": "StyleHub",
        "gender": "men",
        "description": "An oversized denim jacket with washed finish and raw hem detailing. Features multiple pockets and adjustable cuffs, making it the perfect streetwear layering piece.",
        "price": "2499", "original_price": "3299",
        "image_url": "https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=600&q=80",
        "stock": 22, "is_featured": False, "is_new_arrival": True, "rating": "4.6", "review_count": 73,
        "sizes": "S,M,L,XL,XXL",
    },
    # Women's Shirts
    {
        "name": "Floral Embroidered Blouse",
        "slug": "floral-embroidered-blouse",
        "category": "shirts", "brand": "StyleHub",
        "gender": "women",
        "description": "A delicate blouse with hand-inspired floral embroidery across the front. Made from lightweight chiffon with a relaxed fit, flutter sleeves, and a subtle V-neckline.",
        "price": "1199", "original_price": "1799",
        "image_url": "https://images.unsplash.com/photo-1594938298603-c8148c4b4ad4?w=600&q=80",
        "stock": 40, "is_featured": True, "is_new_arrival": False, "rating": "4.8", "review_count": 162,
        "sizes": "XS,S,M,L,XL",
    },
    {
        "name": "Sage Green Oversized Shirt",
        "slug": "sage-green-oversized-shirt",
        "category": "shirts", "brand": "StyleHub",
        "gender": "women",
        "description": "A relaxed oversized shirt in trending sage green. Made from breathable cotton-linen blend, designed to be worn open over a tee or buttoned up and tucked in.",
        "price": "1399", "original_price": "1899",
        "image_url": "https://images.unsplash.com/photo-1554568218-0f1715e72254?w=600&q=80",
        "stock": 35, "is_featured": True, "is_new_arrival": True, "rating": "4.5", "review_count": 94,
        "sizes": "XS,S,M,L,XL",
    },
    {
        "name": "Printed Tie-Front Top",
        "slug": "printed-tie-front-top",
        "category": "shirts", "brand": "StyleHub",
        "gender": "women",
        "description": "A fun and flattering tie-front top in a bold abstract print. Cropped length pairs perfectly with high-waist bottoms. Soft modal fabric for all-day comfort.",
        "price": "899", "original_price": "1299",
        "image_url": "https://images.unsplash.com/photo-1564584217132-2271feaeb3c5?w=600&q=80",
        "stock": 50, "is_featured": False, "is_new_arrival": True, "rating": "4.4", "review_count": 57,
        "sizes": "XS,S,M,L,XL",
    },
    # Men's Pants
    {
        "name": "Loose Fit Cargo Pants",
        "slug": "loose-fit-cargo-pants",
        "category": "pants", "brand": "StyleHub",
        "gender": "men",
        "description": "Street-ready cargo pants with a roomy silhouette and six functional pockets. Made from durable ripstop cotton, with adjustable drawstring waist and tapered ankle.",
        "price": "1799", "original_price": "2499",
        "image_url": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=600&q=80",
        "stock": 38, "is_featured": True, "is_new_arrival": False, "rating": "4.6", "review_count": 110,
        "sizes": "28,30,32,34,36",
    },
    {
        "name": "Slim Tapered Jogger",
        "slug": "slim-tapered-jogger",
        "category": "pants", "brand": "StyleHub",
        "gender": "men",
        "description": "A modern jogger that bridges the gap between athleisure and casual wear. French terry cotton construction with elastic waistband, deep side pockets, and ribbed ankles.",
        "price": "1499", "original_price": "1999",
        "image_url": "https://images.unsplash.com/photo-1552902865-b72c031ac5ea?w=600&q=80",
        "stock": 55, "is_featured": True, "is_new_arrival": False, "rating": "4.4", "review_count": 88,
        "sizes": "28,30,32,34,36",
    },
    {
        "name": "Washed Straight Denim",
        "slug": "washed-straight-denim",
        "category": "pants", "brand": "StyleHub",
        "gender": "men",
        "description": "Classic straight-cut jeans with a medium-fade wash and slight distressing at the knees. 99% cotton denim with stretch comfort waistband for a natural feel.",
        "price": "2199", "original_price": "2999",
        "image_url": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=600&q=80",
        "stock": 42, "is_featured": False, "is_new_arrival": True, "rating": "4.7", "review_count": 195,
        "sizes": "28,30,32,34,36",
    },
    # Women's Pants
    {
        "name": "High Waist Flared Trousers",
        "slug": "high-waist-flared-trousers",
        "category": "pants", "brand": "StyleHub",
        "gender": "women",
        "description": "Elegant high-waist trousers with a dramatic flare silhouette. Crafted from flowy crepe fabric with a wide waistband and invisible side zip. Pairs beautifully with heels or chunky boots.",
        "price": "1999", "original_price": "2799",
        "image_url": "https://images.unsplash.com/photo-1551854596-4b4034b55c2b?w=600&q=80",
        "stock": 28, "is_featured": True, "is_new_arrival": True, "rating": "4.8", "review_count": 143,
        "sizes": "XS,S,M,L,XL",
    },
    {
        "name": "Pleated Corduroy Pants",
        "slug": "pleated-corduroy-pants",
        "category": "pants", "brand": "StyleHub",
        "gender": "women",
        "description": "Vintage-inspired pleated corduroy trousers in warm camel. Features a relaxed wide leg with front pleats and a high-rise waist. Perfect for autumn layering with boots and a turtleneck.",
        "price": "1699", "original_price": "2299",
        "image_url": "https://images.unsplash.com/photo-1593030761757-71fae45fa0e7?w=600&q=80",
        "stock": 30, "is_featured": True, "is_new_arrival": False, "rating": "4.5", "review_count": 76,
        "sizes": "XS,S,M,L,XL",
    },
    {
        "name": "Athleisure Jogger Pants",
        "slug": "athleisure-jogger-pants",
        "category": "pants", "brand": "StyleHub",
        "gender": "women",
        "description": "Ultra-soft lounge pants that go from workout to weekend. Four-way stretch fabric with moisture-wicking technology, deep pockets, and a flattering high waist with elasticated drawstring.",
        "price": "1299", "original_price": "1699",
        "image_url": "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=600&q=80",
        "stock": 65, "is_featured": False, "is_new_arrival": True, "rating": "4.6", "review_count": 201,
        "sizes": "XS,S,M,L,XL",
    },
    # T-Shirts
    {
        "name": "Graphic Print Oversized Tee",
        "slug": "graphic-print-oversized-tee",
        "category": "tshirts", "brand": "StyleHub",
        "gender": "unisex",
        "description": "A statement oversized tee featuring an original artwork print. Drop shoulders, boxy cut, and a heavyweight 220gsm cotton construction that holds its shape wash after wash.",
        "price": "799", "original_price": "999",
        "image_url": "https://images.unsplash.com/photo-1576566588028-4147f3842f27?w=600&q=80",
        "stock": 80, "is_featured": False, "is_new_arrival": True, "rating": "4.5", "review_count": 312,
        "sizes": "XS,S,M,L,XL,XXL",
    },
    {
        "name": "Essential Crew Neck Tee",
        "slug": "essential-crew-neck-tee",
        "category": "tshirts", "brand": "StyleHub",
        "gender": "unisex",
        "description": "The perfect blank canvas tee. Combed and ring-spun 100% cotton for exceptional softness. Pre-shrunk with reinforced shoulder seams. Available in 12 colours.",
        "price": "599", "original_price": "799",
        "image_url": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=600&q=80",
        "stock": 120, "is_featured": True, "is_new_arrival": False, "rating": "4.8", "review_count": 487,
        "sizes": "XS,S,M,L,XL,XXL",
    },
    {
        "name": "Astronaut Print Drop Shoulder Tee",
        "slug": "astronaut-print-drop-shoulder-tee",
        "category": "tshirts", "brand": "StyleHub",
        "gender": "unisex",
        "description": "An eye-catching space-themed print on a premium drop-shoulder silhouette. Screen-printed with water-based inks that won't crack or peel. Slightly cropped for a modern fit.",
        "price": "899", "original_price": "1199",
        "image_url": "https://images.unsplash.com/photo-1527719327859-c6ce80353573?w=600&q=80",
        "stock": 45, "is_featured": False, "is_new_arrival": True, "rating": "4.6", "review_count": 129,
        "sizes": "XS,S,M,L,XL,XXL",
    },
]

BLOGS = [
    {
        "title": "5 Ways to Style a Linen Shirt This Summer",
        "slug": "5-ways-style-linen-shirt-summer",
        "author": "Priya Menon",
        "excerpt": "Linen shirts are the ultimate summer wardrobe hero. Breathable, effortlessly cool, and endlessly versatile — here are five outfit formulas worth trying right now.",
        "content": """<p>As temperatures rise, the linen shirt becomes less of an option and more of a necessity. Lightweight, breathable, and naturally textured, it's the kind of piece that works equally well on a beach holiday or at a rooftop dinner.</p>
<h3>1. The Tuck-and-Tuck</h3>
<p>A fully-tucked linen shirt into high-waist trousers instantly elevates the look. Pair with loafers and a minimal leather belt for a polished summer-office outfit that won't have you sweating through meetings.</p>
<h3>2. Half-Tuck Over Shorts</h3>
<p>A casual half-tuck over well-fitted chino shorts is the weekend uniform. Leave the top two buttons undone and roll the sleeves to the elbow for that effortless "I just got here" vibe.</p>
<h3>3. Open as a Layer</h3>
<p>Wear the linen shirt completely unbuttoned over a plain tee or tank. This instantly adds dimension to a simple outfit and works brilliantly at the beach or festival.</p>
<h3>4. Knotted at the Waist</h3>
<p>Channel a relaxed 90s energy by knotting the shirt at your midriff over a midi skirt or wide-leg pants. This silhouette is having a major moment right now.</p>
<h3>5. Monochrome Linen Set</h3>
<p>If your shirt has matching linen trousers — wear the full set. A coordinated linen co-ord in ecru, sage, or dusty blue is one of the most stylish things you can wear this summer, requiring zero effort.</p>""",
        "image_url": "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=800&q=80",
    },
    {
        "title": "The Ultimate Guide to Building a Capsule Wardrobe",
        "slug": "ultimate-guide-capsule-wardrobe",
        "author": "Arjun Sharma",
        "excerpt": "A capsule wardrobe isn't about owning fewer clothes — it's about owning the right ones. Here's a practical guide to building a collection that always makes getting dressed effortless.",
        "content": """<p>The idea of a capsule wardrobe has been around since the 1970s, but it's never been more relevant. With fast fashion fatigue setting in and sustainability at the forefront of conversations, more people are investing in fewer, better pieces.</p>
<h3>Start With the Foundation</h3>
<p>Every capsule wardrobe needs neutral anchors: a white oxford shirt, a pair of well-fitted dark jeans, a navy blazer, and a simple crewneck sweater. These four pieces alone generate over 20 outfit combinations.</p>
<h3>Add Versatile Bottoms</h3>
<p>Two pairs of trousers (one casual, one formal), a classic straight-cut denim, and one pair of comfortable joggers covers virtually every occasion from boardroom to brunch.</p>
<h3>The Colour Rule</h3>
<p>Stick to a palette of no more than five colours that all work together. Classic combinations: navy-white-camel, black-white-grey, or olive-beige-rust. This ensures everything in your wardrobe can mix and match freely.</p>
<h3>Quality Over Quantity</h3>
<p>One well-made shirt that lasts five years is better than five cheap ones that fade after a month. Look for natural fibres, reinforced seams, and mother-of-pearl buttons as markers of quality.</p>""",
        "image_url": "https://images.unsplash.com/photo-1558769132-cb1aea458c5e?w=800&q=80",
    },
    {
        "title": "Cargo Pants Are Back — Here's How to Wear Them",
        "slug": "cargo-pants-back-how-to-wear",
        "author": "StyleHub Team",
        "excerpt": "The cargo pant has evolved from military surplus to high-fashion runway. We break down the modern way to wear this utilitarian classic without looking like you're going camping.",
        "content": """<p>Cargo pants had a moment in the early 2000s, then disappeared, and now they're everywhere again — but the silhouette has changed dramatically. Today's cargo is slimmer, the pockets are flatter, and the vibe is decidedly fashion-forward.</p>
<h3>The Slim Cargo + Tailored Shirt</h3>
<p>Pairing slim cargos with a well-pressed Oxford or chambray shirt creates a smart-casual contrast that works brilliantly for creative workplaces. Finish with clean leather sneakers or loafers.</p>
<h3>The Streetwear Stack</h3>
<p>Wide-leg cargos with a fitted graphic tee and chunky sneakers is peak streetwear. The key is proportions — let the pants be the statement and keep everything else simple.</p>
<h3>The Editorial Play</h3>
<p>Fashion editors style cargos with tailored blazers and heeled boots for an editorial juxtaposition. This works especially well in neutral palettes — camel cargo, white tee, oversized beige blazer.</p>
<h3>What to Avoid</h3>
<p>Avoid overly baggy cargos with overly baggy tops — the silhouette becomes shapeless. Also avoid too many utility elements in one look; cargos are statement enough on their own.</p>""",
        "image_url": "https://images.unsplash.com/photo-1624378439575-d8705ad7ae80?w=800&q=80",
    },
    {
        "title": "How to Care for Your Cotton Clothes (And Make Them Last)",
        "slug": "how-to-care-for-cotton-clothes",
        "author": "Deepika Rao",
        "excerpt": "Most people are unknowingly destroying their favourite cotton pieces in the wash. A few simple changes to your laundry routine can dramatically extend the life of your clothes.",
        "content": """<p>Cotton is the most popular natural fibre in the world, and for good reason. But it's also one of the most frequently mistreated fabrics in the laundry room. Here's how to treat your cotton pieces right.</p>
<h3>Wash in Cold Water</h3>
<p>Hot water is cotton's enemy. It causes shrinkage, fades colour faster, and breaks down fibres prematurely. Cold water (30°C or below) cleans just as effectively for normal wear and preserves your clothes much longer.</p>
<h3>Turn Dark Items Inside Out</h3>
<p>The friction of washing causes surface pilling and colour loss. Turning dark cotton items inside out dramatically reduces fading and keeps that fresh-from-the-shop look for longer.</p>
<h3>Skip the Tumble Dryer</h3>
<p>Air drying is the single best thing you can do for cotton. The heat of a dryer shrinks fibres and weakens elastic. Hang shirts on padded hangers, and lay knits flat to dry to maintain shape.</p>
<h3>Store Properly</h3>
<p>T-shirts and knitwear should be folded, not hung — hanging stretches the shoulders over time. Shirts and trousers should hang in a breathable garment bag, away from direct sunlight which causes yellowing.</p>""",
        "image_url": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&q=80",
    },
    {
        "title": "Summer 2025 Colour Trends to Know Right Now",
        "slug": "summer-2025-colour-trends",
        "author": "Priya Menon",
        "excerpt": "From dusty terracotta to digital lavender, the colour palette for this season is anything but boring. Here are the six shades dominating runways and street style this summer.",
        "content": """<p>Every season, a handful of colours emerge from the runway chaos and filter into everyday wardrobes. For Summer 2025, the palette swings between earthy warmth and digital vibrancy in a way we haven't seen before.</p>
<h3>Terracotta</h3>
<p>The undisputed colour of the season. Warm, clay-toned, and flattering on virtually every skin tone. Wear as a monochrome set or as an accent piece against neutrals.</p>
<h3>Digital Lavender</h3>
<p>A cool, muted purple with a soft, almost grey undertone. It pairs beautifully with white and cream, and works for both casual and formal contexts.</p>
<h3>Butter Yellow</h3>
<p>Not the bold canary of previous summers — this is softer, creamier, and more wearable. A butter yellow linen shirt is the sleeper hit of the season.</p>
<h3>Forest Green</h3>
<p>A perennial favourite that's especially strong this year. Deep, rich, and versatile — it works in every fabric from cotton to silk.</p>
<h3>Off White / Ecru</h3>
<p>The quietly cool alternative to white. Ecru has a warmth that pure white lacks, making it easier to wear and less harsh against the skin.</p>""",
        "image_url": "https://images.unsplash.com/photo-1523381210434-271e8be1f52b?w=800&q=80",
    },
]


class Command(BaseCommand):
    help = 'Seed the database with real product and blog data'

    def handle(self, *args, **options):
        # Categories
        categories = {
            'shirts': Category.objects.get_or_create(slug='shirts', defaults={'name': 'Shirts & Tops'})[0],
            'pants': Category.objects.get_or_create(slug='pants', defaults={'name': 'Pants & Trousers'})[0],
            'tshirts': Category.objects.get_or_create(slug='tshirts', defaults={'name': 'T-Shirts'})[0],
        }
        self.stdout.write('✓ Categories created')

        # Products
        for p in PRODUCTS:
            if not Product.objects.filter(slug=p['slug']).exists():
                Product.objects.create(
                    name=p['name'], slug=p['slug'],
                    category=categories[p['category']],
                    brand=p['brand'], gender=p['gender'],
                    description=p['description'],
                    price=p['price'],
                    original_price=p.get('original_price'),
                    image_url=p['image_url'],
                    stock=p['stock'],
                    is_featured=p['is_featured'],
                    is_new_arrival=p['is_new_arrival'],
                    rating=p['rating'],
                    review_count=p['review_count'],
                    sizes=p['sizes'],
                )
        self.stdout.write(f'✓ {len(PRODUCTS)} products created')

        # Blog posts
        for b in BLOGS:
            if not BlogPost.objects.filter(slug=b['slug']).exists():
                BlogPost.objects.create(**b)
        self.stdout.write(f'✓ {len(BLOGS)} blog posts created')

        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded successfully!'))
