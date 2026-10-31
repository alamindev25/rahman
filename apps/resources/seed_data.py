import os
import sys
import django
from PIL import Image, ImageDraw, ImageFont

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
sys.path.append(os.getcwd())
django.setup()

from apps.resources.models import ResourceItem

MEDIA_ICONS_DIR = os.path.join("media", "icons")
os.makedirs(MEDIA_ICONS_DIR, exist_ok=True)


def create_icon(name, draw_func):
    size = 128
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Circle background (soft sky blue)
    draw.ellipse([8, 8, size - 8, size - 8], fill=(230, 244, 254, 255))

    # Icon foreground color (cyan/sky blue)
    color = (2, 132, 199, 255)  # #0284c7

    # Call specific drawing function
    draw_func(draw, size, color)

    filename = f"{name}.png"
    filepath = os.path.join(MEDIA_ICONS_DIR, filename)
    image.save(filepath, "PNG")
    return f"icons/{filename}"


def draw_plane(draw, s, c):
    # Airplane icon
    # Main body
    draw.polygon([(s*0.3, s*0.65), (s*0.75, s*0.25), (s*0.7, s*0.35), (s*0.45, s*0.7)], fill=c)
    # Wings
    draw.polygon([(s*0.45, s*0.4), (s*0.25, s*0.35), (s*0.35, s*0.55)], fill=c)
    draw.polygon([(s*0.55, s*0.6), (s*0.6, s*0.8), (s*0.68, s*0.7)], fill=c)


def draw_umbrella(draw, s, c):
    # Umbrella icon
    draw.chord([s*0.25, s*0.25, s*0.75, s*0.65], 180, 360, fill=c)
    # Pole
    draw.line([(s*0.5, s*0.45), (s*0.5, s*0.75)], fill=c, width=5)
    draw.arc([s*0.4, s*0.7, s*0.5, s*0.82], 0, 180, fill=c, width=5)


def draw_shield(draw, s, c):
    # Shield check icon
    draw.polygon([(s*0.5, s*0.2), (s*0.75, s*0.3), (s*0.75, s*0.6), (s*0.5, s*0.82), (s*0.25, s*0.6), (s*0.25, s*0.3)], fill=c)
    # Inner check (white)
    draw.line([(s*0.38, s*0.5), (s*0.48, s*0.6), (s*0.65, s*0.4)], fill=(255, 255, 255, 255), width=6)


def draw_cruise(draw, s, c):
    # Cruise ship icon
    draw.polygon([(s*0.2, s*0.6), (s*0.8, s*0.6), (s*0.72, s*0.78), (s*0.28, s*0.78)], fill=c)
    draw.rectangle([s*0.35, s*0.42, s*0.65, s*0.58], fill=c)
    draw.rectangle([s*0.42, s*0.3, s*0.58, s*0.40], fill=c)


def draw_sea(draw, s, c):
    # Boat at sea icon
    draw.polygon([(s*0.25, s*0.55), (s*0.75, s*0.55), (s*0.68, s*0.7), (s*0.32, s*0.7)], fill=c)
    draw.polygon([(s*0.5, s*0.25), (s*0.5, s*0.5), (s*0.7, s*0.5)], fill=c)
    # Waves
    draw.arc([s*0.2, s*0.72, s*0.5, s*0.82], 0, 180, fill=c, width=4)
    draw.arc([s*0.5, s*0.72, s*0.8, s*0.82], 0, 180, fill=c, width=4)


def draw_stethoscope(draw, s, c):
    # Stethoscope icon
    draw.arc([s*0.3, s*0.25, s*0.7, s*0.6], 0, 180, fill=c, width=6)
    draw.line([(s*0.3, s*0.25), (s*0.3, s*0.35)], fill=c, width=6)
    draw.line([(s*0.7, s*0.25), (s*0.7, s*0.35)], fill=c, width=6)
    draw.line([(s*0.5, s*0.6), (s*0.5, s*0.72)], fill=c, width=6)
    draw.ellipse([s*0.44, s*0.7, s*0.56, s*0.82], fill=c)


def draw_bank(draw, s, c):
    # Bank building icon
    draw.polygon([(s*0.5, s*0.22), (s*0.8, s*0.38), (s*0.2, s*0.38)], fill=c)
    draw.rectangle([s*0.2, s*0.38, s*0.8, s*0.44], fill=c)
    draw.rectangle([s*0.25, s*0.44, s*0.33, s*0.72], fill=c)
    draw.rectangle([s*0.46, s*0.44, s*0.54, s*0.72], fill=c)
    draw.rectangle([s*0.67, s*0.44, s*0.75, s*0.72], fill=c)
    draw.rectangle([s*0.18, s*0.72, s*0.82, s*0.78], fill=c)


def draw_diet(draw, s, c):
    # Bowl of food icon
    draw.chord([s*0.2, s*0.38, s*0.8, s*0.78], 0, 180, fill=c)
    draw.ellipse([s*0.3, s*0.26, s*0.5, s*0.42], fill=c)
    draw.ellipse([s*0.48, s*0.22, s*0.68, s*0.4], fill=c)


def draw_tips(draw, s, c):
    # Travel tips / flight icon
    draw.ellipse([s*0.25, s*0.25, s*0.75, s*0.75], outline=c, width=5)
    draw.polygon([(s*0.35, s*0.6), (s*0.65, s*0.35), (s*0.6, s*0.42), (s*0.45, s*0.65)], fill=c)


def draw_faq(draw, s, c):
    # Question mark circle icon
    draw.ellipse([s*0.2, s*0.2, s*0.8, s*0.8], outline=c, width=6)
    draw.arc([s*0.38, s*0.3, s*0.62, s*0.52], 180, 360, fill=c, width=6)
    draw.line([(s*0.62, s*0.41), (s*0.5, s*0.55)], fill=c, width=6)
    draw.line([(s*0.5, s*0.55), (s*0.5, s*0.62)], fill=c, width=6)
    draw.ellipse([s*0.46, s*0.68, s*0.54, s*0.76], fill=c)


RESOURCES_DATA = [
    {
        "order": 1,
        "title": "Book Dialysis Abroad",
        "sub_title": "Book Dialysis Abroad",
        "description": "Plan treatment overseas with clinic matching and booking support.",
        "is_highlighted": True,
        "icon_key": "book_dialysis_abroad",
        "draw": draw_plane,
    },
    {
        "order": 2,
        "title": "Holiday Destinations",
        "sub_title": "Holiday Destinations",
        "description": "Explore travel-ready places with access to dialysis support.",
        "is_highlighted": False,
        "icon_key": "holiday_destinations",
        "draw": draw_umbrella,
    },
    {
        "order": 3,
        "title": "Travel Insurance",
        "sub_title": "Travel Insurance",
        "description": "Understand cover questions for dialysis and kidney care trips.",
        "is_highlighted": False,
        "icon_key": "travel_insurance",
        "draw": draw_shield,
    },
    {
        "order": 4,
        "title": "Cruise Dialysis",
        "sub_title": "Cruise Dialysis",
        "description": "Plan cruise holidays with dialysis-friendly preparation.",
        "is_highlighted": False,
        "icon_key": "cruise_dialysis",
        "draw": draw_cruise,
    },
    {
        "order": 5,
        "title": "Dialysis at Sea",
        "sub_title": "Dialysis at Sea",
        "description": "Guidance for treatment schedules during sea travel.",
        "is_highlighted": False,
        "icon_key": "dialysis_at_sea",
        "draw": draw_sea,
    },
    {
        "order": 6,
        "title": "Patient Guides",
        "sub_title": "Patient Guides",
        "description": "Practical checklists for dialysis patients and families.",
        "is_highlighted": False,
        "icon_key": "patient_guides",
        "draw": draw_stethoscope,
    },
    {
        "order": 7,
        "title": "Benefits & Financial Help",
        "sub_title": "Benefits & Financial Help",
        "description": "Find support topics for costs, benefits, and care funding.",
        "is_highlighted": False,
        "icon_key": "benefits_financial_help",
        "draw": draw_bank,
    },
    {
        "order": 8,
        "title": "Kidney Diet",
        "sub_title": "Kidney Diet",
        "description": "Diet planning reminders for travel and everyday kidney care.",
        "is_highlighted": False,
        "icon_key": "kidney_diet",
        "draw": draw_diet,
    },
    {
        "order": 9,
        "title": "Travel Tips",
        "sub_title": "Travel Tips",
        "description": "Smart preparation for flights, documents, and appointments.",
        "is_highlighted": False,
        "icon_key": "travel_tips",
        "draw": draw_tips,
    },
    {
        "order": 10,
        "title": "FAQs",
        "sub_title": "FAQs",
        "description": "Answers to common dialysis booking and travel questions.",
        "is_highlighted": False,
        "icon_key": "faqs",
        "draw": draw_faq,
    },
]


def run():
    print("Clearing old resource items or updating...")
    # Delete existing items or update them
    ResourceItem.objects.all().delete()

    for data in RESOURCES_DATA:
        icon_path = create_icon(data["icon_key"], data["draw"])
        item = ResourceItem.objects.create(
            order=data["order"],
            resource_type=data["icon_key"],
            title=data["title"],
            sub_title=data["sub_title"],
            description=data["description"],
            is_highlighted=data["is_highlighted"],
            icon_image=icon_path,
        )
        print(f"Created ResourceItem #{item.order}: {item.title} [{item.resource_type}] ({icon_path})")

    print("Finished seeding resources successfully!")


if __name__ == "__main__":
    run()
