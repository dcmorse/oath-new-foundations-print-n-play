import math
import glob
from typing import List, Tuple
from PIL import Image
from PIL import ImageColor
import numpy as np


def is_denizen_to_print(src_array, src_img, subimage_size, card_idxs) -> bool:
    rv = (
        is_new_foundations_denizen(card_idxs)
        or is_card_with_red_triangle(src_array, src_img, subimage_size, card_idxs)
        or is_royal_ambitions(src_img, card_idxs)
    )
    # print(
    #     f"{denizen_img_name(src_img, card_idxs)} ({denizen_img_suit(src_img)}) {card_idxs} {rv=}"
    # )
    return rv


def denizen_img_suit(src_img) -> str:
    filename = getattr(src_img, "filename", "")
    for suit in ["Arcane", "Hearth", "Beast", "Nomad", "Order", "Discord"]:
        if suit in filename:
            return suit
    raise ValueError(f"Cannot determine suit from filename '{filename}'")


def denizen_img_name(src_img, card_idxs) -> str | None:
    i, j = card_idxs
    return sloppy_card_titles[denizen_img_suit(src_img)][j][i]


def is_royal_ambitions(src_img, card_idxs) -> bool:
    return denizen_img_name(src_img, card_idxs) == "Royal Ambitions"


def is_new_foundations_denizen(card_idxs) -> bool:
    i, j = card_idxs
    return (i >= 3 and j == 3) or (i < 3 and j == 4)


def is_card_with_red_triangle(src_array, src_img, subimage_size, card_idxs) -> bool:
    red = ImageColor.getrgb("#d22147")
    # Ancient Pact wants #d12145
    # Round of Ale wants #d22147
    # Relic Thief wants #d22147
    # Bandit Chief wants #d22146
    expect_red_pxs = [(638, 995), (628, 1001), (646, 1001), (638, 983)]
    expect_not_red_pxs = [(624, 986), (652, 986), (638, 1010)]
    w, h = subimage_size
    i, j = card_idxs

    # only sample bottom right corner of the card
    scan_w, scan_h = 140, 130
    x0, y0, x1, y1 = (
        w * (i + 1) - scan_w,
        h * (j + 1) - scan_h,
        w * (i + 1),
        h * (j + 1),
    )
    sub_array = src_array[y0:y1, x0:x1]

    target_color = np.array(red)
    delta = 30

    # Calculate color distance for pixels in subregion only
    distances_squared = np.sum((sub_array - target_color) ** 2, axis=2)

    # Count pixels within delta
    red_pixel_count = np.sum(distances_squared <= delta**2)

    # log problematic red triangles by card name:
    # denizen_name = denizen_img_name(src_img, card_idxs)
    # if denizen_name in ["Bandit Chief", "A Round of Ale", "Ancient Pact"]:
    #     print(f"{denizen_name} {red_pixel_count}")

    if red_pixel_count < 10:
        return False
    elif 48 <= red_pixel_count <= 69:
        return True
    else:
        log_red_triangle_uncertainty(i, j, w, h, src_img, red_pixel_count)
        return False


def log_red_triangle_uncertainty(i, j, w, h, src_img, count):
    err_img = src_img.crop((i * w, j * h, (i + 1) * w, (j + 1) * h))
    src_filename = getattr(src_img, "filename", "unknown")
    if src_filename:
        src_basename = src_filename.split("/")[-1].split(".")[0]
    else:
        src_basename = "unknown"
    print(
        f"WARNING: Uncertain red triangle detection {count} for card '{src_filename}' ({i}, {j}), logging image"
    )
    err_img.save(f"wip/den-err-{i}-{j}-{src_basename}.png")

# Claude prompt:
#   Here's a grid of photos of cards, 10 wide by 5 high. The title of each card is in a black-background banner near the top. Can you write me a 2D python list literal with the title of each card?
# then
#   Nice work! You nailed it!
#   Now can you do it for the other suits: Arcane, Hearth, Beast, Nomad, and Order. Please put them in a map with their suit names as keys.
sloppy_card_titles = cards_by_suit = {
    "Arcane": [
        [
            "Alchemist",
            "Fire Talkers",
            "Magician's Code",
            "Spirit Snare",
            "Wizard School",
            "Oracle",
            "Acting Troupe",
            "Taming Charm",
            "Inquisitor",
            "Secret Signal",
        ],
        [
            "Augury",
            "Rusting Hay",
            "Quick Visit",
            "Billowing Fog",
            "Kindred Warriors",
            "Terror Spells",
            "Blood Pact",
            "Revelation",
            "Observatory",
            "Plague Engines",
        ],
        [
            "Gleaming Armor",
            "Bewitch",
            "Jinx",
            "Tutor",
            "Dream Thief",
            "Cracking Ground",
            "Scaling Wand",
            "Initiation Rite",
            "Vow of Silence",
            "Forgotten Vault",
        ],
        [
            "Map Library",
            "Witch's Bargain",
            "Master of Disguise",
            "Golem Legions",
            "Council Arbiter",
            "Catacombs",
            "Wand of Silence",
            "Vow of Wisdom",
            "Arcane Brokers",
            "Disciples",
        ],
        [
            "Arcane Armor",
            "Glamor",
            "Wizard's Conclave",
            "Ghost Spire",
            "Underground Library",
            "Magic Portal",
            "School of Wand",
            "Lost Lore",
            "",
            "",
        ],
    ],
    "Hearth": [
        [
            "Tinker's Fair",
            "Wayside Inn",
            "Extra Provisions",
            "Memory of Home",
            "Welcoming Party",
            "Traveling Doctor",
            "Storyteller",
            "Armed Mob",
            "Tavern Songs",
            "Homesteaders",
        ],
        [
            "Crop Rotation",
            "A Round of Ale",
            "Land Garden",
            "Charming Friend",
            "Village Constable",
            "Family Heirloom",
            "News from Afar",
            "Revelers",
            "Fabled Feast",
            "The Great Levy",
        ],
        [
            "Hearts and Minds",
            "Relic Breaker",
            "Book Binders",
            "Ballot Box",
            "Saddle Makers",
            "Herald",
            "Rowdy Pub",
            "Vow of Peace",
            "Deed Writer",
            "Salad Days",
        ],
        [
            "Marriage",
            "Hospital",
            "Awaited Return",
            "Old Songs",
            "Diplomat",
            "Village Idiot",
            "Spinning Bee",
            "Firebrand",
            "Watchdog",
            "Favored Son",
        ],
        [
            "Town Meeting",
            "League Treaty",
            "Skilled Merchants",
            "Hall of Debate",
            "Poisoned Mausoleum",
            "Old Watchtower",
            "Sacred Ground",
            "The Giant Oak",
            "",
            "",
        ],
    ],
    "Beast": [
        [
            "Errand Boy",
            "Wolves",
            "Animal Playmates",
            "True Flames",
            "The Old Oak",
            "Forest Paths",
            "Long-Lost Lair",
            "Rangers",
            "Roving Terror",
            "Future Worship",
        ],
        [
            "Birdsong",
            "Small Friends",
            "Grasping Vines",
            "Threatening Roar",
            "Fae Merchant",
            "Second Chance",
            "Pied Piper",
            "Mushrooms",
            "Insect Swarm",
            "Vow of Union",
        ],
        [
            "Giant Python",
            "War Tortoise",
            "Dew Growth",
            "Wild Cry",
            "Animal Feast",
            "Memory of Nature",
            "Marsh Spirit",
            "Vow of Poverty",
            "Forest Council",
            "Walled Garden",
        ],
        [
            "Vow of Beastskin",
            "Kracken",
            "Wild Lillies",
            "True Oath",
            "Dog",
            "Whispering Leaves",
            "Best of Hoots",
            "Autumn Wind",
            "Shifting Fog",
            "Fae Battalion",
        ],
        [
            "Hunger",
            "Signal Trees",
            "Forest Garden",
            "Power Temple",
            "Lost Hermitage",
            "Hollowed Spring",
            "Great Mall",
            "Great Aqueduct",
            "",
            "",
        ],
    ],
    "Nomad": [
        [
            "Rain Boots",
            "Ancient Binding",
            "Horse Archers",
            "Learning Signals",
            "Elders",
            "The Gathering",
            "Faithful Friend",
            "Tents",
            "Great Herd",
            "Convoys",
        ],
        [
            "Vow of Kinship",
            "Wild Mounts",
            "Lancers",
            "Mountain Giant",
            "Rival Khan",
            "Lost Tongue",
            "Special Envoy",
            "Berserk",
            "Oracle",
            "Pilgrimage",
        ],
        [
            "Spell Breaker",
            "Mounted Patrol",
            "Great Crusade",
            "Ancient Bloodline",
            "Ancient Pact",
            "Storm Caller",
            "Family Wagon",
            "War Station",
            "Twin Heather",
            "Hospitality",
        ],
        [
            "A Fast Steed",
            "Relic Worship",
            "Sacred Ground",
            "Tribute Spoke",
            "Search Party",
            "Moving Market",
            "Traveling Negotiator",
            "Pledge of Defense",
            "The Red Seer",
            "Royal Stables",
        ],
        [
            "Call for Help",
            "Vow of Wandering",
            "Mounted Library",
            "Great Forge",
            "War Dances",
            "Monument Trail",
            "Long Patrol",
            "Tomb Guardians",
            "",
            "",
        ],
    ],
    "Order": [
        [
            "Wrestlers",
            "Battle Donors",
            "Bear Traps",
            "Longbows",
            "Keep",
            "Pressgang",
            "Garrison",
            "Scouts",
            "Martial Culture",
            "Code of Honor",
        ],
        [
            "Outriders",
            "Messenger",
            "Field Promotion",
            "Palanquin",
            "Shield Wall",
            "Military Parade",
            "Tomb Guardians",
            "Tyrant",
            "Forced Labor",
            "Secret Police",
        ],
        [
            "Specialist",
            "Captains",
            "Siege Engines",
            "Royal Tax",
            "Toll Roads",
            "Curfew",
            "Knights Errant",
            "Vow of Obedience",
            "Hunting Party",
            "Council Seat",
        ],
        [
            "Encirclement",
            "Peace Envoy",
            "Relic Hunter",
            "Master at Arms",
            "Baron",
            "Honor Guard",
            "City Wall",
            "Fearsome General",
            "Careful Plans",
            "Garrison Armory",
        ],
        [
            "Battle Axes",
            "Great Feast",
            "Quartermaster",
            "Sprawling Ramparts",
            "Grand Canal",
            "The Tribunal",
            "Harbor Doors",
            "Proving Grounds",
            "",
            "",
        ],
    ],
    "Discord": [
        [
            "Mercenaries",
            "A Small Favor",
            "Second Wind",
            "Sleight of Hand",
            "Key to the City",
            "Sewer",
            "Obsessed Captain",
            "Daysavers",
            "Book Burning",
            "Charlatan",
        ],
        [
            "Assassin",
            "Downtrodden",
            "Blackmail",
            "Cracked Sage",
            "Dissent",
            "False Prophet",
            "Vow of Renewal",
            "Zealots",
            "Royal Ambitions",
            "Salt the Earth",
        ],
        [
            "Beast Tamer",
            "Riots",
            "Silver Tongue",
            "Gambling Hall",
            "Boiling Lake",
            "Relic Thief",
            "Enchantress",
            "Insomnia",
            "Sneak Attack",
            "Gossip",
        ],
        [
            "Bandit Chief",
            "Chaos Cult",
            "Slander",
            "Bandit Paymaster",
            "Reliquary Maid",
            "Tracker",
            "Banner Breakers",
            "Pledge to Discard",
            "Familiar Friar",
            "Unstable Summons",
        ],
        [
            "Bandit Prince",
            "Dark Enforcer",
            "Spoiled Supplies",
            "Festival District",
            "Spied Cards",
            "Coliseum",
            "Drowning Spell",
            "Loosening Tower",
            "",
            "",
        ],
    ],
}
