# OSRIC 3.0 Character Generator — Game Data Reference

**Version**: 1.0.0
**Date**: 2025-07-12
**Status**: Draft

This document contains all OSRIC 3.0 game rule data required for implementation, extracted directly from the OSRIC 3.0 Player Guide PDF.

---

## 1. Ability Score Bonus Tables

### 1.1 Strength

| STR | To-Hit | Damage | Encumbrance (lbs) | Minor Test | Major Test |
|-----|--------|--------|-------------------|------------|------------|
| 3 | -3 | -1 | 0 | — | — |
| 4–5 | -2 | -1 | 10 | — | — |
| 6–7 | -1 | 0 | 20 | — | — |
| 8–9 | 0 | 0 | 35 | — | — |
| 10–11 | 0 | 0 | 35 | — | — |
| 12–13 | 0 | 0 | 45 | — | — |
| 14–15 | 0 | 0 | 55 | — | — |
| 16 | 0 | +1 | 70 | — | — |
| 17 | +1 | +1 | 85 | — | — |
| 18 | +1 | +2 | 110 | — | — |
| 18.01–50 | +1 | +3 | 135 | — | — |
| 18.51–75 | +2 | +3 | 160 | — | — |
| 18.76–90 | +2 | +4 | 185 | — | — |
| 18.91–99 | +2 | +5 | 235 | — | — |
| 18.00/19 | +3 | +6 | 300 | — | — |

### 1.2 Dexterity

| DEX | Surprise | Missile To-Hit | Init (Missile) | AC Adj Desc | AC Adj Asc | Agility Save |
|-----|----------|----------------|----------------|-------------|------------|--------------|
| 3 | -3 | -3 | +3 | +4 | -4 | -4 |
| 4 | -2 | -2 | +2 | +3 | -3 | -3 |
| 5 | -1 | -1 | +1 | +2 | -2 | -2 |
| 6 | 0 | 0 | 0 | +1 | -1 | -1 |
| 7–14 | 0 | 0 | 0 | 0 | 0 | 0 |
| 15 | 0 | 0 | 0 | -1 | +1 | +1 |
| 16 | +1 | +1 | -1 | -2 | +2 | +2 |
| 17 | +2 | +2 | -2 | -3 | +3 | +3 |
| 18 | +3 | +3 | -3 | -4 | +4 | +4 |
| 19 | +3 | +3 | -3 | -4 | +4 | +4 |

### 1.3 Constitution

| CON | HP Mod (Non-Fighter) | HP Mod (Fighter) | Resurrection % | System Shock % |
|-----|---------------------|-------------------|----------------|----------------|
| 3 | -2 | -2 | 40 | 35 |
| 4 | -1 | -1 | 45 | 40 |
| 5 | -1 | -1 | 50 | 45 |
| 6 | -1 | -1 | 55 | 50 |
| 7 | 0 | 0 | 60 | 55 |
| 8 | 0 | 0 | 65 | 60 |
| 9 | 0 | 0 | 70 | 65 |
| 10 | 0 | 0 | 75 | 70 |
| 11 | 0 | 0 | 80 | 75 |
| 12 | 0 | 0 | 85 | 80 |
| 13 | 0 | 0 | 88 | 83 |
| 14 | 0 | 0 | 92 | 88 |
| 15 | +1 | +1 | 94 | 91 |
| 16 | +2 | +2 | 96 | 95 |
| 17 | +2 | +3 | 98 | 97 |
| 18 | +2 | +4 | 100 | 99 |
| 19 | +2 | +5 | 100 | 99 |

Notes:
- "Fighter types" = Fighter, Paladin, Ranger (get higher CON HP bonus at 17+)
- CON 19: all die rolls of 1 are treated as 2 (any class)
- Minimum 1 HP per level even with penalty

### 1.4 Intelligence

| INT | Max Additional Languages |
|-----|------------------------|
| 3–7 | 0 |
| 8–9 | 1 |
| 10–11 | 2 |
| 12–13 | 3 |
| 14–15 | 4 |
| 16 | 5 |
| 17 | 6 |
| 18 | 7 |
| 19 | 8 |

INT 19+: immune to 1st-level illusion spells.

### 1.5 Wisdom

| WIS | Mental Save Modifier |
|-----|---------------------|
| 3 | -3 |
| 4 | -2 |
| 5–7 | -1 |
| 8–14 | 0 |
| 15 | +1 |
| 16 | +2 |
| 17 | +3 |
| 18 | +4 |
| 19 | +5 |

#### Wisdom Bonus Spell Slots (Cleric/Druid only)

| WIS | Bonus |
|-----|-------|
| 13 | +1 first-level slot |
| 14 | +1 first-level slot (total +2 first-level) |
| 15 | +1 second-level slot |
| 16 | +1 second-level slot (total +2 second-level) |
| 17 | +1 third-level slot |
| 18 | +1 fourth-level slot |

### 1.6 Charisma

| CHA | Sidekick Limit | Loyalty Mod | Reaction Mod |
|-----|---------------|-------------|--------------|
| 3 | 1 | -30 | -25 |
| 4 | 1 | -25 | -20 |
| 5 | 2 | -20 | -15 |
| 6 | 2 | -15 | -10 |
| 7 | 3 | -10 | -5 |
| 8 | 3 | -5 | 0 |
| 9–11 | 4 | 0 | 0 |
| 12 | 5 | 0 | 0 |
| 13 | 5 | 0 | +5 |
| 14 | 6 | +5 | +10 |
| 15 | 7 | +15 | +15 |
| 16 | 8 | +20 | +25 |
| 17 | 10 | +30 | +30 |
| 18 | 15 | +40 | +35 |
| 19 | 20 | +50 | +40 |

---

## 2. Class Definitions

### 2.1 Minimum Ability Scores

| Class | STR | DEX | CON | INT | WIS | CHA |
|-------|-----|-----|-----|-----|-----|-----|
| Assassin | 12 | 12 | 6 | 11 | 6 | — |
| Cleric | 6 | — | 6 | 6 | 9 | 6 |
| Druid | 6 | — | 6 | 6 | 12 | 15 |
| Fighter | 9 | 6 | 7 | 3 | 6 | 6 |
| Illusionist | 6 | 16 | — | 15 | 6 | 6 |
| Magic-User | — | 6 | 6 | 9 | 6 | 6 |
| Monk | 10 | 15 | — | — | 10 | — |
| Paladin | 12 | 6 | 9 | 9 | 13 | 17 |
| Ranger | 13 | 6 | 14 | 13 | 14 | 6 |
| Thief | 6 | 9 | 6 | 6 | — | 6 |

Dash (—) = no minimum requirement.

### 2.2 Class Properties

| Class | Hit Die | Max HD Lvl | Alignment | Prime Requisite | XP Bonus Condition | Starting Gold |
|-------|---------|------------|-----------|----------------|-------------------|---------------|
| Assassin | d6 | 15 | LE, NE, CE | None | — | 2d6×10 gp |
| Cleric | d8 | 9 | Any | WIS | WIS ≥ 16 → 10% | 3d6×10 gp |
| Druid | d8 | 14 | TN | WIS + CHA | Both ≥ 16 → 10% | 3d6×10 gp |
| Fighter | d10 | 9 | Any | STR | STR ≥ 16 → 10% | 5d4×10 gp |
| Illusionist | d4 | 10 | Any | None | — | 2d4×10 gp |
| Magic-User | d4 | 10 | Any | INT | INT ≥ 16 → 10% | 2d4×10 gp |
| Monk | d4 | 18 | LG, LN, LE | None | — | 5d4 gp |
| Paladin | d10 | 9 | LG | STR + WIS | Both ≥ 16 → 10% | 5d4×10 gp |
| Ranger | d8 | 11(at L10) | LG, NG, CG | STR + INT + WIS | All ≥ 16 → 10% | 5d4×10 gp |
| Thief | d6 | 10 | LN, TN, CN, LE, NE, CE | DEX | DEX ≥ 16 → 10% | 2d6×10 gp |

Notes:
- Rangers get 2d8 HP at level 1
- Monks get 2d4 HP at level 1

### 2.3 Armor & Weapon Restrictions

| Class | Armor Allowed | Shield | Allowed Weapons |
|-------|--------------|--------|-----------------|
| Assassin | Leather, Studded leather | Yes | Any |
| Cleric | Any | Any | Club, Flail (heavy/light), Warhammer (heavy/light), Mace (heavy/light), Staff, Torch |
| Druid | Leather | Wooden only | Club, Dagger, Dart, Warhammer (light), Scimitar, Sling, Spear, Staff, Torch |
| Fighter | Any | Any | Any |
| Illusionist | None | No | Dagger, Dart, Staff |
| Magic-User | None | No | Dagger, Dart, Staff |
| Monk | None | No | Club, Crossbow (light/heavy), Dagger, Hand axe, Javelin, Pole arm, Spear, Staff |
| Paladin | Any | Any | Any |
| Ranger | Any | Any | Any |
| Thief | Leather, Padded, Studded leather | No | Club, Dagger, Dart, Sling, Long sword, Short sword, Broad sword, Scimitar, Torch |

### 2.4 Weapon Proficiencies

| Class | Starting Slots | Non-Proficiency Penalty |
|-------|---------------|------------------------|
| Assassin | 3 | -3 |
| Cleric | 2 | -3 |
| Druid | 2 | -4 |
| Fighter | 4 | -2 |
| Illusionist | 1 | -5 |
| Magic-User | 1 | -5 |
| Monk | 1 | -3 |
| Paladin | 3 | -2 |
| Ranger | 3 | -2 |
| Thief | 2 | -3 |

### 2.5 Level 1 Spell Slots

| Class | Slots at Level 1 | Spell Type |
|-------|------------------|------------|
| Cleric | 1 first-level (+ WIS bonus) | Divine |
| Druid | 2 first-level (+ WIS bonus) | Druidic |
| Illusionist | 1 first-level | Phantasmal |
| Magic-User | 1 first-level | Arcane |

All other classes: no spellcasting at level 1.

---

## 3. Ancestry Definitions

### 3.1 Ability Score Ranges (After Adjustments)

| Ancestry | STR | DEX | CON | INT | WIS | CHA |
|----------|-----|-----|-----|-----|-----|-----|
| Dwarf | 8–18 | 3–17 | 12–19 | 3–18 | 3–18 | 3–16 |
| Elf | 3–18 | 7–19 | 6–18 | 8–18 | 3–18 | 8–18 |
| Gnome | 6–18 | 3–18 | 8–18 | 7–18 | 3–18 | 3–18 |
| Half-Elf | 3–18 | 6–18 | 6–18 | 4–18 | 3–18 | 3–18 |
| Half-Orc | 6–18 | 3–17 | 13–19 | 3–17 | 3–14 | 3–12 |
| Halfling | 6–17 | 8–18 | 10–19 | 6–18 | 3–17 | 3–18 |
| Human | 3–18 | 3–18 | 3–18 | 3–18 | 3–18 | 3–18 |

### 3.2 Ability Score Adjustments

| Ancestry | STR | DEX | CON | INT | WIS | CHA |
|----------|-----|-----|-----|-----|-----|-----|
| Dwarf | — | — | +1 | — | — | -1 |
| Elf | — | +1 | -1 | — | — | — |
| Gnome | — | — | — | — | — | — |
| Half-Elf | — | — | — | — | — | — |
| Half-Orc | +1 | — | +1 | — | — | -2 |
| Halfling | -1 | +1 | — | — | — | — |
| Human | — | — | — | — | — | — |

### 3.3 Available Classes by Ancestry

| Ancestry | Single Classes | Multi-Classes |
|----------|---------------|---------------|
| Dwarf | Assassin, Cleric, Fighter, Thief | Fighter/Thief |
| Elf | Assassin, Cleric, Fighter, Magic-User, Thief | Fighter/MU, Fighter/Thief, MU/Thief, Fighter/MU/Thief |
| Gnome | Assassin, Cleric, Fighter, Illusionist, Thief | Fighter/Illusionist, Fighter/Thief, Illusionist/Thief |
| Half-Elf | Assassin, Cleric, Druid, Fighter, Magic-User, Ranger, Thief | Cleric/Fighter, Cleric/Ranger, Cleric/MU, Fighter/MU, Fighter/Thief, Cleric/Fighter/MU, Fighter/MU/Thief |
| Half-Orc | Assassin, Cleric, Fighter, Thief | Cleric/Fighter, Cleric/Thief, Cleric/Assassin, Fighter/Thief, Fighter/Assassin |
| Halfling | Fighter, Druid, Thief | Fighter/Thief |
| Human | All 10 single classes | None (dual-class only) |

### 3.4 Physical Characteristics

| Ancestry | Size | Movement | Infravision | Height Formula | Weight Formula |
|----------|------|----------|-------------|----------------|----------------|
| Dwarf | Small | 90 ft | 60 ft | 48 + 3d4 in | 150 + 5d10 lbs |
| Elf | Medium | 120 ft | 60 ft | 54 + 3d4 in | 70 + 5d10 lbs |
| Gnome | Small | 90 ft | 60 ft | 34 + 3d4 in | 45 + 4d10 lbs |
| Half-Elf | Medium | 120 ft | 60 ft | 60 + 4d4 in | 90 + 5d10 lbs |
| Half-Orc | Medium | 120 ft | 60 ft | 66 + 3d4 in | 150 + 5d10 lbs |
| Halfling | Small | 90 ft | 60 ft | 34 + 3d4 in | 45 + 4d10 lbs |
| Human | Medium | 120 ft | None | 64 + 3d4 in | 140 + 6d10 lbs |

### 3.5 Starting Age Formulas

| Ancestry | Cleric | Druid | Fighter | Paladin | Ranger | Magic-User | Illusionist | Monk | Thief | Assassin |
|----------|--------|-------|---------|---------|--------|-----------|-------------|------|-------|----------|
| Dwarf | 250+2d20 | — | 40+5d4 | — | — | — | — | — | 75+3d6 | 75+3d6 |
| Elf | 500+10d10 | — | 130+5d6 | — | — | 150+5d6 | — | — | 100+5d6 | 100+5d6 |
| Gnome | 300+3d12 | — | 60+5d4 | — | — | — | 100+2d12 | — | 80+5d4 | 80+5d4 |
| Half-Elf | 40+2d4 | 40+2d4 | 22+3d4 | — | 22+3d4 | 30+2d8 | — | — | 22+3d8 | 22+3d8 |
| Half-Orc | 20+1d4 | — | 13+1d4 | — | — | — | — | — | 20+2d4 | 20+2d4 |
| Halfling | — | 40+3d4 | 20+3d4 | — | — | — | — | — | 40+2d4 | — |
| Human | 20+1d4 | 20+1d4 | 15+1d4 | 15+1d4 | 15+1d4 | 24+2d8 | 24+2d8 | 20+1d4 | 20+1d4 | 20+1d4 |

Dash (—) = ancestry/class combination not available.

### 3.6 Age Category Thresholds

| Ancestry | Youth < | Adult ≥ | Grizzled ≥ | Elder ≥ | Ancient ≥ |
|----------|---------|---------|------------|---------|-----------|
| Dwarf | 50 | 51 | 150 | 250 | 350 |
| Elf | 175 | 175 | 550 | 875 | 1200 |
| Gnome | 90 | 90 | 300 | 450 | 600 |
| Half-Elf | 40 | 40 | 100 | 175 | 250 |
| Half-Orc | 16 | 16 | 30 | 45 | 60 |
| Halfling | 33 | 33 | 68 | 101 | 144 |
| Human | 20 | 20 | 40 | 60 | 90 |

### 3.7 Age Category Ability Adjustments

| Category | STR | DEX | CON | INT | WIS |
|----------|-----|-----|-----|-----|-----|
| Youth | — | — | +1 | — | -1 |
| Adult | +1 | — | — | — | +1 |
| Grizzled | -1 | — | -1 | +1 | +1 |
| Elder | -2 | -2 | -1 | — | +1 |
| Ancient | -1 | -1 | -1 | +1 | +1 |

### 3.8 Ancestry Features (for character sheet)

**Dwarf**:
- Giant-Slayers: Giants attack at -4 to hit
- Grudge-Bearers: +1 to hit goblins, half-orcs, hobgoblins, orcs
- Stalwart: CON-based save bonus vs poison/spells/magic
- Stone-Kenning: Detect slopes 75%, new construction 75%, sliding walls 65%, traps 50%, depth 50%
- Infravision 60ft

**Elf**:
- Fey Deftness: +1 to hit with bows and short/long swords
- Keen Detection: 1/6 passive concealed/secret; 2/6 active secret, 3/6 active concealed
- Lightfooted: 4-in-6 surprise (light armor, 90ft from non-lightfooted)
- Strength of Will: 90% resist sleep/charm
- Cannot be raised/resurrected
- Infravision 60ft

**Gnome**:
- Ancestral Foes: +1 to hit kobolds and goblins
- Giant-Slayers: Giants attack at -4 to hit
- Stalwart: CON-based save bonus vs poison/spells/magic
- Stone-Kenning: Slopes 80%, unsafe areas 70%, depth 60%, direction 50%
- Infravision 60ft

**Half-Elf**:
- Keen Detection: Active only: 2/6 secret, 3/6 concealed
- Strength of Mind: 30% resist sleep/charm
- Infravision 60ft

**Half-Orc**:
- Infravision 60ft
- Cannot be raised/resurrected

**Halfling**:
- Halfling Marksmanship: +3 to hit with bows/slings
- Lightfooted: 4-in-6 surprise (same conditions as elf)
- Stalwart: CON-based save bonus vs poison/spells/magic
- Infravision 60ft

**Human**:
- No special ancestry features
- Unlimited level advancement (except Assassin 15, Druid 14, Monk 17)
- Eligible for dual-classing

### 3.9 Stalwart Save Bonus (Dwarf/Gnome/Halfling)

Based on CON score:

| CON | Save Bonus |
|-----|-----------|
| 3–4 | +1 |
| 5–6 | +1 |
| 7–8 | +2 |
| 9–10 | +2 |
| 11–13 | +3 |
| 14–17 | +4 |
| 18–19 | +5 |

Applies to saves vs: (1) Aimed magic items, (2) Poison, (3) Spells and magic effects.

---

## 4. Saving Throw Tables (Level 1)

| Class | Level Range | Aimed Magic Items | Breath Weapons | Death/Paralysis/Poison | Petrifaction/Polymorph | Spells |
|-------|------------|-------------------|----------------|----------------------|---------------------|--------|
| Assassin | 1–4 | 14 | 16 | 13 | 12 | 15 |
| Cleric | 1–3 | 14 | 16 | 10 | 13 | 15 |
| Druid | 1–3 | 14 | 16 | 10 | 13 | 15 |
| Fighter | 1–2 | 16 | 17 | 14 | 15 | 17 |
| Illusionist | 1–5 | 11 | 15 | 14 | 13 | 12 |
| Magic-User | 1–5 | 11 | 15 | 14 | 13 | 12 |
| Monk | 1–4 | 14 | 16 | 13 | 12 | 15 |
| Paladin | 1–2 | 14 | 15 | 12 | 13 | 15 |
| Ranger | 1–2 | 16 | 17 | 14 | 15 | 17 |
| Thief | 1–4 | 14 | 16 | 13 | 12 | 15 |

**Modifier**: WIS mental save bonus applies to Spells category.

---

## 5. THAC0 / To-Hit Tables (Level 1)

Using the tables extracted from PDF, level 1 to-hit values for AC 10 through AC 0:

### Cleric (Levels 1–3)
| AC | 10 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
|----|----|----|----|----|----|----|----|----|----|----|-----|
| Roll | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |

**THAC0 = 20, BTHB = 0**

### Druid (Levels 1–3)
Same as Cleric. THAC0 = 20, BTHB = 0.

### Fighter (Levels 1–2)
| AC | 10 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
|----|----|----|----|----|----|----|----|----|----|----|-----|
| Roll | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |

**THAC0 = 20, BTHB = 0**

### Paladin (Level 1)
Same as Fighter. THAC0 = 20, BTHB = 0.

### Ranger (Levels 1–2)
Same as Fighter. THAC0 = 20, BTHB = 0.

### Assassin (Levels 1–4)
| AC | 10 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
|----|----|----|----|----|----|----|----|----|----|----|-----|
| Roll | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 20 |

**THAC0 = 21, BTHB = -1** (needs 21 to hit AC 0, capped at 20 on d20)

### Thief (Levels 1–4)
Same as Assassin. THAC0 = 21, BTHB = -1.

### Monk (Levels 1–3)
| AC | 10 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
|----|----|----|----|----|----|----|----|----|----|----|-----|
| Roll | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 |

**THAC0 = 20, BTHB = 0**

### Magic-User (Levels 1–5)
| AC | 10 | 9 | 8 | 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 |
|----|----|----|----|----|----|----|----|----|----|----|-----|
| Roll | 11 | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 20 |

**THAC0 = 21, BTHB = -1**

### Illusionist (Levels 1–5)
Same as Magic-User. THAC0 = 21, BTHB = -1.

---

## 6. Thief Skills

### 6.1 Base Skills (Level 1)

| Skill | Base % |
|-------|--------|
| Climb | 85 |
| Hide | 10 |
| Listen | 10 |
| Pick Locks | 25 |
| Pick Pockets | 30 |
| Read Languages | 1 |
| Move Quietly | 15 |
| Traps | 20 |

### 6.2 Dexterity Adjustments

| DEX | Climb | Hide | Listen | Pick Locks | Pick Pockets | Move Quietly | Traps | Read Languages |
|-----|-------|------|--------|------------|-------------|-------------|-------|---------------|
| 9 | — | -10 | — | -10 | -15 | -20 | -15 | — |
| 10 | — | -5 | — | -5 | -10 | -15 | -10 | — |
| 11 | — | — | — | — | -5 | -10 | -5 | — |
| 12 | — | — | — | — | — | -5 | — | — |
| 13–15 | — | — | — | — | — | — | — | — |
| 16 | — | — | — | +5 | — | — | — | — |
| 17 | — | +5 | — | +10 | +5 | +5 | +5 | — |
| 18 | — | +10 | — | +15 | +10 | +10 | +10 | — |
| 19 | — | +15 | — | +20 | +15 | +15 | +15 | — |

### 6.3 Ancestry Adjustments

| Ancestry | Climb | Hide | Listen | Pick Locks | Pick Pockets | Move Quietly | Traps | Read Languages |
|----------|-------|------|--------|------------|-------------|-------------|-------|---------------|
| Dwarf | -10 | — | — | +15 | — | -5 | +15 | -5 |
| Elf | -5 | +10 | +5 | -5 | +5 | +5 | +5 | +10 |
| Gnome | -15 | — | +5 | +10 | — | — | — | — |
| Half-Elf | — | +5 | — | — | +10 | — | — | — |
| Halfling | -15 | +15 | +5 | — | +5 | +15 | — | -5 |
| Half-Orc | +5 | — | +5 | +5 | -5 | — | +5 | -10 |
| Human | +5 | — | — | +5 | — | — | — | — |

Minimum for any skill: 1%.

---

## 7. Turn Undead (Cleric Level 1)

| Type | Example | Roll Needed (d20) |
|------|---------|------------------|
| 1 | Skeleton | 10 |
| 2 | Zombie | 13 |
| 3 | Ghoul | 16 |
| 4 | Shadow | 19 |
| 5 | Wight | 20 |
| 6 | Ghast | — |
| 7+ | — | — |

T = automatic turn (2d6 affected), D = automatic destroy (2d6 affected), — = cannot turn.

---

## 8. Equipment Tables

### 8.1 Armor

| Name | AC Desc | AC Asc | Weight (lbs) | Move Cap | Cost (gp) |
|------|---------|--------|-------------|----------|-----------|
| Leather | 8 | 12 | 15 | 120 | 5 |
| Padded | 8 | 12 | 10 | 90 | 4 |
| Studded Leather | 7 | 13 | 20 | 90 | 15 |
| Ring Mail | 7 | 13 | 35 | 90 | 30 |
| Scale/Lamellar | 6 | 14 | 40 | 60 | 45 |
| Chain Mail | 5 | 15 | 30 | 90 | 75 |
| Splint | 4 | 16 | 40 | 60 | 80 |
| Banded | 4 | 16 | 35 | 90 | 90 |
| Plate Mail | 3 | 17 | 45 | 60 | 400 |
| Small Shield | — | — | 5 | — | 10 |
| Medium Shield | — | — | 8 | — | 12 |
| Large Shield | — | — | 10 | — | 15 |

Shield: -1 to AC (descending), +1 to AC (ascending). Blocks 1/2/3 attacks per round (small/medium/large).

### 8.2 Melee Weapons

| Name | Hands | Dmg vs S/M | Dmg vs L+ | Weight (lbs) | Cost (gp) |
|------|-------|-----------|-----------|-------------|-----------|
| Axe, battle | 2 (1 STR15+) | 1d8 | 1d8 | 7 | 5 |
| Axe, hand | 1 | 1d6 | 1d4 | 5 | 1 |
| Club | 1 | 1d6 | 1d3 | 3 | 0.02 |
| Dagger | 1 | 1d4 | 1d3 | 1 | 2 |
| Flail, heavy | 2 (1 STR14+) | 1d6+1 | 2d4 | 10 | 3 |
| Flail, light | 1 | 1d4+1 | 1d4+1 | 4 | 6 |
| Halberd | 2 | 1d10 | 2d6 | 18 | 9 |
| Javelin | 1 | 1d6 | 1d4 | 2 | 0.5 |
| Lance | 1 | 2d4+1 | 3d6 | 15 | 6 |
| Mace, heavy | 2 (1 STR13+) | 1d6+1 | 1d6 | 10 | 10 |
| Mace, light | 1 | 1d4+1 | 1d4+1 | 5 | 4 |
| Morning star | 2 (1 STR16+) | 2d4 | 1d6+1 | 12 | 5 |
| Pick, heavy | 2 (1 STR14+) | 1d6+1 | 2d4 | 1 | 8 |
| Pick, light | 1 | 1d4+1 | 1d4 | 4 | 5 |
| Pole arm | 2 | 1d6+1 | 1d10 | 8 | 6 |
| Spear | 2 or 1 | 1d6 | 1d8 | 5 | 1 |
| Staff | 2 | 1d6 | 1d6 | 5 | 0 |
| Sword, bastard | 2 (1 STR15+) | 2d4 | 2d8 | 10 | 25 |
| Sword, broad | 2 (1 STR12+) | 2d4 | 1d6+1 | 8 | 15 |
| Sword, long | 1 | 1d8 | 1d12 | 7 | 15 |
| Sword, scimitar | 1 | 1d8 | 1d8 | 5 | 15 |
| Sword, short | 1 | 1d6 | 1d8 | 3 | 8 |
| Sword, two-handed | 2 | 1d10 | 3d6 | 25 | 30 |
| Torch | 1 | 1d4 | 1d4 | 1 | 0.01 |
| Trident | 2 (1 STR14+) | 1d6+1 | 3d4 | 5 | 4 |
| Warhammer, heavy | 2 (1 STR15+) | 1d6+1 | 1d6 | 10 | 7 |
| Warhammer, light | 1 | 1d4+1 | 1d4 | 5 | 1 |

### 8.3 Missile Weapons

| Name | Hands | Dmg vs S/M | Dmg vs L+ | Range Inc | ROF | Weight (lbs) | Cost (gp) |
|------|-------|-----------|-----------|-----------|-----|-------------|-----------|
| Bow, long | 2 | 1d6 | 1d6 | 70ft | 2 | 12 | 60 |
| Bow, short | 2 | 1d6 | 1d6 | 50ft | 2 | 8 | 15 |
| Composite bow, long | 2 | 1d6 | 1d6 | 60ft | 2 | 8 | 100 |
| Composite bow, short | 2 | 1d6 | 1d6 | 50ft | 2 | 5 | 75 |
| Crossbow, heavy | 2 | 1d6+1 | 1d6+1 | 80ft | 1/2 | 12 | 20 |
| Crossbow, light | 2 | 1d4+1 | 1d4+1 | 60ft | 1 | 4 | 12 |
| Dart | 1 | 1d3 | 1d2 | 15ft | 3 | 0.5 | 0.2 |
| Sling | 1 | 1d4+1 | 1d6+1 | 35ft | 1 | 0.5 | 0.5 |

### 8.4 Ammunition

| Type | Weight (lbs/dozen) | Cost (gp/dozen) |
|------|--------------------|-----------------|
| Arrow | 4 | 2 |
| Bolt, heavy | 4 | 4 |
| Bolt, light | 2 | 2 |
| Sling bullet | 4 | 1 |
| Sling stone | 2 | 0 (found) |

### 8.5 General Equipment

| Item | Weight (lbs) | Cost (gp) |
|------|-------------|-----------|
| Backpack | 0 (container) | 2 |
| Waterskin | 3 (full) | 1 |
| Rations, standard (per day) | 2 | 2 |
| Rations, trail (per day) | 1 | 6 |
| Torch | 1 | 0.01 |
| Rope, hemp (50ft) | 10 | 1 |
| Rope, silk (50ft) | 5 | 10 |
| Flint and steel | 0 | 1 |
| Iron spikes (12) | 5 | 1 |
| Lantern, hooded | 2 | 7 |
| Lantern, bullseye | 3 | 12 |
| Oil, lamp (per pint) | 1 | 0.1 |
| Holy symbol, wooden | 0 | 0.6 |
| Holy symbol, pewter | 0 | 5 |
| Holy symbol, silver | 0 | 25 |
| Thieves' tools | 1 | 30 |
| Spell book (blank) | 5 | 25 |
| Small pouch | 0 | 0.2 |
| Large pouch | 0 | 0.4 |
| Small sack | 0 | 0.1 |
| Large sack | 0 | 0.15 |
| Bedroll | 5 | 0.2 |

---

## 9. Encumbrance Table

| Weight Over Allowance | Movement | Surprise |
|----------------------|----------|---------|
| 0 (unencumbered) | Full | +1 (light armor only) |
| 1–40 lbs | × 3/4 | 0 |
| 41–80 lbs | × 1/2 | 0 |
| 81–120 lbs | × 1/4 | -1 |
| 121+ lbs | Cannot move | -2 |

---

## 10. Spell Lists

### 10.1 First-Level Cleric Spells (12)

1. Bless
2. Command
3. Create Water
4. Cure Light Wounds
5. Detect Evil
6. Detect Magic
7. Light
8. Protection from Evil
9. Purify Food & Drink
10. Remove Fear
11. Resist Cold
12. Sanctuary

### 10.2 First-Level Druid Spells (11)

1. Animal Friendship
2. Detect Magic
3. Detect Pits/Snares
4. Entangle
5. Faerie Fire
6. Invisibility to Animals
7. Locate Animals
8. Pass Without Trace
9. Predict Weather
10. Purify Water
11. Shillelagh

### 10.3 First-Level Magic-User Spells (30)

1. Affect Normal Fires
2. Burning Hands
3. Charm Person
4. Comprehend Languages
5. Dancing Lights
6. Detect Magic
7. Enlarge
8. Erase
9. Feather Fall
10. Find Familiar
11. Friends
12. Hold Portal
13. Identify
14. Jump
15. Light
16. Niam's Magic Aura
17. Magic Missile
18. Mending
19. Message
20. Protection From Evil
21. Push
22. Read Magic
23. Shield
24. Shocking Grasp
25. Sleep
26. Spider Climb
27. Tanzur's Floating Disk
28. Unseen Servant
29. Ventriloquism
30. Write

Magic-User starts with 4 spells in spellbook. Read Magic is always included. Other 3 selected randomly (no duplicates).

### 10.4 First-Level Illusionist Spells (12)

1. Audible Glamour
2. Change Self
3. Colour Spray
4. Dancing Lights
5. Darkness
6. Detect Illusion
7. Detect Invisibility
8. Gaze Reflection
9. Hypnotism
10. Light
11. Phantasmal Force
12. Wall of Fog

Illusionist starts with 3 spells in spellbook, selected randomly (no duplicates).

---

## 11. Monk-Specific Data (Level 1)

| Property | Value |
|----------|-------|
| AC | 10 [10] |
| Weaponless Attacks | 1 per round |
| Weaponless Damage | 1d3 |
| Movement Rate | 150 ft |
| Hit Dice | 2d4 |

Monk skills at level 1 (same base as thief, but no Pick Pockets or Read Languages):
- Climb: 85%, Hide: 10%, Listen: 10%, Pick Locks: 25%, Move Quietly: 15%, Traps: 20%

---

## 12. Languages by Ancestry

| Ancestry | Starting Languages | Additional Options |
|----------|-------------------|-------------------|
| Dwarf | Common, Dwarfish | Gnomish, Goblin, Kobold, Orcish + max 2 |
| Elf | Common, Elven | Gnoll, Gnomish, Goblin, Halfling, Hobgoblin, Orcish (+ bonus if INT 16+) |
| Gnome | Common, Gnomish | Dwarfish, Goblin, Halfling, Kobold, burrowing animals + max 2 |
| Half-Elf | Common, Elven | Gnoll, Gnomish, Goblin, Halfling, Hobgoblin, Orcish (+ bonus if INT 17+) |
| Half-Orc | Common, Orcish | max 2 additional |
| Halfling | Common, Halfling | Dwarfish, Gnomish, Goblin, Orcish (+ bonus if INT 17+) |
| Human | Common | (per INT max additional languages) |

All characters know their alignment language in addition to above.
