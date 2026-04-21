from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class Alignment(StrEnum):
    LG = "Lawful Good"
    NG = "Neutral Good"
    CG = "Chaotic Good"
    LN = "Lawful Neutral"
    TN = "True Neutral"
    CN = "Chaotic Neutral"
    LE = "Lawful Evil"
    NE = "Neutral Evil"
    CE = "Chaotic Evil"


class AncestryName(StrEnum):
    DWARF = "Dwarf"
    ELF = "Elf"
    GNOME = "Gnome"
    HALF_ELF = "Half-Elf"
    HALF_ORC = "Half-Orc"
    HALFLING = "Halfling"
    HUMAN = "Human"


class ClassName(StrEnum):
    ASSASSIN = "Assassin"
    CLERIC = "Cleric"
    DRUID = "Druid"
    FIGHTER = "Fighter"
    ILLUSIONIST = "Illusionist"
    MAGIC_USER = "Magic-User"
    MONK = "Monk"
    PALADIN = "Paladin"
    RANGER = "Ranger"
    THIEF = "Thief"


class Gender(StrEnum):
    MALE = "Male"
    FEMALE = "Female"


class AbilityScores(BaseModel):
    strength: int = Field(ge=1, le=25)
    dexterity: int = Field(ge=1, le=25)
    constitution: int = Field(ge=1, le=25)
    intelligence: int = Field(ge=1, le=25)
    wisdom: int = Field(ge=1, le=25)
    charisma: int = Field(ge=1, le=25)
    exceptional_strength: int | None = Field(
        default=None,
        ge=1,
        le=100,
        description="Only for Fighter/Paladin/Ranger with STR 18",
    )


class AbilityBonuses(BaseModel):
    str_to_hit: int = 0
    str_damage: int = 0
    str_encumbrance: int = 0
    str_minor_test: str = "—"
    str_major_test: str = "—"
    dex_surprise: int = 0
    dex_missile_to_hit: int = 0
    dex_ac_adj: int = 0
    dex_initiative: int = 0
    con_hp_mod: int = 0
    con_resurrection: int = 0
    con_system_shock: int = 0
    int_max_languages: int = 0
    wis_mental_save: int = 0
    wis_bonus_spells: list[dict[str, int]] = Field(default_factory=list)
    cha_sidekick_limit: int = 4
    cha_loyalty_mod: int = 0
    cha_reaction_mod: int = 0


class SavingThrows(BaseModel):
    aimed_magic_items: int
    breath_weapons: int
    death_paralysis_poison: int
    petrifaction_polymorph: int
    spells: int


class EquipmentItem(BaseModel):
    name: str
    weight: float
    cost_gp: float
    equipped: bool = False
    notes: str = ""


class WeaponItem(BaseModel):
    name: str
    damage_vs_sm: str
    damage_vs_l: str
    weight: float
    cost_gp: float
    hands: int = 1
    to_hit_modifier: int = 0
    damage_modifier: int = 0
    is_proficient: bool = True
    weapon_type: str = "melee"


class ArmorItem(BaseModel):
    name: str
    ac_desc: int
    ac_asc: int
    weight: float
    cost_gp: float
    movement_cap: int


class ThiefSkills(BaseModel):
    climb: int = Field(ge=1, le=99)
    hide: int = Field(ge=1, le=99)
    listen: int = Field(ge=1, le=99)
    pick_locks: int = Field(ge=1, le=99)
    pick_pockets: int = Field(ge=1, le=99)
    read_languages: int = Field(ge=1, le=99)
    move_quietly: int = Field(ge=1, le=99)
    traps: int = Field(ge=1, le=99)


class TurnUndeadEntry(BaseModel):
    undead_type: str
    example: str
    roll_needed: int | str


class SpellSlots(BaseModel):
    level_1: int = 0
    level_2: int = 0
    level_3: int = 0
    level_4: int = 0
    level_5: int = 0
    level_6: int = 0
    level_7: int = 0


class PhysicalCharacteristics(BaseModel):
    height_inches: int
    height_display: str
    weight_lbs: int
    age: int
    age_category: str
    gender: Gender


class MagicalItem(BaseModel):
    name: str
    item_type: str  # "armor", "shield", "weapon", "potion", "scroll", "ring", "miscellaneous", "ammunition"
    bonus: int | None = None
    properties: dict[str, Any] = Field(default_factory=dict)
    equipped: bool = False
    replaces_mundane: str | None = None


class CharacterSheet(BaseModel):
    name: str = "Unnamed Adventurer"
    character_class: ClassName
    level: int = 1
    alignment: Alignment
    ancestry: AncestryName
    xp: int = 0
    xp_bonus_pct: int = 0

    hit_points: int = Field(ge=1)
    armor_class_desc: int
    armor_class_asc: int

    physical: PhysicalCharacteristics

    ability_scores: AbilityScores
    ability_bonuses: AbilityBonuses

    thac0: int
    bthb: int
    saving_throws: SavingThrows
    melee_to_hit_mod: int
    missile_to_hit_mod: int

    armor: ArmorItem | None = None
    shield: EquipmentItem | None = None
    weapons: list[WeaponItem] = Field(default_factory=list)
    equipment: list[EquipmentItem] = Field(default_factory=list)
    gold_remaining: float

    total_weight_lbs: float
    encumbrance_allowance: int
    encumbrance_status: str
    base_movement: int
    effective_movement: int

    thief_skills: ThiefSkills | None = None
    turn_undead: list[TurnUndeadEntry] | None = None
    spell_slots: SpellSlots | None = None
    spells_memorized: list[str] | None = None
    spellbook: list[str] | None = None

    ancestry_features: list[str] = Field(default_factory=list)
    class_features: list[str] = Field(default_factory=list)
    weapon_proficiencies: list[str] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)
    magical_items: list[MagicalItem] = Field(default_factory=list)

    generation_seed: int | None = None
    dice_rolls: dict | None = None
