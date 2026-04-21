# OSRIC 3.0 Character Generator — Level Choice Specification

**Version**: 1.0.0
**Date**: 2025-04-21
**Status**: Draft

---

## 1. Executive Summary

Add an optional level parameter (1–20, default 1) to character generation. The API and front-end allow users to generate characters at any level. Every level-dependent stat must scale: hit points, THAC0/BTHB, saving throws, spell slots, thief/assassin/monk skills, turn undead, weapon proficiency slots, backstab multiplier, assassination chance, monk AC/damage/movement, and class features. Equipment and starting gold remain unchanged — this generates a fresh character at a given level, not a levelled-up one.

---

## 2. Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| LV-001 | Accept `level` parameter (1–20, default 1) on `/api/v1/characters/generate` and `/api/v1/characters/generate/pdf` | Must |
| LV-002 | Front-end provides a level selector (dropdown or number input, 1–20) | Must |
| LV-003 | Roll hit points for the specified level (level × hit_die + CON mod per die, respecting hit die caps) | Must |
| LV-004 | Calculate THAC0/BTHB using full progression tables | Must |
| LV-005 | Calculate saving throws using full progression tables | Must |
| LV-006 | Calculate spell slots using full progression tables (+ WIS bonus for cleric/druid) | Must |
| LV-007 | Calculate thief/assassin skills using full level progression tables | Must |
| LV-008 | Calculate monk skills using full level progression tables | Must |
| LV-009 | Calculate turn undead using full level progression table | Must |
| LV-010 | Calculate weapon proficiency slots using level-based gain schedule | Must |
| LV-011 | Calculate backstab multiplier for thief/assassin based on level | Must |
| LV-012 | Calculate assassination chance for assassin based on level | Should |
| LV-013 | Calculate monk AC, weaponless damage, and movement by level | Must |
| LV-014 | Calculate XP total for the given level (using XP progression tables) | Should |
| LV-015 | HP after hit die cap: fixed HP per level (no CON bonus) | Must |
| LV-016 | Ranger gets 2 hit dice at level 1 only; levels 2+ roll 1 die each | Must |
| LV-017 | Monk gets 2 hit dice at level 1 only; levels 2+ roll 1 die each | Must |
| LV-018 | Select and memorize spells for all available spell slot levels | Must |
| LV-019 | Spellbook contains spells across all accessible spell levels | Must |
| LV-020 | Paladin gains spellcasting at level 9+ | Should |
| LV-021 | Ranger gains druidic spellcasting at level 8+, arcane at level 9+ | Should |
| LV-022 | Front-end auto-generates on level change | Must |
| LV-023 | Seed + level must be deterministic | Must |

---

## 3. API Changes

### 3.1 Query Parameter Addition

Both endpoints gain a `level` parameter:

```
GET /api/v1/characters/generate?level=5&seed=42
GET /api/v1/characters/generate/pdf?level=5&seed=42
```

| Parameter | Type | Default | Range | Description |
|-----------|------|---------|-------|-------------|
| `level` | int | 1 | 1–20 | Character level |

Validation: return 422 if level < 1 or level > 20.

### 3.2 Model Changes

`CharacterSheet.level` already exists. No model changes required — it will simply hold the requested level instead of always being 1.

### 3.3 Service Changes

`CharacterGeneratorService.generate()` accepts a `level` parameter and passes it to every downstream calculator that currently ignores `_level`.

---

## 4. Hit Points by Level

### 4.1 Formula

```
For levels 1 through hit_die_cap:
  HP = sum(roll(hit_die) + CON_hp_mod for each level)
  Minimum 1 HP per die roll (after CON mod)
  CON 19: treat any die roll of 1 as 2

For levels above hit_die_cap:
  HP += fixed_hp_per_level * (level - hit_die_cap)
  No CON bonus on fixed HP
```

### 4.2 Hit Die Caps and Fixed HP

| Class | Hit Die | Hit Die Cap (max level with dice) | Fixed HP/level after cap |
|-------|---------|----------------------------------|--------------------------|
| Assassin | d6 | 15 | +2 |
| Cleric | d8 | 9 | +2 |
| Druid | d8 | 14 | +2 |
| Fighter | d10 | 9 | +3 |
| Illusionist | d4 | 10 | +1 |
| Magic-User | d4 | 10 | +1 |
| Monk | d4 | 18 | — (max level 17) |
| Paladin | d10 | 9 | +3 |
| Ranger | d8 | 11 | +2 |
| Thief | d6 | 10 | +2 |

### 4.3 Special Cases

- **Ranger**: 2d8 at level 1, then 1d8 per level from 2–11, then +2/level after 11.
- **Monk**: 2d4 at level 1, then 1d4 per level from 2–17 (no post-cap, max 17).
- **Minimum**: Total HP is always >= 1, regardless of CON penalties.

---

## 5. THAC0 / BTHB Progression

### 5.1 Fighter / Paladin / Ranger

| Level | THAC0 | BTHB |
|-------|-------|------|
| 1 | 20 | 0 |
| 2 | 20 | 0 |
| 3 | 18 | +2 |
| 4 | 18 | +2 |
| 5 | 16 | +4 |
| 6 | 16 | +4 |
| 7 | 14 | +6 |
| 8 | 14 | +6 |
| 9 | 12 | +8 |
| 10 | 12 | +8 |
| 11 | 10 | +10 |
| 12 | 10 | +10 |
| 13 | 8 | +12 |
| 14 | 8 | +12 |
| 15 | 6 | +14 |
| 16 | 6 | +14 |
| 17 | 4 | +16 |
| 18 | 4 | +16 |
| 19 | 2 | +18 |
| 20 | 2 | +18 |

### 5.2 Cleric / Druid / Monk

| Level | THAC0 | BTHB |
|-------|-------|------|
| 1–3 | 20 | 0 |
| 4–6 | 18 | +2 |
| 7–9 | 16 | +4 |
| 10–12 | 14 | +6 |
| 13–15 | 12 | +8 |
| 16–18 | 10 | +10 |
| 19+ | 8 | +12 |

### 5.3 Thief / Assassin

| Level | THAC0 | BTHB |
|-------|-------|------|
| 1–4 | 21 | -1 |
| 5–8 | 19 | +1 |
| 9–12 | 16 | +4 |
| 13–16 | 14 | +6 |
| 17–20 | 12 | +8 |

### 5.4 Magic-User / Illusionist

| Level | THAC0 | BTHB |
|-------|-------|------|
| 1–5 | 21 | -1 |
| 6–10 | 19 | +1 |
| 11–15 | 16 | +4 |
| 16–20 | 11 | +9 |

---

## 6. Saving Throw Progression

### 6.1 Fighter / Paladin / Ranger

| Level | Aimed Magic | Breath | Death/Para/Poison | Petrification | Spells |
|-------|-------------|--------|-------------------|---------------|--------|
| 1–2 | 16 | 17 | 14 | 15 | 17 |
| 3–4 | 15 | 16 | 13 | 14 | 16 |
| 5–6 | 13 | 13 | 11 | 12 | 14 |
| 7–8 | 12 | 12 | 10 | 11 | 13 |
| 9–10 | 10 | 9 | 8 | 9 | 11 |
| 11–12 | 9 | 8 | 7 | 8 | 10 |
| 13–14 | 7 | 5 | 5 | 6 | 8 |
| 15–16 | 6 | 4 | 4 | 5 | 7 |
| 17–18 | 5 | 4 | 3 | 4 | 6 |
| 19–20 | 4 | 3 | 2 | 3 | 5 |

**Paladin bonus**: -2 to all saves (built into Paladin-specific table, not applied as modifier).

### 6.2 Cleric / Druid

| Level | Aimed Magic | Breath | Death/Para/Poison | Petrification | Spells |
|-------|-------------|--------|-------------------|---------------|--------|
| 1–3 | 14 | 16 | 10 | 13 | 15 |
| 4–6 | 13 | 15 | 9 | 12 | 14 |
| 7–9 | 11 | 13 | 7 | 10 | 12 |
| 10–12 | 10 | 12 | 6 | 9 | 11 |
| 13–15 | 8 | 10 | 4 | 7 | 9 |
| 16–18 | 7 | 9 | 3 | 6 | 8 |
| 19+ | 5 | 7 | 2 | 5 | 6 |

### 6.3 Thief / Assassin / Monk

| Level | Aimed Magic | Breath | Death/Para/Poison | Petrification | Spells |
|-------|-------------|--------|-------------------|---------------|--------|
| 1–4 | 14 | 16 | 13 | 12 | 15 |
| 5–8 | 12 | 15 | 12 | 11 | 13 |
| 9–12 | 10 | 13 | 11 | 10 | 11 |
| 13–16 | 8 | 11 | 9 | 8 | 9 |
| 17–20 | 6 | 9 | 7 | 6 | 7 |

### 6.4 Magic-User / Illusionist

| Level | Aimed Magic | Breath | Death/Para/Poison | Petrification | Spells |
|-------|-------------|--------|-------------------|---------------|--------|
| 1–5 | 11 | 15 | 14 | 13 | 12 |
| 6–10 | 9 | 13 | 13 | 11 | 10 |
| 11–15 | 7 | 11 | 11 | 9 | 8 |
| 16–20 | 5 | 9 | 10 | 7 | 6 |

### 6.5 Paladin (dedicated table — includes built-in -2 bonus)

| Level | Aimed Magic | Breath | Death/Para/Poison | Petrification | Spells |
|-------|-------------|--------|-------------------|---------------|--------|
| 1–2 | 14 | 15 | 12 | 13 | 15 |
| 3–4 | 13 | 14 | 11 | 12 | 14 |
| 5–6 | 11 | 11 | 9 | 10 | 12 |
| 7–8 | 10 | 10 | 8 | 9 | 11 |
| 9–10 | 8 | 7 | 6 | 7 | 9 |
| 11–12 | 7 | 6 | 5 | 6 | 8 |
| 13–14 | 5 | 3 | 3 | 4 | 6 |
| 15–16 | 4 | 2 | 2 | 3 | 5 |
| 17–18 | 3 | 2 | 1 | 2 | 4 |
| 19–20 | 2 | 1 | 1 | 1 | 3 |

### 6.6 Modifiers (applied after table lookup)

- **WIS mental save**: subtracted from Spells save
- **Stalwart** (Dwarf/Gnome/Halfling): CON-based bonus subtracted from Aimed Magic, Death/Paralysis/Poison, and Spells saves

---

## 7. Spell Slot Progression

### 7.1 Cleric Spell Slots

| Level | 1st | 2nd | 3rd | 4th | 5th | 6th | 7th |
|-------|-----|-----|-----|-----|-----|-----|-----|
| 1 | 1 | — | — | — | — | — | — |
| 2 | 2 | — | — | — | — | — | — |
| 3 | 2 | 1 | — | — | — | — | — |
| 4 | 3 | 2 | — | — | — | — | — |
| 5 | 3 | 3 | 1 | — | — | — | — |
| 6 | 3 | 3 | 2 | — | — | — | — |
| 7 | 3 | 3 | 2 | 1 | — | — | — |
| 8 | 3 | 3 | 3 | 2 | — | — | — |
| 9 | 4 | 4 | 3 | 2 | 1 | — | — |
| 10 | 4 | 4 | 3 | 3 | 2 | — | — |
| 11 | 5 | 4 | 4 | 3 | 2 | 1 | — |
| 12 | 6 | 5 | 5 | 3 | 2 | 2 | — |
| 13 | 6 | 6 | 6 | 4 | 2 | 2 | — |
| 14 | 6 | 6 | 6 | 5 | 3 | 2 | — |
| 15 | 7 | 7 | 7 | 5 | 4 | 2 | — |
| 16 | 7 | 7 | 7 | 6 | 5 | 3 | 1 |
| 17 | 8 | 8 | 8 | 6 | 5 | 3 | 1 |
| 18 | 8 | 8 | 8 | 7 | 6 | 4 | 1 |
| 19 | 9 | 9 | 9 | 7 | 6 | 4 | 2 |
| 20 | 9 | 9 | 9 | 8 | 7 | 5 | 2 |

WIS bonus spells added on top (as per existing logic).

### 7.2 Druid Spell Slots

| Level | 1st | 2nd | 3rd | 4th | 5th | 6th | 7th |
|-------|-----|-----|-----|-----|-----|-----|-----|
| 1 | 2 | — | — | — | — | — | — |
| 2 | 2 | 1 | — | — | — | — | — |
| 3 | 3 | 2 | 1 | — | — | — | — |
| 4 | 4 | 2 | 2 | — | — | — | — |
| 5 | 4 | 3 | 2 | — | — | — | — |
| 6 | 4 | 3 | 2 | 1 | — | — | — |
| 7 | 4 | 4 | 3 | 1 | — | — | — |
| 8 | 4 | 4 | 3 | 2 | — | — | — |
| 9 | 5 | 4 | 3 | 2 | 1 | — | — |
| 10 | 5 | 4 | 3 | 3 | 2 | — | — |
| 11 | 5 | 5 | 3 | 3 | 2 | 1 | — |
| 12 | 6 | 5 | 4 | 4 | 3 | 2 | 1 |
| 13 | 6 | 5 | 5 | 5 | 3 | 2 | 1 |
| 14 | 6 | 6 | 6 | 6 | 4 | 3 | 2 |

WIS bonus spells added on top.

### 7.3 Magic-User Spell Slots

| Level | 1st | 2nd | 3rd | 4th | 5th | 6th | 7th |
|-------|-----|-----|-----|-----|-----|-----|-----|
| 1 | 1 | — | — | — | — | — | — |
| 2 | 2 | — | — | — | — | — | — |
| 3 | 2 | 1 | — | — | — | — | — |
| 4 | 3 | 2 | — | — | — | — | — |
| 5 | 4 | 2 | 1 | — | — | — | — |
| 6 | 4 | 2 | 2 | — | — | — | — |
| 7 | 4 | 3 | 2 | 1 | — | — | — |
| 8 | 4 | 3 | 3 | 2 | — | — | — |
| 9 | 4 | 3 | 3 | 2 | 1 | — | — |
| 10 | 4 | 4 | 3 | 2 | 2 | — | — |
| 11 | 4 | 4 | 4 | 3 | 3 | — | — |
| 12 | 4 | 4 | 4 | 4 | 4 | 1 | — |
| 13 | 5 | 5 | 5 | 4 | 4 | 2 | — |
| 14 | 5 | 5 | 5 | 4 | 4 | 2 | 1 |
| 15 | 5 | 5 | 5 | 5 | 5 | 3 | 1 |
| 16 | 5 | 5 | 5 | 5 | 5 | 3 | 2 |
| 17 | 5 | 5 | 5 | 5 | 5 | 3 | 3 |
| 18 | 5 | 5 | 5 | 5 | 5 | 3 | 3 |
| 19 | 5 | 5 | 5 | 5 | 5 | 3 | 3 |
| 20 | 5 | 5 | 5 | 5 | 5 | 4 | 3 |

### 7.4 Illusionist Spell Slots

| Level | 1st | 2nd | 3rd | 4th | 5th | 6th | 7th |
|-------|-----|-----|-----|-----|-----|-----|-----|
| 1 | 1 | — | — | — | — | — | — |
| 2 | 2 | — | — | — | — | — | — |
| 3 | 2 | 1 | — | — | — | — | — |
| 4 | 3 | 2 | — | — | — | — | — |
| 5 | 4 | 2 | 1 | — | — | — | — |
| 6 | 4 | 3 | 1 | — | — | — | — |
| 7 | 4 | 3 | 2 | 1 | — | — | — |
| 8 | 4 | 3 | 3 | 2 | — | — | — |
| 9 | 5 | 3 | 3 | 2 | 1 | — | — |
| 10 | 5 | 4 | 3 | 2 | 2 | — | — |
| 11 | 5 | 4 | 4 | 3 | 3 | — | — |
| 12 | 5 | 5 | 4 | 4 | 4 | 1 | — |
| 13 | 5 | 5 | 5 | 4 | 4 | 2 | — |
| 14 | 5 | 5 | 5 | 4 | 4 | 2 | 1 |

### 7.5 Paladin Spell Slots (level 9+, cleric spells)

| Level | 1st | 2nd | 3rd | 4th |
|-------|-----|-----|-----|-----|
| 1–8 | — | — | — | — |
| 9 | 1 | — | — | — |
| 10 | 2 | — | — | — |
| 11 | 2 | 1 | — | — |
| 12 | 2 | 2 | — | — |
| 13 | 2 | 2 | 1 | — |
| 14 | 3 | 2 | 1 | — |
| 15 | 3 | 2 | 1 | 1 |
| 16 | 3 | 3 | 2 | 1 |
| 17 | 3 | 3 | 3 | 1 |
| 18 | 3 | 3 | 3 | 2 |
| 19 | 4 | 3 | 3 | 2 |
| 20 | 4 | 4 | 3 | 3 |

Paladin uses cleric spell list (1st–4th level only). No WIS bonus spells.

### 7.6 Ranger Spell Slots (druid at level 8+, magic-user at level 9+)

**Druid spells:**

| Level | 1st | 2nd | 3rd |
|-------|-----|-----|-----|
| 1–7 | — | — | — |
| 8 | 1 | — | — |
| 9 | 1 | — | — |
| 10 | 2 | — | — |
| 11 | 2 | — | — |
| 12 | 2 | 1 | — |
| 13 | 2 | 1 | — |
| 14 | 2 | 2 | — |
| 15 | 2 | 2 | 1 |
| 16 | 3 | 2 | 1 |
| 17 | 3 | 2 | 2 |

**Magic-User spells:**

| Level | 1st | 2nd |
|-------|-----|-----|
| 1–8 | — | — |
| 9 | 1 | — |
| 10 | 1 | — |
| 11 | 2 | — |
| 12 | 2 | — |
| 13 | 2 | 1 |
| 14 | 2 | 1 |
| 15 | 2 | 2 |
| 16 | 3 | 2 |
| 17 | 3 | 2 |

---

## 8. Thief Skill Progression

### 8.1 Base Skills by Level

| Level | Climb | Hide | Listen | Pick Locks | Pick Pockets | Read Lang | Move Quietly | Traps |
|-------|-------|------|--------|------------|-------------|-----------|-------------|-------|
| 1 | 85 | 10 | 10 | 25 | 30 | 1 | 15 | 20 |
| 2 | 86 | 15 | 10 | 29 | 35 | 5 | 21 | 25 |
| 3 | 87 | 20 | 15 | 33 | 40 | 10 | 27 | 30 |
| 4 | 88 | 25 | 15 | 37 | 45 | 15 | 33 | 35 |
| 5 | 89 | 31 | 20 | 42 | 50 | 20 | 40 | 40 |
| 6 | 90 | 37 | 20 | 47 | 55 | 25 | 47 | 45 |
| 7 | 91 | 43 | 25 | 52 | 60 | 30 | 55 | 50 |
| 8 | 92 | 49 | 25 | 57 | 65 | 35 | 62 | 55 |
| 9 | 93 | 56 | 30 | 62 | 70 | 40 | 70 | 60 |
| 10 | 94 | 63 | 30 | 67 | 80 | 45 | 78 | 65 |
| 11 | 95 | 70 | 35 | 72 | 90 | 50 | 86 | 70 |
| 12 | 96 | 77 | 35 | 77 | 95 | 55 | 94 | 75 |
| 13 | 97 | 85 | 40 | 82 | 99 | 60 | 99 | 80 |
| 14 | 98 | 93 | 40 | 87 | 99 | 65 | 99 | 85 |
| 15 | 99 | 99 | 45 | 92 | 99 | 70 | 99 | 90 |
| 16 | 99 | 99 | 45 | 97 | 99 | 75 | 99 | 95 |
| 17 | 99 | 99 | 55 | 99 | 99 | 80 | 99 | 99 |

DEX and ancestry adjustments still apply on top of the level-based values. Clamp [1, 99].

### 8.2 Assassin Skills

Assassin uses the same thief skill table progression.

### 8.3 Monk Skills

Monk uses the thief skill table progression but never gains Pick Pockets or Read Languages (kept at 1%).

---

## 9. Turn Undead Progression

| Type | Example | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 | L9+ |
|------|---------|----|----|----|----|----|----|----|----|-----|
| 1 | Skeleton | 10 | 7 | 4 | T | T | D | D | D | D |
| 2 | Zombie | 13 | 10 | 7 | T | T | D | D | D | D |
| 3 | Ghoul | 16 | 13 | 10 | 4 | T | T | D | D | D |
| 4 | Shadow | 19 | 16 | 13 | 7 | 4 | T | T | D | D |
| 5 | Wight | 20 | 19 | 16 | 10 | 7 | 4 | T | T | D |
| 6 | Ghast | — | 20 | 19 | 13 | 10 | 7 | 4 | T | T |
| 7 | Wraith | — | — | 20 | 16 | 13 | 10 | 7 | 4 | T |
| 8 | Mummy | — | — | — | 19 | 16 | 13 | 10 | 7 | 4 |
| 9 | Spectre | — | — | — | 20 | 19 | 16 | 13 | 10 | 7 |
| 10 | Vampire | — | — | — | — | 20 | 19 | 16 | 13 | 10 |
| 11 | Ghost | — | — | — | — | — | 20 | 19 | 16 | 13 |
| 12 | Lich | — | — | — | — | — | — | 20 | 19 | 16 |
| 13 | Fiend | — | — | — | — | — | — | — | 20 | 19 |

T = automatic turn (2d6 HD affected). D = automatic destroy (2d6 HD affected). — = cannot turn.

---

## 10. Weapon Proficiency Progression

| Class | Starting | Gain at levels |
|-------|----------|----------------|
| Assassin | 3 | 4, 8, 12, 16, 20 |
| Cleric | 2 | 4, 7, 10, 13, 16, 19 |
| Druid | 2 | 4, 7, 10, 13, 16, 19 |
| Fighter | 4 | 3, 5, 7, 9, 11, 13, 15, 17, 19 |
| Illusionist | 1 | 6, 11, 16 |
| Magic-User | 1 | 6, 11, 16 |
| Monk | 1 | 3, 5, 7, 9, 11, 13, 15, 17 |
| Paladin | 3 | 5, 8, 11, 14, 17, 20 |
| Ranger | 3 | 5, 8, 11, 14, 17, 20 |
| Thief | 2 | 6, 10, 14, 18 |

**Implementation**: Count starting slots + number of gain levels <= current level.

---

## 11. Backstab Multiplier (Thief / Assassin)

| Level | Multiplier |
|-------|-----------|
| 1–4 | ×2 |
| 5–8 | ×3 |
| 9–12 | ×4 |
| 13+ | ×5 |

---

## 12. Assassination Table (Assassin only)

Base chance = 50% + (5% × assassin level) - (5% × target HD/2, rounded down).

| Level | Base % (0 HD target) |
|-------|---------------------|
| 1 | 55% |
| 2 | 60% |
| 3 | 65% |
| 4 | 70% |
| 5 | 75% |
| ... | ... |
| 14 | 120% (capped at 99%) |

Display the base percentage in class features.

---

## 13. Monk Level Progression

### 13.1 Monk AC

| Level | AC (Desc) | AC (Asc) |
|-------|-----------|----------|
| 1 | 10 | 10 |
| 2 | 9 | 11 |
| 3 | 8 | 12 |
| 4 | 7 | 13 |
| 5 | 6 | 14 |
| 6 | 5 | 15 |
| 7 | 4 | 16 |
| 8 | 3 | 17 |
| 9 | 2 | 18 |
| 10 | 1 | 19 |
| 11 | 0 | 20 |
| 12 | -1 | 21 |
| 13 | -2 | 22 |
| 14 | -3 | 23 |
| 15 | -4 | 24 |
| 16 | -5 | 25 |
| 17 | -6 | 26 |

### 13.2 Monk Weaponless Damage

| Level | Damage |
|-------|--------|
| 1–3 | 1d3 |
| 4–5 | 1d4 |
| 6–7 | 1d6 |
| 8 | 2d4 |
| 9–10 | 2d4+1 |
| 11–13 | 3d4 |
| 14–15 | 4d4 |
| 16–17 | 5d4 |

### 13.3 Monk Movement

| Level | Movement (ft) |
|-------|---------------|
| 1–2 | 150 |
| 3–4 | 160 |
| 5 | 170 |
| 6 | 180 |
| 7 | 190 |
| 8 | 200 |
| 9 | 210 |
| 10 | 220 |
| 11 | 230 |
| 12 | 240 |
| 13 | 250 |
| 14 | 260 |
| 15 | 270 |
| 16 | 280 |
| 17 | 290 |

### 13.4 Monk Special Abilities by Level

| Level | Ability |
|-------|--------|
| 2 | Deflect Missiles (save vs. petrification to negate 1 ranged attack/round) |
| 3 | Speak with Animals (at will) |
| 4 | Slow Fall (20 ft) — no damage |
| 5 | Slow Fall (30 ft), Immune to disease |
| 6 | Slow Fall (any distance), Feign Death |
| 7 | Self-heal 1d4+level HP once/day |
| 8 | Speak with Plants (at will) |
| 9 | +1 to saves vs. mental attacks |
| 10 | Immune to haste, slow, charm, geas, quest |
| 11 | Immune to poison |
| 12 | Immune to psionics |
| 13 | Quivering Palm (1/week, save vs. death or die) |

---

## 14. XP Progression Tables

### 14.1 XP Required per Level

| Level | Fighter | Paladin | Ranger | Cleric | Druid | Thief | Assassin | MU | Illu | Monk |
|-------|---------|---------|--------|--------|-------|-------|----------|-----|------|------|
| 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2 | 2,000 | 2,750 | 2,250 | 1,500 | 2,000 | 1,250 | 1,500 | 2,500 | 2,250 | 2,250 |
| 3 | 4,000 | 5,500 | 4,500 | 3,000 | 4,000 | 2,500 | 3,000 | 5,000 | 4,500 | 4,750 |
| 4 | 8,000 | 12,000 | 9,500 | 6,000 | 7,500 | 5,000 | 6,000 | 10,000 | 9,000 | 10,000 |
| 5 | 16,000 | 24,000 | 20,000 | 13,000 | 12,500 | 10,000 | 12,000 | 20,000 | 18,000 | 22,500 |
| 6 | 32,000 | 50,000 | 40,000 | 27,500 | 20,000 | 20,000 | 25,000 | 40,000 | 35,000 | 47,500 |
| 7 | 64,000 | 100,000 | 90,000 | 55,000 | 35,000 | 42,500 | 50,000 | 60,000 | 60,000 | 98,000 |
| 8 | 125,000 | 200,000 | 150,000 | 110,000 | 60,000 | 70,000 | 100,000 | 90,000 | 95,000 | 200,000 |
| 9 | 250,000 | 350,000 | 300,000 | 225,000 | 90,000 | 110,000 | 200,000 | 135,000 | 145,000 | 350,000 |
| 10 | 500,000 | 500,000 | 600,000 | 450,000 | 125,000 | 160,000 | 300,000 | 250,000 | 220,000 | 500,000 |
| 11 | 750,000 | 750,000 | 900,000 | 675,000 | 200,000 | 220,000 | 400,000 | 375,000 | 440,000 | 700,000 |
| 12 | 1,000,000 | 1,000,000 | 1,200,000 | 900,000 | 400,000 | 440,000 | 600,000 | 750,000 | 660,000 | 1,000,000 |
| 13 | 1,250,000 | 1,250,000 | 1,500,000 | 1,125,000 | 700,000 | 660,000 | 750,000 | 1,125,000 | 880,000 | 1,500,000 |
| 14 | 1,500,000 | 1,500,000 | 1,800,000 | 1,350,000 | 1,000,000 | 880,000 | 1,000,000 | 1,500,000 | 1,100,000 | 2,000,000 |
| 15 | 1,750,000 | 1,750,000 | 2,100,000 | 1,575,000 | — | 1,100,000 | 1,500,000 | 1,875,000 | — | 2,500,000 |
| 16 | 2,000,000 | 2,000,000 | 2,400,000 | 1,800,000 | — | 1,320,000 | — | 2,250,000 | — | 3,000,000 |
| 17 | 2,250,000 | 2,250,000 | 2,700,000 | 2,025,000 | — | 1,540,000 | — | 2,625,000 | — | 3,500,000 |
| 18 | 2,500,000 | 2,500,000 | 3,000,000 | 2,250,000 | — | 1,760,000 | — | 3,000,000 | — | — |
| 19 | 2,750,000 | 2,750,000 | 3,300,000 | 2,475,000 | — | 1,980,000 | — | 3,375,000 | — | — |
| 20 | 3,000,000 | 3,000,000 | 3,600,000 | 2,700,000 | — | 2,200,000 | — | 3,750,000 | — | — |

— = class maximum level reached.

---

## 15. Spell Lists for Higher Levels

Higher-level spell lists are required for spell selection at levels 2+. These must be added to `spells.py`.

### 15.1 Spells Needed by Spell Level

| Spell Level | Cleric | Druid | Magic-User | Illusionist |
|-------------|--------|-------|------------|-------------|
| 1st | Existing | Existing | Existing | Existing |
| 2nd | New | New | New | New |
| 3rd | New | New | New | New |
| 4th | New | New | New | New |
| 5th | New | New | New | New |
| 6th | New | — | New | New |
| 7th | New | — | New | New |

These spell lists need to be extracted from the OSRIC 3.0 Player Guide and added as data tables.

### 15.2 Spellbook Rules

- Magic-User: starts with 4 level-1 spells (including Read Magic). Gains spells as found/researched. For generator purposes: randomly select spells per slot level, with count = slots × 1.5 (rounded up) for the spellbook, and slots count for memorized.
- Illusionist: starts with 3 level-1 spells. Same rule for higher levels.
- Cleric/Druid: access full spell list (divine casters choose freely). Randomly select memorized spells = slot count.

---

## 16. Class Feature Text by Level

Class features displayed on the sheet must update based on level. Key changes:

| Class | Feature | Level dependency |
|-------|---------|------------------|
| Thief | Backstab | "×2 damage" → "×3 damage" etc. per section 11 |
| Assassin | Assassination | "55% base" → "60% base" etc. per section 12 |
| Assassin | Backstab | Same as thief |
| Cleric | Turn Undead | "Turn Undead" (always present) |
| Cleric | Spellcasting | Slot count updates |
| Druid | Spellcasting | Slot count updates |
| Magic-User | Spellcasting | Slot count updates |
| Illusionist | Spellcasting | Slot count updates |
| Paladin | Lay on Hands | "2 HP × level per day" — value changes |
| Paladin | Spellcasting | Appears at level 9+ |
| Ranger | Damage vs giants | "+1 damage per level" — value changes |
| Ranger | Spellcasting | Druidic at 8+, Arcane at 9+ |
| Monk | AC | Updates per section 13.1 |
| Monk | Weaponless damage | Updates per section 13.2 |
| Monk | Movement | Updates per section 13.3 |
| Monk | Special abilities | Accumulate per section 13.4 |
| Fighter | Heroic Assault | Available at level 2+ |

---

## 17. Front-End Changes

### 17.1 Level Selector

Add a number input or dropdown to the toolbar:

```html
<label for="level-select">Level:</label>
<select id="level-select">
  <option value="1" selected>1</option>
  <option value="2">2</option>
  ...
  <option value="20">20</option>
</select>
```

### 17.2 Behavior

- Default: level 1 (backward compatible).
- Changing level triggers `generateCharacter()` with the selected level.
- The `fetch` call includes `?level=N` in the query string.
- PDF download also passes `&level=N`.
- Level field on the sheet reflects the selected level.

### 17.3 JavaScript Changes

```javascript
async function generateCharacter() {
  const level = document.getElementById('level-select').value;
  const resp = await fetch('/api/v1/characters/generate?level=' + level);
  // ...
}

function downloadPdf() {
  const level = document.getElementById('level-select').value;
  window.open('/api/v1/characters/generate/pdf?seed=' + currentSeed + '&level=' + level, '_blank');
}
```

---

## 18. Implementation Phases

### Phase 1: Data Tables (No business logic changes)

Add to `src/osric_character_gen/data/`:

1. `saving_throws.py`: Replace `SAVING_THROWS_LEVEL_1` with `SAVING_THROWS` — full progression tables per class group
2. `classes.py`: Add `CLASS_HIT_DIE_CAP`, `CLASS_FIXED_HP_PER_LEVEL`, `CLASS_THAC0_PROGRESSION`, `CLASS_PROFICIENCY_GAIN_LEVELS`, `CLASS_XP_TABLE`
3. `thief_skills.py`: Add `THIEF_SKILLS_BY_LEVEL` — full 17-level table
4. `turn_undead.py`: Replace `TURN_UNDEAD_LEVEL_1` with `TURN_UNDEAD` — full 9+ level table
5. `spells.py`: Add level 2–7 spell lists for all casting classes
6. New file `monk_tables.py`: Monk AC, damage, movement, and special abilities by level

### Phase 2: Calculator Updates

Update `src/osric_character_gen/domain/stats_calculator.py`:

1. `calculate_saving_throws()`: Use `level` to look up correct row
2. `calculate_thac0()`: Use `level` to look up correct row
3. `calculate_thief_skills()`: Use `level` to look up base values
4. `calculate_turn_undead()`: Use `level` to look up correct table
5. `calculate_spell_slots()`: Use `level` to look up correct row, handle Paladin/Ranger
6. New: `calculate_weapon_proficiencies()`: Count slots from gain schedule
7. New: `calculate_backstab_multiplier()`: Level-based lookup

### Phase 3: Service Orchestrator

Update `src/osric_character_gen/services/character_generator.py`:

1. Accept `level` parameter in `generate()`
2. Roll HP for N levels (dice up to cap, fixed after)
3. Pass `level` to all calculator methods
4. Handle Paladin/Ranger spell acquisition at higher levels
5. Select spells for all accessible spell levels
6. Update class features text based on level
7. Calculate XP for level from table

### Phase 4: API + Frontend

1. Add `level` query parameter to both endpoints
2. Add level selector to HTML page
3. Wire JavaScript to pass level

---

## 19. Files Modified

| File | Change |
|------|--------|
| `data/saving_throws.py` | Full progression tables |
| `data/classes.py` | Hit die caps, THAC0 progression, proficiency schedules, XP tables |
| `data/thief_skills.py` | Full level progression table |
| `data/turn_undead.py` | Full level progression table |
| `data/spells.py` | Level 2–7 spell lists |
| `data/monk_tables.py` | New file — monk level tables |
| `domain/stats_calculator.py` | All calculate methods use level |
| `services/character_generator.py` | Level parameter, multi-level HP, spell selection |
| `domain/spell_selector.py` | Handle multi-level spell selection |
| `domain/dice.py` | `roll_hit_points` handle multi-level rolls |
| `api/v1/endpoints/characters.py` | `level` query parameter |
| `api/v1/endpoints/frontend.py` | Level selector in HTML |
| `models/requests.py` | Add level field |
| `models/character.py` | Add backstab_multiplier, assassination_chance, monk fields |

---

## 20. Assumptions

1. Equipment and starting gold are NOT scaled by level. The generator creates a "fresh" character at the target level, not a character who accumulated wealth over time.
2. The spellbook for magic-users/illusionists at higher levels contains randomly selected spells per accessible level (count = spell_slots × 1.5 rounded up). This is an approximation since OSRIC doesn't define how many spells a mage would have found by a given level.
3. XP is set to the minimum for the given level (the table entry). No bonus XP is included.
4. Monks are capped at level 17, Druids at 14, Assassins at 15. Requesting a level beyond the cap for these classes will generate at the cap level.
5. Paladin saving throws use their own dedicated table (which includes the -2 bonus) rather than the Fighter table with a -2 modifier applied.
6. All progression data is sourced from the OSRIC 3.0 Player Guide. Values must be verified against the PDF during implementation.
