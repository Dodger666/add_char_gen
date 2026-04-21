"""Front-end route serving the character sheet HTML page."""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["frontend"])

_HTML_PAGE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OSRIC 3.0 Character Generator</title>
<style>
:root {
  --parchment: #f5f0e1;
  --ink: #2c1810;
  --border: #8b7355;
  --header-bg: #3c2415;
  --header-fg: #f5f0e1;
  --section-bg: #e8dcc8;
  --accent: #6b3a2a;
  --cell-border: #b8a88a;
  --positive: #2d5a1e;
  --negative: #8b1a1a;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: 'Segoe UI', system-ui, sans-serif;
  background: #3c2415;
  color: var(--ink);
  min-height: 100vh;
  padding: 20px;
}
.toolbar {
  max-width: 900px;
  margin: 0 auto 16px;
  display: flex;
  gap: 12px;
  align-items: center;
}
.toolbar button {
  padding: 10px 24px;
  border: 2px solid var(--border);
  background: var(--parchment);
  color: var(--ink);
  font-weight: 700;
  font-size: 14px;
  cursor: pointer;
  transition: background 0.15s;
}
.toolbar button:hover { background: var(--section-bg); }
.toolbar button:disabled { opacity: 0.5; cursor: wait; }
.toolbar label {
  color: var(--parchment);
  font-family: 'Courier New', monospace;
  font-size: 14px;
  font-weight: 700;
}
.toolbar select, .toolbar input[type="number"] {
  background: var(--section-bg);
  color: var(--text-color);
  border: 1px solid var(--border);
  padding: 4px 8px;
  font-family: 'Courier New', monospace;
  font-size: 14px;
}
.toolbar .seed-display {
  margin-left: auto;
  color: var(--parchment);
  font-size: 12px;
  opacity: 0.7;
}
#character-sheet {
  max-width: 900px;
  margin: 0 auto;
  background: var(--parchment);
  border: 3px solid var(--border);
  padding: 24px;
  position: relative;
}
#loading {
  text-align: center;
  padding: 80px 20px;
  font-size: 18px;
  color: var(--accent);
}
#error-display {
  text-align: center;
  padding: 40px 20px;
  color: var(--negative);
  display: none;
}
h1 {
  text-align: center;
  font-size: 22px;
  color: var(--header-bg);
  border-bottom: 2px solid var(--border);
  padding-bottom: 8px;
  margin-bottom: 16px;
  letter-spacing: 2px;
}
.section {
  margin-bottom: 14px;
}
.section-header {
  background: var(--header-bg);
  color: var(--header-fg);
  padding: 4px 10px;
  font-weight: 700;
  font-size: 13px;
  letter-spacing: 1px;
  margin-bottom: 6px;
}
.field-row {
  display: flex;
  flex-wrap: wrap;
  gap: 4px 16px;
  padding: 2px 0;
}
.field {
  display: flex;
  flex-direction: column;
  min-width: 80px;
}
.field-label {
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--accent);
  letter-spacing: 0.5px;
}
.field-value {
  font-size: 14px;
  border-bottom: 1px solid var(--cell-border);
  padding: 1px 0;
  min-height: 20px;
}
.field-value.large {
  font-size: 18px;
  font-weight: 700;
}
.field-wide { flex: 1; min-width: 180px; }
.field-narrow { min-width: 50px; max-width: 70px; }

/* Ability scores grid */
.ability-grid {
  display: grid;
  grid-template-columns: 80px 50px 1fr;
  gap: 2px 8px;
  align-items: center;
}
.ability-name {
  font-weight: 700;
  font-size: 13px;
}
.ability-score {
  font-size: 16px;
  font-weight: 700;
  text-align: center;
  background: var(--section-bg);
  padding: 2px 6px;
  border: 1px solid var(--cell-border);
}
.ability-bonuses {
  display: flex;
  flex-wrap: wrap;
  gap: 2px 10px;
  font-size: 11px;
}
.bonus-item { display: flex; gap: 3px; }
.bonus-label { color: var(--accent); font-weight: 600; }
.bonus-value.positive { color: var(--positive); }
.bonus-value.negative { color: var(--negative); }

/* Saves row */
.saves-row {
  display: flex;
  flex-wrap: wrap;
  gap: 4px 16px;
}
.save-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  min-width: 80px;
}
.save-label {
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--accent);
  text-align: center;
}
.save-value {
  font-size: 16px;
  font-weight: 700;
  background: var(--section-bg);
  border: 1px solid var(--cell-border);
  width: 36px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* To-hit grid */
.to-hit-grid {
  overflow-x: auto;
}
.to-hit-grid table {
  border-collapse: collapse;
  font-size: 11px;
  width: 100%;
}
.to-hit-grid th, .to-hit-grid td {
  border: 1px solid var(--cell-border);
  padding: 2px 4px;
  text-align: center;
  min-width: 28px;
}
.to-hit-grid th {
  background: var(--section-bg);
  font-weight: 700;
}

/* Weapon table */
.weapon-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}
.weapon-table th {
  background: var(--section-bg);
  border: 1px solid var(--cell-border);
  padding: 3px 6px;
  text-align: left;
  font-size: 10px;
  text-transform: uppercase;
  color: var(--accent);
}
.weapon-table td {
  border: 1px solid var(--cell-border);
  padding: 3px 6px;
}

/* Equipment list */
.equip-list {
  columns: 2;
  column-gap: 20px;
  font-size: 12px;
  list-style: none;
  padding: 0;
}
.equip-list li {
  padding: 1px 0;
  break-inside: avoid;
}
.equip-list li::before {
  content: "\\2022 ";
  color: var(--accent);
}

/* Feature / language lists */
.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  list-style: none;
  padding: 0;
}
.tag-list li {
  background: var(--section-bg);
  border: 1px solid var(--cell-border);
  padding: 2px 8px;
  font-size: 11px;
}

/* Thief skills grid */
.thief-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 4px 12px;
}
.thief-skill {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  border-bottom: 1px dotted var(--cell-border);
  padding: 2px 0;
}
.thief-skill-val { font-weight: 700; }

/* Turn undead */
.turn-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12px;
}
.turn-table th {
  background: var(--section-bg);
  border: 1px solid var(--cell-border);
  padding: 3px 6px;
  text-align: left;
  font-size: 10px;
  text-transform: uppercase;
  color: var(--accent);
}
.turn-table td {
  border: 1px solid var(--cell-border);
  padding: 3px 6px;
}

/* Spell section */
.spell-slots-row {
  display: flex;
  gap: 10px;
  margin-bottom: 6px;
}
.spell-slot-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.spell-slot-label {
  font-size: 9px;
  font-weight: 700;
  color: var(--accent);
}
.spell-slot-val {
  font-size: 14px;
  font-weight: 700;
  background: var(--section-bg);
  border: 1px solid var(--cell-border);
  width: 30px;
  text-align: center;
}

/* Page 2 marker */
.page-break {
  border-top: 2px dashed var(--border);
  margin: 18px 0;
  position: relative;
}
.page-break::after {
  content: "Page 2";
  position: absolute;
  top: -10px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--parchment);
  padding: 0 12px;
  font-size: 11px;
  color: var(--accent);
}

@media (max-width: 640px) {
  body { padding: 8px; }
  #character-sheet { padding: 12px; }
  .ability-grid { grid-template-columns: 60px 40px 1fr; }
  .equip-list { columns: 1; }
  .thief-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>
</head>
<body>

<div class="toolbar">
  <label for="level-select">Level:</label>
  <select id="level-select" onchange="generateCharacter()">
    <option value="1" selected>1</option><option value="2">2</option><option value="3">3</option><option value="4">4</option><option value="5">5</option>
    <option value="6">6</option><option value="7">7</option><option value="8">8</option><option value="9">9</option><option value="10">10</option>
    <option value="11">11</option><option value="12">12</option><option value="13">13</option><option value="14">14</option><option value="15">15</option>
    <option value="16">16</option><option value="17">17</option><option value="18">18</option><option value="19">19</option><option value="20">20</option>
  </select>
  <label for="seed-input">Seed:</label>
  <input type="number" id="seed-input" placeholder="Random" style="width:110px;">
  <button id="generate-new" onclick="generateCharacter()">Generate New Character</button>
  <button id="download-pdf" onclick="downloadPdf()" disabled>Download PDF</button>
  <span class="seed-display" id="seed-display"></span>
</div>

<div id="character-sheet">
  <div id="loading">Rolling dice&hellip;</div>
  <div id="error-display"></div>
  <div id="sheet-content" style="display:none">

    <h1>OSRIC 3.0 Character Sheet</h1>

    <!-- Character Information -->
    <div class="section">
      <div class="section-header">Character Information</div>
      <div class="field-row">
        <div class="field field-wide"><span class="field-label">Name</span><span class="field-value large" id="f-name"></span></div>
        <div class="field"><span class="field-label">Class</span><span class="field-value" id="f-class"></span></div>
        <div class="field field-narrow"><span class="field-label">Level</span><span class="field-value" id="f-level"></span></div>
      </div>
      <div class="field-row">
        <div class="field"><span class="field-label">Ancestry</span><span class="field-value" id="f-ancestry"></span></div>
        <div class="field"><span class="field-label">Alignment</span><span class="field-value" id="f-alignment"></span></div>
        <div class="field"><span class="field-label">Gender</span><span class="field-value" id="f-gender"></span></div>
      </div>
      <div class="field-row">
        <div class="field field-narrow"><span class="field-label">HP</span><span class="field-value large" id="f-hp"></span></div>
        <div class="field field-narrow"><span class="field-label">AC</span><span class="field-value large" id="f-ac"></span></div>
        <div class="field field-narrow"><span class="field-label">XP</span><span class="field-value" id="f-xp"></span></div>
        <div class="field field-narrow"><span class="field-label">XP Bonus</span><span class="field-value" id="f-xp-bonus"></span></div>
        <div class="field field-narrow"><span class="field-label">Age</span><span class="field-value" id="f-age"></span></div>
        <div class="field"><span class="field-label">Height</span><span class="field-value" id="f-height"></span></div>
        <div class="field field-narrow"><span class="field-label">Weight</span><span class="field-value" id="f-weight"></span></div>
      </div>
    </div>

    <!-- Ability Scores -->
    <div class="section">
      <div class="section-header">Ability Scores</div>
      <div class="ability-grid" id="ability-grid"></div>
    </div>

    <!-- Saving Throws -->
    <div class="section">
      <div class="section-header">Saving Throws</div>
      <div class="saves-row" id="saves-row"></div>
    </div>

    <!-- Combat -->
    <div class="section">
      <div class="section-header">Combat</div>
      <div class="field-row">
        <div class="field field-narrow"><span class="field-label">THAC0</span><span class="field-value large" id="f-thac0"></span></div>
        <div class="field field-narrow"><span class="field-label">BTHB</span><span class="field-value large" id="f-bthb"></span></div>
        <div class="field field-narrow"><span class="field-label">Melee To-Hit</span><span class="field-value" id="f-melee-hit"></span></div>
        <div class="field field-narrow"><span class="field-label">Missile To-Hit</span><span class="field-value" id="f-missile-hit"></span></div>
      </div>
      <div class="to-hit-grid" id="to-hit-grid"></div>
    </div>

    <!-- Weapons -->
    <div class="section">
      <div class="section-header">Weapons</div>
      <div id="weapons-container"></div>
    </div>

    <!-- Armour -->
    <div class="section">
      <div class="section-header">Armour / Protection</div>
      <div class="field-row" id="armour-row"></div>
    </div>

    <!-- Equipment -->
    <div class="section">
      <div class="section-header">Equipment</div>
      <ul class="equip-list" id="equipment-list"></ul>
    </div>

    <!-- Magical Items -->
    <div class="section" id="section-magical-items" style="display:none">
      <div class="section-header">Magical Items</div>
      <ul class="equip-list" id="magical-items-list"></ul>
    </div>

    <!-- Movement -->
    <div class="section">
      <div class="field-row">
        <div class="field"><span class="field-label">Movement</span><span class="field-value" id="f-movement"></span></div>
        <div class="field"><span class="field-label">Base</span><span class="field-value" id="f-base-move"></span></div>
        <div class="field"><span class="field-label">Encumbrance</span><span class="field-value" id="f-encumbrance"></span></div>
        <div class="field"><span class="field-label">Total Weight</span><span class="field-value" id="f-total-weight"></span></div>
      </div>
    </div>

    <div class="page-break"></div>

    <!-- Wealth -->
    <div class="section">
      <div class="section-header">Wealth</div>
      <div class="field-row">
        <div class="field"><span class="field-label">Gold Remaining</span><span class="field-value large" id="f-gold"></span></div>
      </div>
    </div>

    <!-- Ancestry Features -->
    <div class="section" id="section-ancestry-features" style="display:none">
      <div class="section-header">Special Abilities (Ancestry)</div>
      <ul class="tag-list" id="ancestry-features"></ul>
    </div>

    <!-- Class Features -->
    <div class="section" id="section-class-features" style="display:none">
      <div class="section-header">Special Abilities (Class)</div>
      <ul class="tag-list" id="class-features"></ul>
    </div>

    <!-- Thief Skills -->
    <div class="section" id="section-thief-skills" style="display:none">
      <div class="section-header">Thief Skills</div>
      <div class="thief-grid" id="thief-skills-grid"></div>
    </div>

    <!-- Turn Undead -->
    <div class="section" id="section-turn-undead" style="display:none">
      <div class="section-header">Turn Undead</div>
      <div id="turn-undead-container"></div>
    </div>

    <!-- Spells -->
    <div class="section" id="section-spells" style="display:none">
      <div class="section-header">Spells</div>
      <div id="spell-slots-row" class="spell-slots-row"></div>
      <div id="spells-memorized-container"></div>
      <div id="spellbook-container"></div>
    </div>

    <!-- Weapon Proficiencies -->
    <div class="section" id="section-weapon-profs" style="display:none">
      <div class="section-header">Weapon Proficiencies</div>
      <ul class="tag-list" id="weapon-profs"></ul>
    </div>

    <!-- Languages -->
    <div class="section">
      <div class="section-header">Languages</div>
      <ul class="tag-list" id="languages"></ul>
    </div>

  </div>
</div>

<script>
let currentSeed = null;

function escapeHtml(text) {
  const d = document.createElement('div');
  d.textContent = String(text);
  return d.innerHTML;
}

function signStr(n) {
  return n >= 0 ? '+' + n : String(n);
}

function bonusClass(n) {
  if (n > 0) return 'positive';
  if (n < 0) return 'negative';
  return '';
}

async function generateCharacter() {
  const btn = document.getElementById('generate-new');
  const pdfBtn = document.getElementById('download-pdf');
  const loading = document.getElementById('loading');
  const errorEl = document.getElementById('error-display');
  const content = document.getElementById('sheet-content');

  btn.disabled = true;
  pdfBtn.disabled = true;
  loading.style.display = 'block';
  errorEl.style.display = 'none';
  content.style.display = 'none';

  try {
    const level = document.getElementById('level-select').value;
    const seedInput = document.getElementById('seed-input').value.trim();
    let url = '/api/v1/characters/generate?level=' + level;
    if (seedInput !== '') url += '&seed=' + encodeURIComponent(seedInput);
    const resp = await fetch(url);
    if (!resp.ok) throw new Error('Generation failed: ' + resp.status);
    const data = await resp.json();
    currentSeed = data.character.generation_seed;
    document.getElementById('seed-display').textContent = 'Seed: ' + currentSeed;
    document.getElementById('seed-input').value = '';
    renderCharacter(data.character);
    loading.style.display = 'none';
    content.style.display = 'block';
    pdfBtn.disabled = false;
  } catch (e) {
    loading.style.display = 'none';
    errorEl.textContent = 'Failed to generate character. ' + e.message;
    errorEl.style.display = 'block';
  } finally {
    btn.disabled = false;
  }
}

function downloadPdf() {
  if (currentSeed === null) return;
  const level = document.getElementById('level-select').value;
  window.open('/api/v1/characters/generate/pdf?seed=' + encodeURIComponent(currentSeed) + '&level=' + level, '_blank');
}

function renderCharacter(c) {
  // Character info
  document.getElementById('f-name').textContent = c.name;
  document.getElementById('f-class').textContent = c.character_class;
  document.getElementById('f-level').textContent = c.level;
  document.getElementById('f-ancestry').textContent = c.ancestry;
  document.getElementById('f-alignment').textContent = c.alignment;
  document.getElementById('f-gender').textContent = c.physical.gender;
  document.getElementById('f-hp').textContent = c.hit_points;
  document.getElementById('f-ac').textContent = c.armor_class_desc + ' [' + c.armor_class_asc + ']';
  document.getElementById('f-xp').textContent = c.xp;
  document.getElementById('f-xp-bonus').textContent = c.xp_bonus_pct + '%';
  document.getElementById('f-age').textContent = c.physical.age;
  document.getElementById('f-height').textContent = c.physical.height_display;
  document.getElementById('f-weight').textContent = c.physical.weight_lbs + ' lbs';

  // Ability Scores
  renderAbilities(c);

  // Saving Throws
  renderSaves(c.saving_throws);

  // Combat
  document.getElementById('f-thac0').textContent = c.thac0;
  document.getElementById('f-bthb').textContent = c.bthb;
  document.getElementById('f-melee-hit').textContent = signStr(c.melee_to_hit_mod);
  document.getElementById('f-missile-hit').textContent = signStr(c.missile_to_hit_mod);
  renderToHitGrid(c.thac0);

  // Weapons
  renderWeapons(c.weapons);

  // Armour
  renderArmour(c);

  // Equipment
  renderEquipment(c.equipment);

  // Magical Items
  renderMagicalItems(c.magical_items);

  // Movement
  document.getElementById('f-movement').textContent = c.effective_movement + ' ft';
  document.getElementById('f-base-move').textContent = c.base_movement + ' ft';
  document.getElementById('f-encumbrance').textContent = c.encumbrance_status;
  document.getElementById('f-total-weight').textContent = c.total_weight_lbs + ' lbs';

  // Gold
  document.getElementById('f-gold').textContent = c.gold_remaining.toFixed(2) + ' gp';

  // Ancestry features
  renderTagList('section-ancestry-features', 'ancestry-features', c.ancestry_features);
  renderTagList('section-class-features', 'class-features', c.class_features);

  // Thief skills
  if (c.thief_skills) {
    document.getElementById('section-thief-skills').style.display = '';
    renderThiefSkills(c.thief_skills);
  } else {
    document.getElementById('section-thief-skills').style.display = 'none';
  }

  // Turn undead
  if (c.turn_undead && c.turn_undead.length > 0) {
    document.getElementById('section-turn-undead').style.display = '';
    renderTurnUndead(c.turn_undead);
  } else {
    document.getElementById('section-turn-undead').style.display = 'none';
  }

  // Spells
  if (c.spell_slots || (c.spells_memorized && c.spells_memorized.length > 0)) {
    document.getElementById('section-spells').style.display = '';
    renderSpells(c);
  } else {
    document.getElementById('section-spells').style.display = 'none';
  }

  // Weapon proficiencies
  renderTagList('section-weapon-profs', 'weapon-profs', c.weapon_proficiencies);

  // Languages
  const langList = document.getElementById('languages');
  langList.innerHTML = '';
  (c.languages || []).forEach(function(l) {
    const li = document.createElement('li');
    li.textContent = l;
    langList.appendChild(li);
  });
}

function renderAbilities(c) {
  const s = c.ability_scores;
  const b = c.ability_bonuses;
  const grid = document.getElementById('ability-grid');
  grid.innerHTML = '';

  const abilities = [
    { name: 'STR', score: s.strength, exc: s.exceptional_strength, bonuses: [
      ['To-Hit', signStr(b.str_to_hit)], ['Dmg', signStr(b.str_damage)],
      ['Enc', String(b.str_encumbrance)], ['Minor', b.str_minor_test], ['Major', b.str_major_test]
    ]},
    { name: 'DEX', score: s.dexterity, bonuses: [
      ['AC Adj', signStr(b.dex_ac_adj)], ['Missile', signStr(b.dex_missile_to_hit)], ['Init', signStr(b.dex_initiative)]
    ]},
    { name: 'CON', score: s.constitution, bonuses: [
      ['HP', signStr(b.con_hp_mod)], ['Res%', String(b.con_resurrection)], ['Shock%', String(b.con_system_shock)]
    ]},
    { name: 'INT', score: s.intelligence, bonuses: [['Languages', String(b.int_max_languages)]] },
    { name: 'WIS', score: s.wisdom, bonuses: [['Mental Save', signStr(b.wis_mental_save)]] },
    { name: 'CHA', score: s.charisma, bonuses: [
      ['Henchmen', String(b.cha_sidekick_limit)], ['Loyalty', signStr(b.cha_loyalty_mod)], ['Reaction', signStr(b.cha_reaction_mod)]
    ]}
  ];

  abilities.forEach(function(a) {
    const nameEl = document.createElement('div');
    nameEl.className = 'ability-name';
    nameEl.textContent = a.name;
    grid.appendChild(nameEl);

    const scoreEl = document.createElement('div');
    scoreEl.className = 'ability-score';
    let scoreText = String(a.score);
    if (a.exc) scoreText += '.' + String(a.exc).padStart(2, '0');
    scoreEl.textContent = scoreText;
    grid.appendChild(scoreEl);

    const bonusEl = document.createElement('div');
    bonusEl.className = 'ability-bonuses';
    a.bonuses.forEach(function(pair) {
      const item = document.createElement('span');
      item.className = 'bonus-item';
      const label = document.createElement('span');
      label.className = 'bonus-label';
      label.textContent = pair[0] + ':';
      const val = document.createElement('span');
      val.className = 'bonus-value';
      val.textContent = pair[1];
      if (pair[1].startsWith('+') && pair[1] !== '+0') val.classList.add('positive');
      else if (pair[1].startsWith('-')) val.classList.add('negative');
      item.appendChild(label);
      item.appendChild(val);
      bonusEl.appendChild(item);
    });
    grid.appendChild(bonusEl);
  });
}

function renderSaves(saves) {
  const row = document.getElementById('saves-row');
  row.innerHTML = '';
  const items = [
    ['Aimed Magic', saves.aimed_magic_items],
    ['Breath', saves.breath_weapons],
    ['Death/Para/Poison', saves.death_paralysis_poison],
    ['Petrification', saves.petrifaction_polymorph],
    ['Spells', saves.spells]
  ];
  items.forEach(function(pair) {
    const el = document.createElement('div');
    el.className = 'save-item';
    el.innerHTML = '<span class="save-label">' + escapeHtml(pair[0]) + '</span><span class="save-value">' + escapeHtml(pair[1]) + '</span>';
    row.appendChild(el);
  });
}

function renderToHitGrid(thac0) {
  const container = document.getElementById('to-hit-grid');
  let html = '<table><tr><th>AC</th>';
  for (let ac = 10; ac >= -10; ac--) {
    html += '<th>' + ac + '</th>';
  }
  html += '</tr><tr><td><strong>Roll</strong></td>';
  for (let ac = 10; ac >= -10; ac--) {
    let roll = thac0 - ac;
    roll = Math.min(20, Math.max(1, roll));
    html += '<td>' + roll + '</td>';
  }
  html += '</tr></table>';
  container.innerHTML = html;
}

function renderWeapons(weapons) {
  const container = document.getElementById('weapons-container');
  if (!weapons || weapons.length === 0) {
    container.innerHTML = '<em>None</em>';
    return;
  }
  let html = '<table class="weapon-table"><thead><tr>' +
    '<th>Weapon</th><th>Dmg S/M</th><th>Dmg L</th><th>Weight</th><th>To-Hit</th><th>Type</th>' +
    '</tr></thead><tbody>';
  weapons.forEach(function(w) {
    html += '<tr><td>' + escapeHtml(w.name) + '</td><td>' + escapeHtml(w.damage_vs_sm) +
      '</td><td>' + escapeHtml(w.damage_vs_l) + '</td><td>' + w.weight +
      '</td><td>' + signStr(w.to_hit_modifier) + '</td><td>' + escapeHtml(w.weapon_type) + '</td></tr>';
  });
  html += '</tbody></table>';
  container.innerHTML = html;
}

function renderArmour(c) {
  const row = document.getElementById('armour-row');
  row.innerHTML = '';
  if (c.armor) {
    row.innerHTML += '<div class="field"><span class="field-label">Armour</span><span class="field-value">' +
      escapeHtml(c.armor.name) + ' (AC ' + c.armor.ac_desc + ')</span></div>';
  } else {
    row.innerHTML += '<div class="field"><span class="field-label">Armour</span><span class="field-value">None</span></div>';
  }
  if (c.shield) {
    row.innerHTML += '<div class="field"><span class="field-label">Shield</span><span class="field-value">' +
      escapeHtml(c.shield.name) + '</span></div>';
  }
}

function renderEquipment(equipment) {
  const list = document.getElementById('equipment-list');
  list.innerHTML = '';
  (equipment || []).forEach(function(item) {
    const li = document.createElement('li');
    let text = item.name;
    if (item.weight > 0) text += ' (' + item.weight + ' lbs)';
    li.textContent = text;
    list.appendChild(li);
  });
}

function renderMagicalItems(items) {
  const section = document.getElementById('section-magical-items');
  const list = document.getElementById('magical-items-list');
  if (!items || items.length === 0) {
    section.style.display = 'none';
    return;
  }
  section.style.display = '';
  list.innerHTML = '';
  items.forEach(function(item) {
    const li = document.createElement('li');
    let text = item.name;
    if (item.equipped) text += ' (equipped)';
    li.textContent = text;
    list.appendChild(li);
  });
}

function renderTagList(sectionId, listId, items) {
  const section = document.getElementById(sectionId);
  const list = document.getElementById(listId);
  if (!items || items.length === 0) {
    section.style.display = 'none';
    return;
  }
  section.style.display = '';
  list.innerHTML = '';
  items.forEach(function(t) {
    const li = document.createElement('li');
    li.textContent = t;
    list.appendChild(li);
  });
}

function renderThiefSkills(skills) {
  const grid = document.getElementById('thief-skills-grid');
  grid.innerHTML = '';
  const entries = [
    ['Climb', skills.climb], ['Hide', skills.hide],
    ['Listen', skills.listen], ['Pick Locks', skills.pick_locks],
    ['Pick Pockets', skills.pick_pockets], ['Read Languages', skills.read_languages],
    ['Move Quietly', skills.move_quietly], ['Traps', skills.traps]
  ];
  entries.forEach(function(pair) {
    const el = document.createElement('div');
    el.className = 'thief-skill';
    el.innerHTML = '<span>' + escapeHtml(pair[0]) + '</span><span class="thief-skill-val">' + pair[1] + '%</span>';
    grid.appendChild(el);
  });
}

function renderTurnUndead(entries) {
  const container = document.getElementById('turn-undead-container');
  let html = '<table class="turn-table"><thead><tr><th>Undead Type</th><th>Example</th><th>Roll Needed</th></tr></thead><tbody>';
  entries.forEach(function(e) {
    html += '<tr><td>' + escapeHtml(e.undead_type) + '</td><td>' + escapeHtml(e.example) +
      '</td><td>' + escapeHtml(e.roll_needed) + '</td></tr>';
  });
  html += '</tbody></table>';
  container.innerHTML = html;
}

function renderSpells(c) {
  const slotsRow = document.getElementById('spell-slots-row');
  slotsRow.innerHTML = '';
  if (c.spell_slots) {
    for (let lvl = 1; lvl <= 7; lvl++) {
      const val = c.spell_slots['level_' + lvl];
      if (val > 0) {
        slotsRow.innerHTML += '<div class="spell-slot-item"><span class="spell-slot-label">Level ' + lvl +
          '</span><span class="spell-slot-val">' + val + '</span></div>';
      }
    }
  }

  const memContainer = document.getElementById('spells-memorized-container');
  if (c.spells_memorized && c.spells_memorized.length > 0) {
    let html = '<div style="margin-top:6px"><strong style="font-size:11px;color:var(--accent)">SPELLS MEMORIZED</strong><ul class="tag-list">';
    c.spells_memorized.forEach(function(s) { html += '<li>' + escapeHtml(s) + '</li>'; });
    html += '</ul></div>';
    memContainer.innerHTML = html;
  } else {
    memContainer.innerHTML = '';
  }

  const bookContainer = document.getElementById('spellbook-container');
  if (c.spellbook && c.spellbook.length > 0) {
    let html = '<div style="margin-top:6px"><strong style="font-size:11px;color:var(--accent)">SPELLBOOK</strong><ul class="tag-list">';
    c.spellbook.forEach(function(s) { html += '<li>' + escapeHtml(s) + '</li>'; });
    html += '</ul></div>';
    bookContainer.innerHTML = html;
  } else {
    bookContainer.innerHTML = '';
  }
}

// Auto-generate on page load
generateCharacter();
</script>
</body>
</html>
"""


@router.get("/", response_class=HTMLResponse)
async def character_sheet_page() -> HTMLResponse:
    """Serve the character sheet front-end page."""
    return HTMLResponse(content=_HTML_PAGE)
