"""Holmesian Random Name Generator.

Based on the method by Zenopus Archives:
https://zenopusarchives.blogspot.com/2013/06/holmesian-random-names.html

Syllables drawn from the proper names in the Holmes Basic Rulebook
and module B1 by Mike Carr.
"""

from osric_character_gen.domain.dice import DiceRoller


class HolmesianNameGenerator:
    """Generates random character names using the Holmesian method.

    Roll d100 for syllable count, then d100 for each syllable from a
    table of 100 entries. Optionally add a title from a d20 table.
    """

    # fmt: off
    SYLLABLE_TABLE: list[list[str]] = [
        ["Af"],                  # 1
        ["Al", "Ael"],           # 2
        ["Baf"],                 # 3
        ["Bel"],                 # 4
        ["Ber", "Berd"],         # 5
        ["Bes"],                 # 6
        ["Bo"],                  # 7
        ["Bor"],                 # 8
        ["Bran"],                # 9
        ["Bru"],                 # 10
        ["Car"],                 # 11
        ["Chor"],                # 12
        ["Cig"],                 # 13
        ["Cla"],                 # 14
        ["Da"],                  # 15
        ["Do", "Doh"],           # 16
        ["Don"],                 # 17
        ["Dor"],                 # 18
        ["Dre", "Dreb"],         # 19
        ["Eg", "Feg"],           # 20
        ["Er"],                  # 21
        ["Es"],                  # 22
        ["Ev"],                  # 23
        ["Fal", "Ful"],          # 24
        ["Fan", "Fen"],          # 25
        ["Far"],                 # 26
        ["Fum"],                 # 27
        ["Ga", "Gahn"],          # 28
        ["Gaith"],               # 29
        ["Gar"],                 # 30
        ["Gen", "Glen"],         # 31
        ["Go"],                  # 32
        ["Gram"],                # 33
        ["Ha"],                  # 34
        ["Hag", "Harg"],         # 35
        ["Ho"],                  # 36
        ["Ig"],                  # 37
        ["Ka"],                  # 38
        ["Kar"],                 # 39
        ["Kra", "Krac"],         # 40
        ["Ky"],                  # 41
        ["Lag"],                 # 42
        ["Lap"],                 # 43
        ["Le"],                  # 44
        ["Lef"],                 # 45
        ["Lis"],                 # 46
        ["Lo"],                  # 47
        ["Lu"],                  # 48
        ["Mal"],                 # 49
        ["Mar"],                 # 50
        ["Me"],                  # 51
        ["Mez"],                 # 52
        ["Mich"],                # 53
        ["Mil", "Mul"],          # 54
        ["Mo"],                  # 55
        ["Mun"],                 # 56
        ["Mus"],                 # 57
        ["Ned"],                 # 58
        ["Nic"],                 # 59
        ["No"],                  # 60
        ["Nor"],                 # 61
        ["Nu"],                  # 62
        ["Os"],                  # 63
        ["Pal"],                 # 64
        ["Pen"],                 # 65
        ["Phil"],                # 66
        ["Po", "Poy"],           # 67
        ["Pos", "Pus"],          # 68
        ["Pres"],                # 69
        ["Quas"],                # 70
        ["Que"],                 # 71
        ["Rag"],                 # 72
        ["Ralt"],                # 73
        ["Ram"],                 # 74
        ["Rin", "Ron"],          # 75
        ["Ris"],                 # 76
        ["Ro"],                  # 77
        ["Sa"],                  # 78
        ["See"],                 # 79
        ["Ser", "Sur"],          # 80
        ["Sho"],                 # 81
        ["Sit"],                 # 82
        ["Spor"],                # 83
        ["Tar"],                 # 84
        ["Tas"],                 # 85
        ["Ten", "Ton"],          # 86
        ["To"],                  # 87
        ["Tra"],                 # 88
        ["Treb", "Tred"],        # 89
        ["Tue"],                 # 90
        ["Vak"],                 # 91
        ["Ven"],                 # 92
        ["Web"],                 # 93
        ["Wil"],                 # 94
        ["Yor"],                 # 95
        ["Zef"],                 # 96
        ["Zell"],                # 97
        ["Zen"],                 # 98
        ["Zo"],                  # 99
        ["A", "E", "I", "O", "U", "Y"],  # 100 (vowel)
    ]

    TITLE_TABLE: list[list[str]] = [
        ["of the North", "of the South", "of the East", "of the West",
         "of the City", "of the Hills", "of the Mountains", "of the Plains",
         "of the Woods", "of the Coast"],
        ["the Bold", "the Daring"],
        ["the Barbarian", "the Civilized"],
        ["the Battler"],
        ["the Black", "the Blue", "the Brown", "the Green", "the Red", "the Yellow"],
        ["the Fearless", "the Brave"],
        ["the Fair", "the Foul", "the Lovely", "the Loathsome"],
        ["the First", "the Second", "the Third", "the Fourth", "the Fifth",
         "the Sixth", "the Seventh", "the Eighth", "the Ninth", "the Tenth"],
        ["the Gentle", "the Cruel"],
        ["the Great"],
        ["the Merciful", "the Merciless"],
        ["the Mighty"],
        ["the Mysterious", "the Unknown"],
        ["the Old", "the Young"],
        ["the Quick", "the Slow"],
        ["the Quiet", "the Silent", "the Loud"],
        ["the Steady", "the Unready"],
        ["the Traveller", "the Wanderer"],
        ["the Unexpected"],
        ["the Hooded", "the Cloaked", "the Robed"],
    ]
    # fmt: on

    def __init__(self, roller: DiceRoller) -> None:
        self._roller = roller

    def _roll_syllable(self) -> str:
        """Roll d100 and return a random syllable from the table."""
        roll = self._roller.roll(100)
        variants = self.SYLLABLE_TABLE[roll - 1]
        return self._roller.choice(variants)

    def _roll_syllable_count(self) -> int:
        """Roll d100 to determine number of syllables: 1-4."""
        roll = self._roller.roll(100)
        if roll <= 10:
            return 1
        if roll <= 70:
            return 2
        if roll <= 90:
            return 3
        return 4

    def _roll_title(self) -> str:
        """Roll d20 and return a random title."""
        roll = self._roller.roll(20)
        variants = self.TITLE_TABLE[roll - 1]
        return self._roller.choice(variants)

    def generate(self, include_title: bool = False) -> str:
        """Generate a random Holmesian name.

        Args:
            include_title: If True, append a random title (e.g. "the Bold").

        Returns:
            A capitalized character name, optionally with title.
        """
        syllable_count = self._roll_syllable_count()
        syllables = [self._roll_syllable() for _ in range(syllable_count)]

        # First syllable keeps its case, subsequent are lowercased
        name_parts = [syllables[0]] + [s.lower() for s in syllables[1:]]
        name = "".join(name_parts)

        if include_title:
            title = self._roll_title()
            name = f"{name} {title}"

        return name
