"""Equipment auto-purchase logic for OSRIC 3.0 character generation."""

from pydantic import BaseModel

from osric_character_gen.data.armor import ARMOR_TABLE, SHIELD_TABLE
from osric_character_gen.data.classes import (
    CLASS_ARMOR_ALLOWED,
    CLASS_SHIELD_ALLOWED,
    CLASS_WEAPONS_ALLOWED,
)
from osric_character_gen.data.equipment import (
    ADVENTURING_GEAR,
    CLASS_REQUIRED_EQUIPMENT,
)
from osric_character_gen.data.weapons import (
    BACKUP_WEAPON_PRIORITY,
    WEAPON_PRIORITY,
    get_melee_weapon,
)
from osric_character_gen.models.character import (
    ArmorItem,
    ClassName,
    EquipmentItem,
    WeaponItem,
)


class EquipmentLoadout(BaseModel):
    armor: ArmorItem | None = None
    shield: EquipmentItem | None = None
    weapons: list[WeaponItem] = []
    equipment: list[EquipmentItem] = []
    gold_remaining: float = 0.0
    total_weight: float = 0.0


class EquipmentPurchaser:
    def purchase_equipment(
        self,
        class_name: ClassName,
        gold_available: float,
        strength: int,
    ) -> EquipmentLoadout:
        """Auto-purchase equipment within budget, respecting class restrictions."""
        budget = gold_available
        weapons: list[WeaponItem] = []
        equipment: list[EquipmentItem] = []
        total_weight = 0.0
        armor_item: ArmorItem | None = None
        shield_item: EquipmentItem | None = None

        # 1. Buy armor
        allowed_armor = CLASS_ARMOR_ALLOWED[class_name]
        if allowed_armor:
            armor_item, budget, total_weight = self._buy_armor(allowed_armor, budget, total_weight)

        # 2. Buy shield
        if CLASS_SHIELD_ALLOWED[class_name] and budget >= 10.0:
            shield_data = SHIELD_TABLE[0]  # Small Shield
            shield_item = EquipmentItem(
                name=shield_data[0],
                weight=shield_data[1],
                cost_gp=shield_data[2],
                equipped=True,
                notes="Blocks 1 attack per round",
            )
            budget -= shield_data[2]
            total_weight += shield_data[1]

        # 3. Buy primary weapon
        primary, budget, total_weight = self._buy_weapon(class_name, WEAPON_PRIORITY, budget, total_weight)
        if primary:
            weapons.append(primary)

        # 4. Buy backup weapon
        backup, budget, total_weight = self._buy_weapon(
            class_name,
            BACKUP_WEAPON_PRIORITY,
            budget,
            total_weight,
            exclude=[w.name for w in weapons],
        )
        if backup:
            weapons.append(backup)

        # 5. Class-specific required equipment
        required = CLASS_REQUIRED_EQUIPMENT.get(class_name.value, [])
        for name, weight, cost in required:
            if budget >= cost:
                equipment.append(
                    EquipmentItem(
                        name=name,
                        weight=weight,
                        cost_gp=cost,
                        equipped=True,
                    )
                )
                budget -= cost
                total_weight += weight

        # 6. Adventuring gear
        for name, weight, cost in ADVENTURING_GEAR:
            if budget >= cost:
                equipment.append(
                    EquipmentItem(
                        name=name,
                        weight=weight,
                        cost_gp=cost,
                        equipped=True,
                    )
                )
                budget -= cost
                total_weight += weight

        # 7. Remaining gold adds weight (10 coins = 1 lb)
        coin_weight = budget / 10.0
        total_weight += coin_weight

        return EquipmentLoadout(
            armor=armor_item,
            shield=shield_item,
            weapons=weapons,
            equipment=equipment,
            gold_remaining=round(budget, 2),
            total_weight=round(total_weight, 2),
        )

    def _buy_armor(
        self,
        allowed: list[str],
        budget: float,
        total_weight: float,
    ) -> tuple[ArmorItem | None, float, float]:
        """Buy best affordable armor from allowed list."""
        # Sort armor by AC desc (ascending = better defense first)
        candidates = []
        for name, ac_desc, ac_asc, weight, move_cap, cost in ARMOR_TABLE:
            if name in allowed and cost <= budget:
                candidates.append((name, ac_desc, ac_asc, weight, move_cap, cost))

        if not candidates:
            return None, budget, total_weight

        # Best armor = lowest AC desc value, then prefer lighter weight on tie
        candidates.sort(key=lambda x: (x[1], x[3]))
        best = candidates[0]
        armor = ArmorItem(
            name=best[0],
            ac_desc=best[1],
            ac_asc=best[2],
            weight=best[3],
            cost_gp=best[5],
            movement_cap=best[4],
        )
        return armor, budget - best[5], total_weight + best[3]

    def _buy_weapon(
        self,
        class_name: ClassName,
        priority_table: dict,
        budget: float,
        total_weight: float,
        exclude: list[str] | None = None,
    ) -> tuple[WeaponItem | None, float, float]:
        """Buy first affordable weapon from priority list."""
        exclude = exclude or []
        weapon_priority = priority_table.get(class_name, [])
        allowed = CLASS_WEAPONS_ALLOWED[class_name]

        for weapon_name in weapon_priority:
            if weapon_name in exclude:
                continue
            if allowed is not None and weapon_name not in allowed:
                continue
            w = get_melee_weapon(weapon_name)
            if w is None:
                continue
            name, hands, dmg_sm, dmg_l, weight, cost = w
            if cost <= budget:
                weapon = WeaponItem(
                    name=name,
                    damage_vs_sm=dmg_sm,
                    damage_vs_l=dmg_l,
                    weight=weight,
                    cost_gp=cost,
                    hands=hands,
                    weapon_type="melee",
                )
                return weapon, budget - cost, total_weight + weight

        return None, budget, total_weight
