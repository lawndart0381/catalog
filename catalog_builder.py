from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from catalog_setup import Base, User, Category, Item

engine = create_engine('postgresql://catalog:pa$$word@localhost/catalog')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# First User
user1 = User(id=1, name="Sean Magrann", email="mag4417@gmail.com")
session.add(user1)
session.commit()

# Categories and Items
category1 = Category(name="Dry Flies", image="dryflies.jpg", user=user1)
session.add(category1)
session.commit()

item1 = Item(name="Elk Hair Caddis",
             description="Most effective Caddis pattern out there!",
             price="$3.99", image="elkhair.jpg",
             category=category1, user=user1)
session.add(item1)
session.commit()

item2 = Item(name="Parachute Adams",
             description="The most commonly used dry fly ever!",
             price="$3.99", image="parachute.jpg",
             category=category1, user=user1)
session.add(item2)
session.commit()

item3 = Item(name="Light Cahill",
             description="Popular fly for imitating a Cahill Dun!",
             price="$3.99", image="cahill.jpg",
             category=category1, user=user1)
session.add(item3)
session.commit()

item4 = Item(name="Royal Wulff",
             description="Popular attractor pattern by Lee Wulff!",
             price="$3.49", image="royal.jpg",
             category=category1, user=user1)
session.add(item4)
session.commit()

item5 = Item(name="Fat Albert",
             description="Wild and buggy pattern that trout go crazy for!",
             price="$3.49", image="fat_albert.jpg",
             category=category1, user=user1)
session.add(item5)
session.commit()

category2 = Category(name="Wet Flies", image='wetflies.jpg', user=user1)
session.add(category2)
session.commit()

item1 = Item(name="Hunchback Scud",
             description="Classic pattern for targeting trout!",
             price="$5.99", image="scud.jpg", category=category2, user=user1)
session.add(item1)
session.commit()

item2 = Item(name="Pheasant Tail Nymph",
             description="Popular all-purpose pattern!", price="$2.99",
             image="pheasant_tail.jpg", category=category2, user=user1)
session.add(item2)
session.commit()

item3 = Item(name="Rainbow Warrior",
             description="A flashy nymph that grabs the attention of trout!",
             price="$3.49",
             image="rainbow_warrior.jpg", category=category2, user=user1)
session.add(item3)
session.commit()

item4 = Item(name="Zebra Midge",
             description="Classic pattern that trout go crazy for!",
             price="$3.99", image="zebramidge.jpg",
             category=category2, user=user1)
session.add(item4)
session.commit()

item5 = Item(name="Red Copper John",
             description="Copper Johns are an excellent all-purpose pattern!",
             price="$4.99", image="copper.jpg",
             category=category2, user=user1)
session.add(item5)
session.commit()


category3 = Category(name="Fly Rods", image="flyrods.jpg", user=user1)
session.add(category3)
session.commit()

item1 = Item(name="Signature Fly Rod",
             description="High performance, light weight, and fast action!",
             price="$250.00", image="flyrod.jpg",
             category=category3, user=user1)
session.add(item1)
session.commit()

item2 = Item(name="Classic Fly Rod",
             description="Moderate action makes this rod extremely versatile!",
             price="$150.00", image="flyrod2.jpg",
             category=category3, user=user1)
session.add(item2)
session.commit()

item3 = Item(name="SWS Fly Rod",
             description="Super strong fast action provides casting accuracy!",
             price="$650.00", image="flyrod3.jpg",
             category=category3, user=user1)
session.add(item3)
session.commit()

item4 = Item(name="Eagle Fly Rod",
             description="Entry level fly rod for beginners!",
             price="$99.00", image="flyrod4.jpg",
             category=category3, user=user1)
session.add(item4)
session.commit()

item5 = Item(name="Santo Fly Rod",
             description="Premium graphite rod for smoother casting!",
             price="$130.00", image="flyrod1.jpg",
             category=category3, user=user1)
session.add(item5)
session.commit()

category4 = Category(name="Fly Reels", image="flyreels.jpg", user=user1)
session.add(category4)
session.commit()

item1 = Item(name="Colorado Fly Reel",
             description="High performance and corrosion resistant!",
             price="$50.00", image="reel.jpg",
             category=category4, user=user1)
session.add(item1)
session.commit()

item2 = Item(name="Speedster Reel",
             description="Super fast retrieval high perfomance fishing reel",
             price="$175.00", image="reel2.jpg",
             category=category4, user=user1)
session.add(item2)
session.commit()

item3 = Item(name="Rapids Fly Reel",
             description="Easy to grip handle and silent retrieval!",
             price="$75.00", image="reel3.jpg",
             category=category4, user=user1)
session.add(item3)
session.commit()

item4 = Item(name="Eagle Fly Reel",
             description="Entry level fly reel for beginners!",
             price="$39.00", image="reel4.jpg",
             category=category4, user=user1)
session.add(item4)
session.commit()

item5 = Item(name="Remix Fly Reel",
             description="CNC machined for a preceision fit and finish!",
             price="$180.00", image="reel1.jpg",
             category=category4, user=user1)
session.add(item5)
session.commit()

category5 = Category(name="Waders", image="waders.jpg", user=user1)
session.add(category5)
session.commit()

item1 = Item(name="Premium Chest Waders",
             description="Breathable stockingfoot chest waders.",
             price="$121.99", image="chest_wader.jpg",
             category=category5, user=user1)
session.add(item1)
session.commit()

item2 = Item(name="Bootfoot Chest Waders",
             description="Ultraflexible neoprene chest waders.",
             price="$99.99", image="chest_wader2.jpg",
             category=category5, user=user1)
session.add(item2)
session.commit()

item3 = Item(name="Wading Pants",
             description="Breathable & waterproof GORE-TEX wading pants.",
             price="$299.00", image="wader_pants.jpg",
             category=category5, user=user1)
session.add(item3)
session.commit()

item4 = Item(name="Hip Boots",
             description="Waterproof hip boots for wading in shallow water.",
             price="$99.00", image="hip_boots.jpg",
             category=category5, user=user1)
session.add(item4)
session.commit()

item5 = Item(name="Stockingfoot Hip Waders",
             description="Four-ply nylon for shallow water wading.",
             price="$89.99", image="hip_wader.jpg",
             category=category5, user=user1)
session.add(item5)
session.commit()

category6 = Category(name="Wading Boots", image="wadingboots.jpg", user=user1)
session.add(category6)
session.commit()

item1 = Item(name="Ultralight Boots",
             description="Rugged nylon and synthetic boots with rubber soles.",
             price="$75.99", image="boots1.jpg",
             category=category6, user=user1)
session.add(item1)
session.commit()

item2 = Item(name="Guide Boots",
             description="Waterproof boots with rubber soles.",
             price="$199.99", image="boots2.jpg",
             category=category6, user=user1)
session.add(item2)
session.commit()

item3 = Item(name="Hightop Sneaker Boots",
             description="Durable leather boots with rubber traction soles.",
             price="$99.00", image="boots3.jpg",
             category=category6, user=user1)
session.add(item3)
session.commit()

item4 = Item(name="Felt Sole Boots",
             description="100% waterproof insulated boots with felt soles.",
             price="$99.00", image="boots4.jpg",
             category=category6, user=user1)
session.add(item4)
session.commit()

item5 = Item(name="Lug Sole Boots",
             description="Leather boots with replaceable metal lug soles.",
             price="$89.99", image="boots5.jpg",
             category=category6, user=user1)
session.add(item5)
session.commit()

category7 = Category(name="Float Tubes", image="floattubes.jpg", user=user1)
session.add(category7)
session.commit()

item1 = Item(name="Classic Float",
             description="Rides higher for better visibility on the water!",
             price="$219.99", image="float1.jpg",
             category=category7, user=user1)
session.add(item1)
session.commit()

item2 = Item(name="Caddis Float",
             description="Float tube that won't let you down on the water!",
             price="$99.99", image="float2.jpg",
             category=category7, user=user1)
session.add(item2)
session.commit()

item3 = Item(name="Fish Cat",
             description="Ample storage for a full day on the water!",
             price="$219.00", image="float3.jpg",
             category=category7, user=user1)
session.add(item3)
session.commit()

item4 = Item(name="Float Combo Pack",
             description="Rugged float tube complete with fins and foot pump!",
             price="$159.99", image="float4.jpg",
             category=category7, user=user1)
session.add(item4)
session.commit()

item5 = Item(name="Caddis Premier Float",
             description="Heavy-duty construction for the avid fisherman!",
             price="$198.99", image="float5.jpg",
             category=category7, user=user1)
session.add(item5)
session.commit()

category8 = Category(name="Tackle", image="tackle.jpg", user=user1)
session.add(category8)
session.commit()

item1 = Item(name="Fly-Tying Bag",
             description="Tie your flies anywhere with this travel bag!",
             price="$25.99", image="flytiebag.jpg",
             category=category8, user=user1)
session.add(item1)
session.commit()

item2 = Item(name="Duffle Bag",
             description="Large duffle bag perfect for day trips!",
             price="$169.99", image="duffle.jpg",
             category=category8, user=user1)
session.add(item2)
session.commit()

item3 = Item(name="Fishing Vest",
             description="Cool breathable mesh construction.", price="$99.00",
             image="vest.jpg", category=category8, user=user1)
session.add(item3)
session.commit()

item4 = Item(name="Chest Pack",
             description="The perfect tackle for the minimalist!",
             price="$19.00", image="chestpack.jpg",
             category=category8, user=user1)
session.add(item4)
session.commit()

item5 = Item(name="Sling Pack",
             description="Easily carry all your gear on day trips.",
             price="$89.99", image="slingbag.jpg",
             category=category8, user=user1)
session.add(item5)
session.commit()

print "added categories & items!"
