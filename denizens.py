import math
import glob
from typing import List, Tuple
from abc import ABC, abstractmethod
from PIL import Image
from PIL import ImageColor
import numpy as np


class Denizen(ABC):
    def __init__(self, name: str):
        self._name = name

    @property
    def name(self) -> str:
        return self._name

    @abstractmethod
    def prints(self) -> bool:
        pass


class BaseDenizen(Denizen):
    def prints(self) -> bool:
        return False


class RevisedDenizen(Denizen):
    def prints(self) -> bool:
        return True


class NFDenizen(Denizen):
    def prints(self) -> bool:
        return True


class DudEdifice(Denizen):
    def prints(self) -> bool:
        return False


class DeletedDenizen(Denizen):
    def prints(self) -> bool:
        return False


def is_new_denizen(src_img, subimage_size, card_idxs) -> bool:
    denizen = img_denizen(src_img, card_idxs)
    return denizen and denizen.prints()


def denizen_img_suit(src_img) -> str:
    filename = getattr(src_img, "filename", "")
    for suit in ["Arcane", "Hearth", "Beast", "Nomad", "Order", "Discord"]:
        if suit in filename:
            return suit
    raise ValueError(f"Cannot determine suit from filename '{filename}'")


def img_denizen(src_img, card_idxs) -> Denizen | None:
    i, j = card_idxs
    row = card_sheets[denizen_img_suit(src_img)][j]
    return row[i] if i < len(row) else None


card_sheets = {
    "Arcane": [
        [
            RevisedDenizen("Alchemist"),
            BaseDenizen("Fire Talkers"),
            RevisedDenizen("Magician's Code"),
            BaseDenizen("Spirit Snare"),
            BaseDenizen("Wizard School"),
            BaseDenizen("Oracle"),
            BaseDenizen("Acting Troupe"),
            BaseDenizen("Taming Charm"),
            RevisedDenizen("Inquisitor"),
            BaseDenizen("Secret Signal"),
        ],
        [
            BaseDenizen("Augury"),
            BaseDenizen("Rusting Ray"),
            RevisedDenizen("Quick Exit"),
            BaseDenizen("Billowing Fog"),
            BaseDenizen("Kindred Warriors"),
            BaseDenizen("Terror Spells"),
            BaseDenizen("Blood Pact"),
            BaseDenizen("Revelation"),
            BaseDenizen("Observatory"),
            BaseDenizen("Plague Engines"),
        ],
        [
            BaseDenizen("Gleaming Armor"),
            RevisedDenizen("Bewitch"),
            BaseDenizen("Jinx"),
            BaseDenizen("Tutor"),
            BaseDenizen("Dream Thief"),
            BaseDenizen("Cracking Ground"),
            BaseDenizen("Sealing Ward"),
            BaseDenizen("Initiation Rite"),
            RevisedDenizen("Vow of Silence"),
            RevisedDenizen("Forgotten Vault"),
        ],
        [
            BaseDenizen("Map Library"),
            BaseDenizen("Witch's Bargain"),
            BaseDenizen("Master of Disguise"),
            NFDenizen("Golem Legions"),
            NFDenizen("Council Arbiter"),
            NFDenizen("Catacombs"),
            NFDenizen("Wand of Silence"),
            NFDenizen("Vow of Wisdom"),
            NFDenizen("Arcane Brokers"),
            NFDenizen("Disciples"),
        ],
        [
            NFDenizen("Arcane Armor"),
            NFDenizen("Glamor"),
            NFDenizen("Wizard's Conclave"),
            DudEdifice("Great Spire"),
            DudEdifice("Underground Library"),
            DudEdifice("Magic Portal"),
            DudEdifice("School of Vines"),
            DudEdifice("Lost Lore"),
        ],
    ],
    "Hearth": [
        [
            RevisedDenizen("Tinker's Fair"),
            BaseDenizen("Wayside Inn"),
            BaseDenizen("Extra Provisions"),
            RevisedDenizen("Memory of Home"),
            BaseDenizen("Welcoming Party"),
            BaseDenizen("Traveling Doctor"),
            BaseDenizen("Storyteller"),
            BaseDenizen("Armed Mob"),
            BaseDenizen("Tavern Songs"),
            BaseDenizen("Homesteaders"),
        ],
        [
            BaseDenizen("Crop Rotation"),
            RevisedDenizen("A Round of Ale"),
            BaseDenizen("Walled Garden"),
            BaseDenizen("Charming Friend"),
            BaseDenizen("Village Constable"),
            BaseDenizen("Family Heirloom"),
            BaseDenizen("News from Afar"),
            BaseDenizen("Levelers"),
            BaseDenizen("Fabled Feast"),
            BaseDenizen("The Great Levy"),
        ],
        [
            BaseDenizen("Hearts and Minds"),
            RevisedDenizen("Relic Breaker"),
            BaseDenizen("Book Binders"),
            RevisedDenizen("Ballot Box"),
            BaseDenizen("Saddle Makers"),
            BaseDenizen("Herald"),
            BaseDenizen("Rowdy Pub"),
            BaseDenizen("Vow of Peace"),
            RevisedDenizen("Deed Writer"),
            BaseDenizen("Salad Days"),
        ],
        [
            BaseDenizen("Marriage"),
            BaseDenizen("Hospital"),
            BaseDenizen("Awaited Return"),
            NFDenizen("Old Songs"),
            NFDenizen("Diplomat"),
            NFDenizen("Village Idiot"),
            NFDenizen("Spinning Bee"),
            NFDenizen("Firebrand"),
            NFDenizen("Watchdog"),
            NFDenizen("Favored Son"),
        ],
        [
            NFDenizen("Town Meeting"),
            NFDenizen("League Treaty"),
            NFDenizen("Skilled Merchants"),
            DudEdifice("Hall of Debate"),
            DudEdifice("Poisoned Mausoleum"),
            DudEdifice("Old Watchtower"),
            DudEdifice("Sacred Ground"),
            DudEdifice("The Giant Oak"),
        ],
    ],
    "Beast": [
        [
            BaseDenizen("Errand Boy"),
            BaseDenizen("Wolves"),
            BaseDenizen("Animal Playmates"),
            BaseDenizen("True Flames"),
            BaseDenizen("The Old Oak"),
            BaseDenizen("Forest Paths"),
            RevisedDenizen("Long-Lost Heir"),
            BaseDenizen("Rangers"),
            BaseDenizen("Roving Terror"),
            BaseDenizen("Nature Worship"),
        ],
        [
            BaseDenizen("Birdsong"),
            BaseDenizen("Small Friends"),
            BaseDenizen("Grasping Vines"),
            BaseDenizen("Threatening Roar"),
            BaseDenizen("Fae Merchant"),
            BaseDenizen("Second Chance"),
            BaseDenizen("Pied Piper"),
            BaseDenizen("Mushrooms"),
            BaseDenizen("Insect Swarm"),
            RevisedDenizen("Vow of Union"),
        ],
        [
            RevisedDenizen("Giant Python"),
            BaseDenizen("War Tortoise"),
            BaseDenizen("New Growth"),
            BaseDenizen("Wild Cry"),
            BaseDenizen("Animal Feast"),
            BaseDenizen("Memory of Nature"),
            BaseDenizen("Marsh Spirit"),
            BaseDenizen("Vow of Poverty"),
            RevisedDenizen("Forest Council"),
            BaseDenizen("Walled Garden"),
        ],
        [
            BaseDenizen("Vow of Beastkin"),
            RevisedDenizen("Bracken"),
            BaseDenizen("Wild Allies"),
            NFDenizen("True Oath"),
            NFDenizen("Bog"),
            NFDenizen("Whispering Leaves"),
            NFDenizen("Bed of Roots"),
            NFDenizen("Autumn Wind"),
            NFDenizen("Shifting Fog"),
            NFDenizen("Fae Battalion"),
        ],
        [
            NFDenizen("Hunger"),
            NFDenizen("Signal Trees"),
            NFDenizen("Forest Garden"),
            DudEdifice("Power Temple"),
            DudEdifice("Lost Hermitage"),
            DudEdifice("Hollowed Spring"),
            DudEdifice("Great Mall"),
            DudEdifice("Great Aqueduct"),
        ],
    ],
    "Nomad": [
        [
            BaseDenizen("Rain Boots"),
            BaseDenizen("Ancient Binding"),
            BaseDenizen("Horse Archers"),
            BaseDenizen("Learning Signals"),
            BaseDenizen("Elders"),
            BaseDenizen("The Gathering"),
            BaseDenizen("Faithful Friend"),
            BaseDenizen("Tents"),
            BaseDenizen("Great Herd"),
            BaseDenizen("Convoys"),
        ],
        [
            BaseDenizen("Vow of Kinship"),
            BaseDenizen("Wild Mounts"),
            BaseDenizen("Lancers"),
            BaseDenizen("Mountain Giant"),
            BaseDenizen("Rival Khan"),
            BaseDenizen("Lost Tongue"),
            BaseDenizen("Special Envoy"),
            BaseDenizen("Berserk"),
            BaseDenizen("Oracle"),
            BaseDenizen("Pilgrimage"),
        ],
        [
            BaseDenizen("Spell Breaker"),
            BaseDenizen("Mounted Patrol"),
            BaseDenizen("Great Crusade"),
            BaseDenizen("Ancient Bloodline"),
            RevisedDenizen("Ancient Pact"),
            BaseDenizen("Storm Caller"),
            RevisedDenizen("Family Wagon"),
            BaseDenizen("Way Station"),
            BaseDenizen("Twin Brother"),
            BaseDenizen("Hospitality"),
        ],
        [
            BaseDenizen("A Fast Steed"),
            RevisedDenizen("Relic Worship"),
            DeletedDenizen("Sacred Ground"),
            NFDenizen("Tribute Spoils"),
            NFDenizen("Search Party"),
            NFDenizen("Moving Market"),
            NFDenizen("Traveling Negotiator"),
            NFDenizen("Pledge of Defense"),
            NFDenizen("The Red Seer"),
            NFDenizen("Royal Stables"),
        ],
        [
            NFDenizen("Call for Help"),
            NFDenizen("Vow of Wandering"),
            NFDenizen("Mounted Library"),
            DudEdifice("Great Forge"),
            DudEdifice("War Dances"),
            DudEdifice("Monument Trail"),
            DudEdifice("Long Patrol"),
            DudEdifice("Tomb Guardians"),
        ],
    ],
    "Order": [
        [
            BaseDenizen("Wrestlers"),
            BaseDenizen("Battle Honors"),
            BaseDenizen("Bear Traps"),
            BaseDenizen("Longbows"),
            RevisedDenizen("Keep"),
            BaseDenizen("Pressgangs"),
            BaseDenizen("Garrison"),
            BaseDenizen("Scouts"),
            RevisedDenizen("Martial Culture"),
            BaseDenizen("Code of Honor"),
        ],
        [
            BaseDenizen("Outriders"),
            BaseDenizen("Messenger"),
            BaseDenizen("Field Promotion"),
            BaseDenizen("Palanquin"),
            BaseDenizen("Shield Wall"),
            BaseDenizen("Military Parade"),
            DeletedDenizen("Tome Guardians"),
            BaseDenizen("Tyrant"),
            BaseDenizen("Forced Labor"),
            BaseDenizen("Secret Police"),
        ],
        [
            BaseDenizen("Specialist"),
            BaseDenizen("Captains"),
            BaseDenizen("Siege Engines"),
            BaseDenizen("Royal Tax"),
            BaseDenizen("Toll Roads"),
            BaseDenizen("Curfew"),
            BaseDenizen("Knights Errant"),
            BaseDenizen("Vow of Obedience"),
            BaseDenizen("Hunting Party"),
            BaseDenizen("Council Seat"),
        ],
        [
            BaseDenizen("Encirclement"),
            BaseDenizen("Peace Envoy"),
            BaseDenizen("Relic Hunter"),
            NFDenizen("Master at Arms"),
            NFDenizen("Baron"),
            NFDenizen("Honor Guard"),
            NFDenizen("City Wall"),
            NFDenizen("Fearsome General"),
            NFDenizen("Careful Plans"),
            NFDenizen("Garrison Armory"),
        ],
        [
            NFDenizen("Battle Axes"),
            NFDenizen("Great Feast"),
            NFDenizen("Quartermaster"),
            DudEdifice("Sprawling Ramparts"),
            DudEdifice("Grand Canal"),
            DudEdifice("The Tribunal"),
            DudEdifice("Harbor Doors"),
            DudEdifice("Proving Grounds"),
        ],
    ],
    "Discord": [
        [
            BaseDenizen("Mercenaries"),
            BaseDenizen("A Small Favor"),
            BaseDenizen("Second Wind"),
            BaseDenizen("Sleight of Hand"),
            BaseDenizen("Key to the City"),
            BaseDenizen("Sewer"),
            RevisedDenizen("Disgraced Captain"),
            BaseDenizen("Naysayers"),
            RevisedDenizen("Book Burning"),
            BaseDenizen("Charlatan"),
        ],
        [
            BaseDenizen("Assassin"),
            BaseDenizen("Downtrodden"),
            BaseDenizen("Blackmail"),
            BaseDenizen("Cracked Sage"),
            BaseDenizen("Dissent"),
            BaseDenizen("False Prophet"),
            RevisedDenizen("Vow of Division"),
            BaseDenizen("Zealots"),
            RevisedDenizen("Royal Ambitions"),
            RevisedDenizen("Salt the Earth"),
        ],
        [
            BaseDenizen("Beast Tamer"),
            RevisedDenizen("Riots"),
            BaseDenizen("Silver Tongue"),
            BaseDenizen("Gambling Hall"),
            DeletedDenizen("Boiling Lake"),
            RevisedDenizen("Relic Thief"),
            BaseDenizen("Enchantress"),
            BaseDenizen("Insomnia"),
            BaseDenizen("Sneak Attack"),
            RevisedDenizen("Gossip"),
        ],
        [
            RevisedDenizen("Bandit Chief"),
            BaseDenizen("Chaos Cult"),
            RevisedDenizen("Defame"),
            NFDenizen("Bandit Paymaster"),
            NFDenizen("Reliquary Raid"),
            NFDenizen("Tracker"),
            NFDenizen("Banner Breakers"),
            NFDenizen("Pledge to Discard"),
            NFDenizen("Familiar Friar"),
            NFDenizen("Unstable Summons"),
        ],
        [
            NFDenizen("Bandit Prince"),
            NFDenizen("Dark Enforcer"),
            NFDenizen("Spoiled Supplies"),
            DudEdifice("Festival District"),
            DudEdifice("Spied Cards"),
            DudEdifice("Coliseum"),
            DudEdifice("Drowning Spell"),
            DudEdifice("Loosening Tower"),
        ],
    ],
}
