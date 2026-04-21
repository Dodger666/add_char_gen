# OSRIC Character Generator — Magical Items Specification (DMG Appendix P)

**Version**: 1.0.0
**Date**: 2025-04-21
**Status**: Draft
**Source**: AD&D Dungeon Master's Guide, Appendix P: Creating a Party on the Spur of the Moment, pages 225–228

---

## 1. Executive Summary

Characters of level 2+ have a chance to possess magical items reflecting prior adventuring. This specification implements the DMG Appendix P tables: Protective Items, Scrolls, Weapons, Potions, and Miscellaneous Items. Each item has a per-level percentage chance of being owned; the generator rolls against these tables and adds any won items to the character sheet. Equipment purchasing (mundane gear, armor, weapons) is unchanged. Magical items are determined **after** mundane equipment and are **added** to the character's inventory. Only level 2+ characters roll on these tables; level 1 characters get no magical items.

---

## 2. Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| MI-001 | Characters at level 1 receive no magical items | Must |
| MI-002 | Characters at level 2+ roll on Protective Items table | Must |
| MI-003 | Characters at level 2+ roll on Weapons table | Must |
| MI-004 | Characters at level 2+ roll on Potions table | Must |
| MI-005 | Characters at level 2+ roll on Scrolls table | Must |
| MI-006 | Characters at level 6+ (or 9+ for high-level parties) may receive Miscellaneous Items | Should |
| MI-007 | Percentage chance = per_level_chance × character_level | Must |
| MI-008 | Each item has a 1% per level chance of being above average (+2 instead of +1) | Must |
| MI-009 | If chance for having item exceeds 90%, excess above 90% adds to above-average chance | Must |
| MI-010 | Above-average items have a further 1% per level chance of being +3 | Must |
| MI-011 | Magical items must respect class restrictions (e.g., MU cannot have magic plate) | Must |
| MI-012 | For armor/weapons with mutually exclusive options, only one category is tried | Must |
| MI-013 | Magical items appear on the character sheet in a dedicated section | Must |
| MI-014 | Magical armor replaces mundane armor if acquired (better AC) | Should |
| MI-015 | Magical weapons replace mundane weapons of the same type if acquired | Should |
| MI-016 | All magical item rolls use the seeded DiceRoller for determinism | Must |
| MI-017 | PDF character sheet includes magical items | Should |

---

## 3. Core Mechanic

### 3.1 Percentage Chance Formula

```
effective_chance = per_level_chance × level
roll = d100 (1–100)
has_item = roll <= effective_chance
```

If `effective_chance > 100`, the character automatically has the item.

### 3.2 Above-Average Enhancement (+2)

```
above_avg_chance = 1 × level
if effective_chance > 90:
    above_avg_chance += (effective_chance - 90)

roll = d100
is_plus_2 = roll <= above_avg_chance
```

### 3.3 Exceptional Enhancement (+3)

Only checked if item is already +2:

```
exceptional_chance = 1 × level
roll = d100
is_plus_3 = roll <= exceptional_chance
```

### 3.4 Enhancement Summary

| Roll Result | Protective Items | Weapons | Bracers |
|-------------|-----------------|---------|---------|
| Base (+1) | +1 armor/shield | +1 weapon | AC 6 |
| Above avg (+2) | +2 armor/shield | +2 weapon | AC 5 |
| Exceptional (+3) | +3 armor/shield | +3 weapon | AC 4 |

---

## 4. Protective Items Table

### 4.1 Per-Level Chances

| Class | Shield | Plate | Banded | Chain | Leather | Ring of Protection | Bracers |
|-------|--------|-------|--------|-------|---------|--------------------|---------|
| Cleric | 10% | 5%* | 6%* | 8%* | — | 2% | — |
| Druid | — | — | — | — | 8% | 5% | — |
| Fighter | 10% | 6%* | 8%* | 10%* | — | — | — |
| Paladin | 10% | 6%* | 8%* | 10%* | — | — | — |
| Ranger | 8% | 5%* | 7%* | 15%* | — | — | — |
| Magic-User | — | — | — | — | — | 15% | 4% |
| Illusionist | — | — | — | — | — | 15% | 4% |
| Thief | — | — | — | — | 10% | 4% | — |
| Assassin | 8% | — | — | — | 10% | 3% | — |
| Monk | — | — | — | — | — | — | — |

**\* Mutually exclusive**: The character must choose ONE armor type before rolling. The generator picks the best affordable option by priority (Plate > Banded > Chain), attempting the highest AC armor first. If that roll fails, no fallback to a lesser type — the character chose and lost.

### 4.2 Selection Logic

```
1. If class has mutually exclusive armor options (marked *):
   a. Pick the best armor type (highest AC = Plate first, then Banded, then Chain)
   b. Calculate chance = per_level_pct × level
   c. Roll d100. If success → character has magic armor of that type
   d. If fail → no magic armor (do NOT try the next type)

2. For non-exclusive items (Shield, Leather, Ring of Protection, Bracers):
   a. Roll each independently
   b. Character can have multiple (e.g., magic shield AND ring of protection)

3. Apply above-average / exceptional enhancement rolls to each won item
```

### 4.3 Magic Armor Properties

- Base magic armor is +1 (AC improved by 1 from the mundane version)
- Magic armor has no encumbrance penalty when worn (weight = 0)
- Magic armor movement cap is +30 ft vs mundane equivalent
- +2 armor improves AC by 2, +3 by 3, etc.
- Bracers of AC 6 [14] set AC to 6 (or better if already better). AC 5 [15] for +2, AC 4 [16] for +3.
- Ring of Protection +1: -1 AC [+1] and +1 to all saving throws. +2/+3 scale accordingly.
- Magic shield is +1 (additional -1 AC [+1] beyond mundane shield bonus)

### 4.4 Magic Armor AC Calculation

```
magic_plate_+1:   AC 2 [18] (base plate 3 [17], +1 magic)
magic_banded_+1:  AC 3 [17] (base banded 4 [16], +1 magic)
magic_chain_+1:   AC 4 [16] (base chain 5 [15], +1 magic)
magic_leather_+1: AC 7 [13] (base leather 8 [12], +1 magic)
magic_shield_+1:  extra -1 [+1] AC on top of mundane shield
```

---

## 5. Weapons Table

### 5.1 Per-Level Chances

| Class | Dagger | Sword | Mace | Battle Axe | Spear | Bow | 15 Bolts +2 |
|-------|--------|-------|------|------------|-------|-----|-------------|
| Cleric | — | — | 12% | — | — | — | — |
| Druid | 10% | 7%† | — | — | 10% | — | — |
| Fighter | 10% | 10%* | — | 7%* | 8%* | 1% | 10%* |
| Paladin | 10% | 10%* | — | 10%* | 10%* | — | — |
| Ranger | 10% | 9%* | — | 9%* | 8%* | 5% | 10%* |
| Magic-User | 15% | — | — | — | — | — | — |
| Illusionist | 15% | — | — | — | — | — | — |
| Thief | 12% | 11% | — | — | — | — | — |
| Assassin | 10% | 5%* | 5%* | 5%* | 5%* | — | 1% |
| Monk | 5% | — | — | — | 2% | — | — |

**\* Mutually exclusive**: Among starred weapon categories, only ONE may be attempted (Sword, Battle Axe, Spear, or 15 Bolts +2). Generator picks by priority: Sword > Battle Axe > Spear > Bolts.

**† Druid swords are Scimitars.**

### 5.2 Sword Type Rules

- Characters under 5 ft tall: Short Sword
- All other characters: Long Sword (may opt for Short Sword)
- Druids: Scimitar
- Generator always picks Long Sword for medium+ characters, Short Sword for small ancestries

### 5.3 Selection Logic

```
1. For non-exclusive weapons (Dagger, and any non-starred entry):
   - Roll each independently

2. For mutually exclusive weapons (starred *):
   - Pick one category by priority: Sword > Battle Axe > Spear > Bolts
   - Roll for that one only

3. Apply above-average / exceptional enhancement to each won weapon
   - +2 weapon: as per enhancement rules
   - +3 weapon: for swords, may substitute special feature
     (e.g., Flame Tongue, Giant Slayer) — implementation: keep as +3
   - +3 Bolts: instead give Crossbow of Speed + double bolt quantity (30 bolts +2)

4. Bow: if won, also give 20 arrows (mundane) unless bolts are also present
```

### 5.4 Magic Weapon Properties

- +1 weapon: +1 to hit and +1 damage
- +2 weapon: +2 to hit and +2 damage
- +3 weapon: +3 to hit and +3 damage
- Magic weapons have no weight change from mundane
- 15 Bolts +2 are ammunition, not a weapon — they accompany a crossbow

---

## 6. Potions Table

### 6.1 Per-Level Chances and Maximums

| Class | Per Level Chance | Max Potions |
|-------|-----------------|-------------|
| Cleric | 6% | 1 |
| Druid | 11% | 2 |
| Fighter | 8% | 1 |
| Paladin | 6% | 1 |
| Ranger | 7% | 1 |
| Magic-User | 10% | 3 |
| Illusionist | 10% | 2 |
| Thief | 9% | 2 |
| Assassin | 5% | 1 |
| Monk | — | 0 |

### 6.2 Potion Types (d10)

| Roll | Potion |
|------|--------|
| 1 | Climbing |
| 2 | Diminution |
| 3 | Extra-healing |
| 4 | Fire Resistance |
| 5 | Flying |
| 6 | Gaseous Form |
| 7 | Growth |
| 8 | Healing |
| 9 | Invisibility |
| 0 | Polymorph Self |

### 6.3 Selection Logic

```
1. Calculate chance = per_level_chance × level
2. Roll d100. If success → character has 1 potion
3. If max_potions > 1, roll again for each additional potion
   (same chance, up to max_potions total)
4. For each potion won, roll d10 on the potion type table
5. If chance >= 100%, character auto-selects (no random roll):
   - Generator picks the most useful: Healing first, then Extra-healing, then Fire Resistance
```

### 6.4 Potion Properties

Potions are consumable items. They have no weight (negligible), no cost (already acquired), and a single use.

---

## 7. Scrolls Table

### 7.1 Per-Level Chances

| Class | Per Level Chance | Protection | 1 Spell (levels) | 3 Spells (levels) |
|-------|-----------------|------------|-------------------|-------------------|
| Cleric | 8% | No | 1–3 | 1–4 |
| Druid | 7% | Yes | 1–3 | 1–4 |
| Fighter | 6% | Yes | — | — |
| Paladin | 4% | Yes | — | — |
| Ranger | 5% | Yes | — | — |
| Magic-User | 15% | No | 1–4 | 1–6 |
| Illusionist | 12% | No | 1–3 | 1–4 |
| Thief | 6% | Yes | 1–3 | 1–4 |
| Assassin | 3% | Yes | 1–3 | — |
| Monk | — | — | — | — |

### 7.2 Scroll Type Determination

```
1. Roll d100 against (per_level_chance × level)
2. If success, determine scroll type:
   a. If class has "Protection = Yes" and no spell scroll ability: Protection scroll
   b. If class has spell scroll ability:
      - 50% chance: 1 spell scroll (random spell of level within range)
      - 50% chance: 3 spell scroll (random spells of levels within range)
      - If character already has another scroll type, prefer the other kind
   c. If class has "Protection = No" (casters): always spell scroll
      - 50/50 between 1-spell and 3-spell
   d. Thief/Assassin spell scrolls contain Magic-User spells
3. Protection scrolls: pick randomly from [Protection from Demons,
   Protection from Devils, Protection from Elementals, Protection from
   Lycanthropes, Protection from Magic, Protection from Undead]
```

### 7.3 Spell Level Ranges

When generating spell scrolls, each spell's level is rolled randomly within the class range:

- "1–3" means each spell is randomly level 1, 2, or 3
- "1–4" means each spell is randomly level 1, 2, 3, or 4
- "1–6" means each spell is randomly level 1 through 6

The actual spell is picked randomly from the class's spell list for that level (using `SPELL_LISTS` data).

---

## 8. Miscellaneous Items

### 8.1 Eligibility

Miscellaneous items are awarded only to higher-level parties:
- Party generally above level 5 going into hazardous areas, OR
- Party generally above level 8

**Generator rule**: Award miscellaneous items when `level >= 6`.

### 8.2 Number of Items

- 1 item at levels 6–8
- 2 items at levels 9–12
- 3 items at levels 13–16
- 4 items at levels 17–20

### 8.3 Item Table (d16 or pick)

| Roll | Item |
|------|------|
| 1 | Ring of Feather Falling |
| 2 | Ring of Warmth |
| 3 | Ring of Water Walking |
| 4 | Wand of Negation |
| 5 | Wand of Wonder |
| 6 | Bag of Holding (500 lb capacity) |
| 7 | Folding Boat (small rowboat) |
| 8 | Brooch of Shielding |
| 9 | Cloak and Boots of Elvenkind |
| 10 | Javelin of Lightning (pair) |
| 11 | Javelin of Piercing (pair) |
| 12 | Necklace of Adaptation |
| 13 | Robe of Useful Items |
| 14 | Rope of Climbing |
| 15 | Trident of Warning |
| 16 | Wings of Flying |

### 8.4 Selection Logic

```
1. Determine number of items based on level
2. For each item slot, roll d16 (or 1d20 rerolling 17–20) on the table
3. No duplicates — reroll if already awarded
4. Add items to character's magical items list
```

---

## 9. Data Model Changes

### 9.1 New Model: `MagicalItem`

```python
class MagicalItem(BaseModel):
    name: str                          # "Chain Mail +1", "Potion of Healing"
    item_type: str                     # "armor", "shield", "weapon", "potion", "scroll", "ring", "miscellaneous"
    bonus: int | None = None           # +1, +2, +3 or None for non-plus items
    properties: dict[str, Any] = {}    # Additional properties (AC value, damage bonus, spell list, etc.)
    equipped: bool = False             # Whether the item is equipped/worn
    replaces_mundane: str | None = None  # Name of mundane item this replaces (e.g., "Chain Mail")
```

### 9.2 CharacterSheet Additions

```python
class CharacterSheet(BaseModel):
    # ... existing fields ...
    magical_items: list[MagicalItem] = []   # All magical items from Appendix P
```

### 9.3 JSON Response Changes

The `magical_items` list appears in the character JSON:

```json
{
  "character": {
    "magical_items": [
      {
        "name": "Chain Mail +2",
        "item_type": "armor",
        "bonus": 2,
        "properties": {"ac_desc": 3, "ac_asc": 17, "movement_cap": 120},
        "equipped": true,
        "replaces_mundane": "Chain Mail"
      },
      {
        "name": "Potion of Healing",
        "item_type": "potion",
        "bonus": null,
        "properties": {"effect": "Restores 1d8+1 HP"},
        "equipped": false,
        "replaces_mundane": null
      }
    ]
  }
}
```

---

## 10. Implementation Architecture

### 10.1 New Domain Component: `MagicalItemGenerator`

```
src/osric_character_gen/domain/magical_item_generator.py
```

Single class `MagicalItemGenerator` with:
- `__init__(self, roller: DiceRoller)` — seeded randomness
- `generate_magical_items(self, class_name, level, ancestry) -> list[MagicalItem]`
  - Returns empty list if level < 2
  - Calls internal methods for each table
- `_roll_protective_items(self, class_name, level) -> list[MagicalItem]`
- `_roll_weapons(self, class_name, level, ancestry) -> list[MagicalItem]`
- `_roll_potions(self, class_name, level) -> list[MagicalItem]`
- `_roll_scrolls(self, class_name, level) -> list[MagicalItem]`
- `_roll_miscellaneous(self, level) -> list[MagicalItem]`
- `_roll_enhancement(self, level, effective_chance) -> int` — returns 1, 2, or 3

### 10.2 New Data Module: `magical_items.py`

```
src/osric_character_gen/data/magical_items.py
```

Contains all Appendix P tables as Python dicts:

```python
PROTECTIVE_ITEMS_TABLE: dict[ClassName, dict[str, float]]
WEAPONS_TABLE: dict[ClassName, dict[str, float]]
POTIONS_TABLE: dict[ClassName, tuple[float, int]]  # (per_level_pct, max_potions)
SCROLLS_TABLE: dict[ClassName, dict[str, Any]]
MISCELLANEOUS_ITEMS: list[str]
POTION_TYPES: list[str]
PROTECTION_SCROLL_TYPES: list[str]
```

### 10.3 Service Integration

In `CharacterGeneratorService.generate()`, after mundane equipment purchase:

```python
# After step 13 (mundane equipment purchase)
# Step 13b: Magical items (level 2+ only)
if effective_level >= 2:
    magic_gen = MagicalItemGenerator(roller)
    magical_items = magic_gen.generate_magical_items(class_name, effective_level, ancestry)
    # Replace mundane equipment where magical version is better
    loadout = self._apply_magical_upgrades(loadout, magical_items)
```

### 10.4 Mundane Replacement Logic

When magical armor or weapons are won:

```
1. Magic armor replaces mundane armor if:
   - Magic armor provides better AC
   - Character already has mundane armor of any type

2. Magic weapon replaces the mundane weapon of the same category:
   - Magic sword replaces mundane sword
   - Magic dagger replaces mundane dagger
   - If no matching mundane weapon, add the magic weapon

3. Magic shield replaces mundane shield

4. Recalculate AC after replacements:
   - Use magic armor AC (if any)
   - Add magic shield bonus (if any)
   - Add Ring of Protection bonus (if any)
   - Add DEX modifier
   - Bracers: use bracers AC if better than armor AC (they don't stack)

5. Potions, scrolls, misc items are added (no replacement)
```

---

## 11. AC Recalculation with Magic Items

### 11.1 Priority Rules

```
Final AC = best of:
  Option A: magic_armor_ac + magic_shield_bonus + ring_bonus + dex_adj
  Option B: bracers_ac + ring_bonus + dex_adj  (bracers don't stack with armor)
  Option C: base_10 + mundane_armor + mundane_shield + ring_bonus + dex_adj

Ring of Protection stacks with everything.
Bracers do NOT stack with any armor (use whichever is better).
Magic shield stacks with magic armor.
```

### 11.2 Saving Throw Bonus

Ring of Protection provides its bonus to ALL saving throws:
- +1 Ring: +1 to all saves
- +2 Ring: +2 to all saves
- +3 Ring: +3 to all saves

This modifies the character's saving throws after normal calculation.

---

## 12. Integration with Existing Systems

### 12.1 What Changes

| Component | Change |
|-----------|--------|
| `models/character.py` | Add `MagicalItem` model and `magical_items` field to `CharacterSheet` |
| `services/character_generator.py` | Call `MagicalItemGenerator` after mundane equipment, apply upgrades |
| `domain/stats_calculator.py` | AC recalculation method that accounts for magic items |
| `api/v1/endpoints/characters.py` | No change (level already passed through) |
| `api/v1/endpoints/frontend.py` | Add magical items display section |
| `domain/pdf_sheet_generator.py` | Include magical items on PDF sheet |

### 12.2 What Does NOT Change

- Ability score generation
- Class/ancestry selection
- Mundane equipment purchasing logic (still runs first)
- Hit point rolling
- Spell selection
- Thief skills, turn undead, THAC0, saving throws (base values)
- Starting gold rolling
- Physical characteristics

---

## 13. Test Plan

### 13.1 Data Table Tests (`test_data/test_magical_items_tables.py`)

| Test | Description |
|------|-------------|
| test_all_classes_have_protective_entries | Every ClassName has an entry in PROTECTIVE_ITEMS_TABLE |
| test_all_classes_have_weapons_entries | Every ClassName has an entry in WEAPONS_TABLE |
| test_all_classes_have_potions_entries | Every ClassName has an entry in POTIONS_TABLE |
| test_all_classes_have_scrolls_entries | Every ClassName has an entry in SCROLLS_TABLE |
| test_percentages_are_valid | All per-level percentages are 0–20% range |
| test_potion_types_count | 10 potion types |
| test_miscellaneous_items_count | 16 miscellaneous items |

### 13.2 Domain Logic Tests (`test_domain/test_magical_item_generator.py`)

| Test | Description |
|------|-------------|
| test_level_1_no_items | Level 1 characters get empty list |
| test_level_2_can_have_items | Level 2+ may produce items |
| test_deterministic_with_seed | Same seed + level + class → same items |
| test_fighter_can_get_magic_plate | Fighter rolls on plate armor |
| test_magic_user_gets_ring_or_bracers | MU rolls Ring of Protection and Bracers |
| test_thief_no_heavy_armor | Thief never gets plate/chain/banded |
| test_enhancement_scales_with_level | Higher levels have better chance of +2/+3 |
| test_mutual_exclusion_armor | Only one armor type attempted for starred entries |
| test_mutual_exclusion_weapons | Only one weapon type attempted for starred entries |
| test_potion_max_respected | Never exceeds max potions for class |
| test_scroll_spell_levels_in_range | Scroll spells are within the class's level range |
| test_miscellaneous_at_level_6 | Level 6+ gets miscellaneous items |
| test_no_miscellaneous_below_6 | Level 5 and below gets no miscellaneous items |
| test_miscellaneous_no_duplicates | No duplicate miscellaneous items |
| test_monk_no_protective_items | Monk has no entries in protective table |
| test_monk_no_potions | Monk has no potion chance |
| test_druid_sword_is_scimitar | Druid sword type is always scimitar |
| test_small_ancestry_short_sword | Halfling/gnome/dwarf get short sword |
| test_above_average_enhancement | Test the +2 upgrade mechanic |
| test_overflow_above_90_adds_to_enhancement | Chance above 90% boosts +2 chance |

### 13.3 Service Integration Tests (`test_services/test_character_generator.py`)

| Test | Description |
|------|-------------|
| test_level_1_no_magical_items | Level 1 character has empty magical_items |
| test_level_5_may_have_items | Level 5 characters can have magical items |
| test_level_10_likely_has_items | Level 10 characters across many seeds have some items |
| test_magical_armor_replaces_mundane | Magic armor replaces mundane in equipment list |
| test_ac_reflects_magic_items | AC calculation includes magic armor/shield/ring |
| test_ring_of_protection_modifies_saves | Ring bonus applied to saving throws |
| test_deterministic_magical_items | Seed determinism includes magical items |

### 13.4 API Tests (`test_api/test_characters_endpoint.py`)

| Test | Description |
|------|-------------|
| test_level_5_response_has_magical_items_field | JSON includes `magical_items` array |
| test_level_1_magical_items_empty | Level 1 has empty array |

---

## 14. Implementation Phases

### Phase 1: Data Tables
1. Create `src/osric_character_gen/data/magical_items.py` with all Appendix P tables
2. Write table integrity tests
3. Run tests (green)

### Phase 2: Domain Logic
1. Write `MagicalItemGenerator` tests (red)
2. Create `src/osric_character_gen/domain/magical_item_generator.py`
3. Implement all five table rollers + enhancement logic
4. Run tests (green)

### Phase 3: Model & Service Integration
1. Add `MagicalItem` to `models/character.py`
2. Add `magical_items` field to `CharacterSheet`
3. Write service integration tests (red)
4. Update `CharacterGeneratorService.generate()` to call `MagicalItemGenerator`
5. Implement mundane replacement and AC recalculation
6. Run tests (green)

### Phase 4: Frontend & PDF
1. Add magical items display section to frontend HTML
2. Update PDF generator to include magical items
3. Run all tests + ruff

---

## 15. Worked Example

**Gonzo, 9th-level Ranger (Human)**

**Protective Items** (mutually exclusive armor — picks Chain at 15%):
- Chance for Chain Mail: 15% × 9 = 135% → automatic.
- Above-average chance: 9% (base) + 45% (overflow above 90%) = 54% → rolls 51 → +2 Chain Mail
- Exceptional chance: 9% → rolls 99 → stays at +2
- Shield chance: 8% × 9 = 72% → rolls 68 → +1 Shield
- **Result**: Chain Mail +2, Shield +1

**Weapons** (mutually exclusive among Sword/Axe/Spear/Bolts — picks Sword at 9%):
- Dagger chance: 10% × 9 = 90% → rolls 45 → +1 Dagger
- Sword chance: 9% × 9 = 81% → rolls 70 → +1 Long Sword
- Bow chance: 5% × 9 = 45% → rolls 80 → no bow
- **Result**: Dagger +1, Long Sword +1

**Potions** (7% per level, max 1):
- Chance: 7% × 9 = 63% → rolls 50 → 1 potion
- Type: rolls d10 = 5 → Potion of Flying
- **Result**: Potion of Flying

**Scrolls** (5% per level):
- Chance: 5% × 9 = 45% → rolls 60 → no scroll

**Miscellaneous** (level 9 → 2 items):
- Rolls d16 = 6 → Bag of Holding
- Rolls d16 = 14 → Rope of Climbing
- **Result**: Bag of Holding, Rope of Climbing

---

## 16. Assumptions

| # | Assumption | Rationale |
|---|-----------|-----------|
| A1 | Monk receives no items from any Appendix P table | DMG shows no entries for Monk in Protective/Potions tables, minimal in Weapons |
| A2 | "Mutually exclusive" armor selection uses priority Plate > Banded > Chain | Higher AC armor is more desirable; DMG says "character must make a decision" |
| A3 | "Mutually exclusive" weapon selection uses priority Sword > Battle Axe > Spear > Bolts | Swords are the most versatile weapon type |
| A4 | Miscellaneous item count scales linearly: 1 at 6–8, 2 at 9–12, 3 at 13–16, 4 at 17–20 | DMG says "one to four" without precise breakpoints; this is a reasonable gradient |
| A5 | Potion auto-select (>= 100% chance) picks Healing > Extra-healing > Fire Resistance | DMG says character "would have supplies available to choose from"; these are most universally useful |
| A6 | Magic armor weight is 0 when worn | Per OSRIC rule: "Magic armor: no weight penalty when worn" |
| A7 | +3 weapons are kept as +3 (no special sword subtypes like Flame Tongue) | Simplification; special sword types would require additional tables and mechanics |
| A8 | +3 Bolts scenario gives Crossbow of Speed + 30 bolts +2 | Direct from DMG: "Add a crossbow of speed to +2 bolts if a +3 is indicated, otherwise double their number only" |
| A9 | Protection scrolls use a fixed list of 6 types | Standard AD&D protection scroll types |
| A10 | Bracers and armor don't stack; use whichever gives better AC | Standard AD&D rule |
