"""Fillable PDF character sheet generator for OSRIC 3.0."""

from fpdf import FPDF

from osric_character_gen.models.character import CharacterSheet

# Characters unsupported by Helvetica in fpdf2
_PDF_CHAR_MAP = str.maketrans(
    {
        "\u2014": "-",  # em dash
        "\u2013": "-",  # en dash
        "\u2022": "-",  # bullet
        "\u2018": "'",  # left single quote
        "\u2019": "'",  # right single quote
        "\u201c": '"',  # left double quote
        "\u201d": '"',  # right double quote
    }
)


def _sanitize(text: str) -> str:
    """Replace characters unsupported by Helvetica."""
    return text.translate(_PDF_CHAR_MAP)


class PDFSheetGenerator:
    """Generates a 2-page fillable PDF replicating the OSRIC 3.0
    Player Character Reference Sheet."""

    PAGE_W = 210  # A4 width mm
    PAGE_H = 297  # A4 height mm
    MARGIN = 10
    FONT_SIZE = 8
    HEADER_FONT_SIZE = 10
    TITLE_FONT_SIZE = 14

    def generate(self, character: CharacterSheet) -> bytes:
        """Generate a complete fillable PDF character sheet."""
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.set_auto_page_break(auto=False)
        self._pdf = pdf

        self._render_page1(character)
        self._render_page2(character)

        return bytes(pdf.output())

    def _render_page1(self, character: CharacterSheet) -> None:
        """Render front page."""
        pdf = self._pdf
        pdf.add_page()
        pdf.set_font("Helvetica", "B", self.TITLE_FONT_SIZE)
        pdf.cell(0, 8, "OSRIC 3.0 Character Sheet", new_x="LMARGIN", new_y="NEXT", align="C")

        # Header section
        self._section_header("Character Information")
        y = pdf.get_y()
        col_w = 62
        self._labeled_field("Name", character.name, self.MARGIN, y, col_w)
        self._labeled_field("Class", character.character_class.value, self.MARGIN + col_w + 2, y, col_w)
        self._labeled_field("Level", str(character.level), self.MARGIN + 2 * (col_w + 2), y, col_w)
        pdf.set_y(y + 10)

        y = pdf.get_y()
        self._labeled_field("Ancestry", character.ancestry.value, self.MARGIN, y, col_w)
        self._labeled_field("Alignment", character.alignment.value, self.MARGIN + col_w + 2, y, col_w)
        self._labeled_field("Gender", character.physical.gender.value, self.MARGIN + 2 * (col_w + 2), y, col_w)
        pdf.set_y(y + 10)

        y = pdf.get_y()
        self._labeled_field("HP", str(character.hit_points), self.MARGIN, y, 30)
        ac_str = f"{character.armor_class_desc} [{character.armor_class_asc}]"
        self._labeled_field("AC", ac_str, self.MARGIN + 32, y, 30)
        self._labeled_field("XP", str(character.xp), self.MARGIN + 64, y, 30)
        self._labeled_field("XP Bonus", f"{character.xp_bonus_pct}%", self.MARGIN + 96, y, 30)
        self._labeled_field("Age", str(character.physical.age), self.MARGIN + 128, y, 30)
        self._labeled_field("Height", character.physical.height_display, self.MARGIN + 160, y, 30)
        pdf.set_y(y + 10)

        # Ability Scores
        self._section_header("Ability Scores")
        self._render_ability_scores(character)

        # Saving Throws
        self._section_header("Saving Throws")
        self._render_saving_throws(character)

        # Combat
        self._section_header("Combat")
        y = pdf.get_y()
        self._labeled_field("THAC0", str(character.thac0), self.MARGIN, y, 30)
        self._labeled_field("BTHB", str(character.bthb), self.MARGIN + 32, y, 30)
        self._labeled_field("Melee To-Hit", f"{character.melee_to_hit_mod:+d}", self.MARGIN + 64, y, 35)
        self._labeled_field("Missile To-Hit", f"{character.missile_to_hit_mod:+d}", self.MARGIN + 101, y, 35)
        pdf.set_y(y + 10)

        # To-Hit Grid
        self._render_to_hit_grid(character)

        # Weapons
        self._section_header("Weapons")
        self._render_weapons(character)

        # Armour
        self._section_header("Armour / Protection")
        y = pdf.get_y()
        if character.armor:
            self._labeled_field("Armour", f"{character.armor.name} (AC {character.armor.ac_desc})", self.MARGIN, y, 90)
        else:
            self._labeled_field("Armour", "None", self.MARGIN, y, 90)
        if character.shield:
            self._labeled_field("Shield", character.shield.name, self.MARGIN + 92, y, 60)
        pdf.set_y(y + 10)

        # Equipment
        self._section_header("Equipment")
        self._render_equipment_list(character)

        # Magical Items
        if character.magical_items:
            self._section_header("Magical Items")
            self._render_magical_items(character)

        # Movement / Encumbrance
        y = pdf.get_y()
        self._labeled_field("Movement", f"{character.effective_movement} ft", self.MARGIN, y, 40)
        self._labeled_field("Base", f"{character.base_movement} ft", self.MARGIN + 42, y, 30)
        self._labeled_field("Encumbrance", character.encumbrance_status, self.MARGIN + 74, y, 40)
        self._labeled_field("Weight", f"{character.total_weight_lbs} lbs", self.MARGIN + 116, y, 35)
        pdf.set_y(y + 10)

    def _render_page2(self, character: CharacterSheet) -> None:
        """Render back page."""
        pdf = self._pdf
        pdf.add_page()
        pdf.set_font("Helvetica", "B", self.TITLE_FONT_SIZE)
        pdf.cell(0, 8, "OSRIC 3.0 Character Sheet - Page 2", new_x="LMARGIN", new_y="NEXT", align="C")

        # Wealth
        self._section_header("Wealth")
        y = pdf.get_y()
        self._labeled_field("Gold Remaining", f"{character.gold_remaining:.2f} gp", self.MARGIN, y, 60)
        pdf.set_y(y + 10)

        # Special Abilities - Ancestry
        self._section_header("Special Abilities (Ancestry)")
        for feature in character.ancestry_features:
            pdf.set_font("Helvetica", "", self.FONT_SIZE)
            pdf.cell(0, 5, _sanitize(f"  - {feature}"), new_x="LMARGIN", new_y="NEXT")

        # Special Abilities - Class
        self._section_header("Special Abilities (Class)")
        for feature in character.class_features:
            pdf.set_font("Helvetica", "", self.FONT_SIZE)
            pdf.cell(0, 5, _sanitize(f"  - {feature}"), new_x="LMARGIN", new_y="NEXT")

        # Thief Skills
        if character.thief_skills:
            self._section_header("Thief Skills")
            skills = character.thief_skills
            y = pdf.get_y()
            col_w = 45
            row = 0
            for i, (skill, val) in enumerate(
                [
                    ("Climb", skills.climb),
                    ("Hide", skills.hide),
                    ("Listen", skills.listen),
                    ("Pick Locks", skills.pick_locks),
                    ("Pick Pockets", skills.pick_pockets),
                    ("Read Languages", skills.read_languages),
                    ("Move Quietly", skills.move_quietly),
                    ("Traps", skills.traps),
                ]
            ):
                col = i % 4
                if i > 0 and col == 0:
                    row += 1
                x = self.MARGIN + col * (col_w + 2)
                self._labeled_field(skill, f"{val}%", x, y + row * 10, col_w)
            pdf.set_y(y + (row + 1) * 10)

        # Turn Undead
        if character.turn_undead:
            self._section_header("Turn Undead")
            for entry in character.turn_undead:
                pdf.set_font("Helvetica", "", self.FONT_SIZE)
                pdf.cell(
                    0,
                    5,
                    _sanitize(f"  {entry.undead_type} ({entry.example}): {entry.roll_needed}"),
                    new_x="LMARGIN",
                    new_y="NEXT",
                )

        # Spells
        if character.spell_slots:
            self._section_header("Spell Slots")
            slots = character.spell_slots
            y = pdf.get_y()
            for lvl in range(1, 8):
                val = getattr(slots, f"level_{lvl}")
                if val > 0:
                    self._labeled_field(f"Level {lvl}", str(val), self.MARGIN, y, 40)
                    y += 8
            pdf.set_y(y)

        if character.spells_memorized:
            self._section_header("Spells Memorized")
            for spell in character.spells_memorized:
                pdf.set_font("Helvetica", "", self.FONT_SIZE)
                pdf.cell(0, 5, _sanitize(f"  - {spell}"), new_x="LMARGIN", new_y="NEXT")

        if character.spellbook:
            self._section_header("Spellbook")
            for spell in character.spellbook:
                pdf.set_font("Helvetica", "", self.FONT_SIZE)
                pdf.cell(0, 5, _sanitize(f"  - {spell}"), new_x="LMARGIN", new_y="NEXT")

        # Weapon Proficiencies
        if character.weapon_proficiencies:
            self._section_header("Weapon Proficiencies")
            for prof in character.weapon_proficiencies:
                pdf.set_font("Helvetica", "", self.FONT_SIZE)
                pdf.cell(0, 5, _sanitize(f"  - {prof}"), new_x="LMARGIN", new_y="NEXT")

        # Languages
        self._section_header("Languages")
        for lang in character.languages:
            pdf.set_font("Helvetica", "", self.FONT_SIZE)
            pdf.cell(0, 5, _sanitize(f"  - {lang}"), new_x="LMARGIN", new_y="NEXT")

        # Notes
        self._section_header("Notes")
        pdf.set_font("Helvetica", "", self.FONT_SIZE)
        # Empty bordered box for notes
        y = pdf.get_y()
        remaining = self.PAGE_H - y - self.MARGIN
        if remaining > 20:
            pdf.rect(self.MARGIN, y, self.PAGE_W - 2 * self.MARGIN, remaining)

    def _section_header(self, title: str) -> None:
        pdf = self._pdf
        pdf.set_font("Helvetica", "B", self.HEADER_FONT_SIZE)
        pdf.set_fill_color(220, 220, 220)
        pdf.cell(0, 7, f"  {title}", new_x="LMARGIN", new_y="NEXT", fill=True)
        pdf.set_y(pdf.get_y() + 1)

    def _labeled_field(self, label: str, value: str, x: float, y: float, w: float) -> None:
        pdf = self._pdf
        pdf.set_xy(x, y)
        pdf.set_font("Helvetica", "B", 6)
        pdf.cell(w, 4, _sanitize(label))
        pdf.set_xy(x, y + 3)
        pdf.set_font("Helvetica", "", self.FONT_SIZE)
        pdf.cell(w, 5, _sanitize(value))

    def _render_ability_scores(self, character: CharacterSheet) -> None:
        pdf = self._pdf
        scores = character.ability_scores
        bonuses = character.ability_bonuses
        y = pdf.get_y()
        col_w = 30

        abilities = [
            (
                "STR",
                str(scores.strength) + (f".{scores.exceptional_strength:02d}" if scores.exceptional_strength else ""),
                [
                    ("To-Hit", f"{bonuses.str_to_hit:+d}"),
                    ("Dmg", f"{bonuses.str_damage:+d}"),
                    ("Enc", str(bonuses.str_encumbrance)),
                    ("Minor", bonuses.str_minor_test),
                    ("Major", bonuses.str_major_test),
                ],
            ),
            (
                "DEX",
                str(scores.dexterity),
                [
                    ("AC Adj", f"{bonuses.dex_ac_adj:+d}"),
                    ("Missile", f"{bonuses.dex_missile_to_hit:+d}"),
                    ("Init", f"{bonuses.dex_initiative:+d}"),
                ],
            ),
            (
                "CON",
                str(scores.constitution),
                [
                    ("HP", f"{bonuses.con_hp_mod:+d}"),
                    ("Res%", str(bonuses.con_resurrection)),
                    ("Shock%", str(bonuses.con_system_shock)),
                ],
            ),
            ("INT", str(scores.intelligence), [("Languages", str(bonuses.int_max_languages))]),
            ("WIS", str(scores.wisdom), [("Mental Save", f"{bonuses.wis_mental_save:+d}")]),
            (
                "CHA",
                str(scores.charisma),
                [
                    ("Henchmen", str(bonuses.cha_sidekick_limit)),
                    ("Loyalty", f"{bonuses.cha_loyalty_mod:+d}"),
                    ("Reaction", f"{bonuses.cha_reaction_mod:+d}"),
                ],
            ),
        ]

        for i, (name, score_val, derived) in enumerate(abilities):
            row_y = y + i * 10
            self._labeled_field(name, score_val, self.MARGIN, row_y, 20)
            for j, (dlabel, dval) in enumerate(derived):
                dx = self.MARGIN + 22 + j * col_w
                self._labeled_field(dlabel, dval, dx, row_y, col_w - 2)

        pdf.set_y(y + len(abilities) * 10)

    def _render_saving_throws(self, character: CharacterSheet) -> None:
        pdf = self._pdf
        saves = character.saving_throws
        y = pdf.get_y()
        col_w = 36

        save_list = [
            ("Aimed Magic", saves.aimed_magic_items),
            ("Breath", saves.breath_weapons),
            ("Death/Para/Poison", saves.death_paralysis_poison),
            ("Petrification", saves.petrifaction_polymorph),
            ("Spells", saves.spells),
        ]

        for i, (name, val) in enumerate(save_list):
            x = self.MARGIN + i * (col_w + 2)
            self._labeled_field(name, str(val), x, y, col_w)

        pdf.set_y(y + 10)

    def _render_to_hit_grid(self, character: CharacterSheet) -> None:
        """Render the Roll Required to Hit Armour Class grid."""
        pdf = self._pdf
        y = pdf.get_y()
        pdf.set_font("Helvetica", "B", 6)

        cell_w = 8.5
        start_x = self.MARGIN

        # Header row: AC values
        for ac in range(10, -11, -1):
            x = start_x + (10 - ac) * cell_w
            pdf.set_xy(x, y)
            pdf.cell(cell_w, 4, str(ac), align="C")

        # Values row: roll needed = THAC0 - AC
        y += 4
        pdf.set_font("Helvetica", "", 7)
        for ac in range(10, -11, -1):
            roll = character.thac0 - ac
            roll_display = str(min(20, max(1, roll)))
            x = start_x + (10 - ac) * cell_w
            pdf.set_xy(x, y)
            pdf.cell(cell_w, 4, roll_display, align="C", border=1)

        pdf.set_y(y + 6)

    def _render_weapons(self, character: CharacterSheet) -> None:
        pdf = self._pdf
        if not character.weapons:
            pdf.set_font("Helvetica", "", self.FONT_SIZE)
            pdf.cell(0, 5, "  None", new_x="LMARGIN", new_y="NEXT")
            return

        # Header
        y = pdf.get_y()
        pdf.set_font("Helvetica", "B", 6)
        headers = ["Weapon", "Dmg S/M", "Dmg L", "Weight", "To-Hit", "Type"]
        widths = [50, 25, 25, 20, 20, 25]
        x = self.MARGIN
        for h, w in zip(headers, widths, strict=True):
            pdf.set_xy(x, y)
            pdf.cell(w, 4, h)
            x += w

        y += 5
        pdf.set_font("Helvetica", "", self.FONT_SIZE)
        for weapon in character.weapons[:5]:
            x = self.MARGIN
            vals = [
                weapon.name,
                weapon.damage_vs_sm,
                weapon.damage_vs_l,
                f"{weapon.weight:.0f}",
                f"{weapon.to_hit_modifier:+d}",
                weapon.weapon_type,
            ]
            for val, w in zip(vals, widths, strict=True):
                pdf.set_xy(x, y)
                pdf.cell(w, 5, _sanitize(val))
                x += w
            y += 5

        pdf.set_y(y)

    def _render_equipment_list(self, character: CharacterSheet) -> None:
        pdf = self._pdf
        pdf.set_font("Helvetica", "", self.FONT_SIZE)
        for item in character.equipment[:10]:
            weight_str = f" ({item.weight:.0f} lbs)" if item.weight > 0 else ""
            pdf.cell(
                0,
                5,
                _sanitize(f"  - {item.name}{weight_str}"),
                new_x="LMARGIN",
                new_y="NEXT",
            )

    def _render_magical_items(self, character: CharacterSheet) -> None:
        pdf = self._pdf
        pdf.set_font("Helvetica", "", self.FONT_SIZE)
        for item in character.magical_items:
            suffix = " (equipped)" if item.equipped else ""
            pdf.cell(
                0,
                5,
                _sanitize(f"  - {item.name}{suffix}"),
                new_x="LMARGIN",
                new_y="NEXT",
            )
