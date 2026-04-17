"""Saving throw tables from OSRIC 3.0 Player Guide."""

from osric_character_gen.models.character import ClassName

# Level 1 saving throws: (aimed_magic, breath, death_paralysis_poison, petrification, spells)
SAVING_THROWS_LEVEL_1: dict[ClassName, tuple[int, int, int, int, int]] = {
    ClassName.ASSASSIN: (14, 16, 13, 12, 15),
    ClassName.CLERIC: (14, 16, 10, 13, 15),
    ClassName.DRUID: (14, 16, 10, 13, 15),
    ClassName.FIGHTER: (16, 17, 14, 15, 17),
    ClassName.ILLUSIONIST: (11, 15, 14, 13, 12),
    ClassName.MAGIC_USER: (11, 15, 14, 13, 12),
    ClassName.MONK: (14, 16, 13, 12, 15),
    ClassName.PALADIN: (14, 15, 12, 13, 15),
    ClassName.RANGER: (16, 17, 14, 15, 17),
    ClassName.THIEF: (14, 16, 13, 12, 15),
}
