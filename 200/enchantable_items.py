import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from urllib.request import urlretrieve

from bs4 import BeautifulSoup as Soup

TMP = Path(os.getenv("TMP", "/tmp"))
HTML_FILE = TMP / "enchantment_list_pc.html"

# source:
# https://www.digminecraft.com/lists/enchantment_list_pc.php
URL = "https://bites-data.s3.us-east-2.amazonaws.com/" "minecraft-enchantment.html"

ROMAN = ["I", "II", "III", "IV", "V"]
RE_CLEAN = re.compile("_(?!rod)|enchanted|iron|sm")


@dataclass
class Enchantment:
    """Minecraft enchantment class"""

    id_name: str
    name: str
    max_level: int
    description: str
    items: list = field(default_factory=list)

    def __str__(self):
        return f"{self.name} ({self.max_level}): {self.description}"


@dataclass
class Item:
    """Minecraft enchantable item class"""

    name: str
    enchantments: list = field(default_factory=list)

    def __str__(self):
        result = f"{self.name.replace('_', ' ').title()}: "
        for x in sorted(self.enchantments, key=lambda x: x.id_name):
            result += f"\n  [{x.max_level}] {x.id_name}"
        return result


def generate_enchantments(soup):
    """Generates a dictionary of Enchantment objects

    With the key being the id_name of the enchantment.
    """

    items = {}
    results = {}
    for row in soup.find_all("tr")[1:]:
        cells = row.find_all("td")

        enchantment = Enchantment(
            name=cells[0].text.split("(")[0],
            max_level=1 + ROMAN.index(cells[1].text),
            description=cells[2].text,
            id_name=cells[0].text.split("(")[1][:-1],
        )

        raw_filename = Path(cells[4].find("img").attrs["data-src"]).stem
        item_names = RE_CLEAN.sub(" ", raw_filename).split()

        for item_name in item_names:
            if item_name not in items.keys():
                items[item_name] = Item(name=item_name)

            item = items[item_name]
            if enchantment not in item.enchantments:
                item.enchantments.append(enchantment)

            enchantment.items.append(items[item_name])

        results[enchantment.id_name] = enchantment

    return results


def generate_items(data):
    """Generates a dictionary of Item objects

    With the key being the item name.
    """
    results = {}
    for x in data.values():
        for y in x.items:
            if not y.name in results.keys():
                results[y.name] = y

    return results


def get_soup(file=HTML_FILE):
    """Retrieves/takes source HTML and returns a BeautifulSoup object"""
    if isinstance(file, Path):
        if not file.is_file():
            urlretrieve(URL, file)

        with file.open() as html_source:
            soup = Soup(html_source, "html.parser")
    else:
        soup = Soup(file, "html.parser")

    return soup


def main():
    """This function is here to help you test your final code.

    Once complete, the print out should match what's at the bottom of this file"""
    soup = get_soup()
    enchantment_data = generate_enchantments(soup)
    minecraft_items = generate_items(enchantment_data)
    for item in minecraft_items:
        print(minecraft_items[item], "\n")


if __name__ == "__main__":
    main()

"""
Armor: 
  [1] binding_curse
  [4] blast_protection
  [4] fire_protection
  [4] projectile_protection
  [4] protection
  [3] thorns 

Axe: 
  [5] bane_of_arthropods
  [5] efficiency
  [3] fortune
  [5] sharpness
  [1] silk_touch
  [5] smite 

Boots: 
  [3] depth_strider
  [4] feather_falling
  [2] frost_walker 

Bow: 
  [1] flame
  [1] infinity
  [5] power
  [2] punch 

Chestplate: 
  [1] mending
  [3] unbreaking
  [1] vanishing_curse 

Crossbow: 
  [1] multishot
  [4] piercing
  [3] quick_charge 

Fishing Rod: 
  [3] luck_of_the_sea
  [3] lure
  [1] mending
  [3] unbreaking
  [1] vanishing_curse 

Helmet: 
  [1] aqua_affinity
  [3] respiration 

Pickaxe: 
  [5] efficiency
  [3] fortune
  [1] mending
  [1] silk_touch
  [3] unbreaking
  [1] vanishing_curse 

Shovel: 
  [5] efficiency
  [3] fortune
  [1] silk_touch 

Sword: 
  [5] bane_of_arthropods
  [2] fire_aspect
  [2] knockback
  [3] looting
  [1] mending
  [5] sharpness
  [5] smite
  [3] sweeping
  [3] unbreaking
  [1] vanishing_curse 

Trident: 
  [1] channeling
  [5] impaling
  [3] loyalty
  [3] riptide
"""
