"""Front-end routes for the character sheet manager pages."""

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["frontend-manager"])

# ---------------------------------------------------------------------------
# Shared CSS & JS (embedded in every page for self-contained delivery)
# ---------------------------------------------------------------------------

_SHARED_CSS = """\
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
  background: var(--parchment);
  color: var(--ink);
  padding: 1rem;
  max-width: 1200px;
  margin: 0 auto;
}
h1, h2, h3 { color: var(--accent); margin-bottom: 0.5rem; }
h1 { font-size: 1.6rem; border-bottom: 2px solid var(--border); padding-bottom: 0.3rem; }
h2 { font-size: 1.2rem; margin-top: 1rem; }
h3 { font-size: 1rem; }
.panel {
  background: var(--section-bg);
  border: 1px solid var(--border);
  border-radius: 6px;
  padding: 1rem;
  margin-bottom: 1rem;
}
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 0.5rem; }
.grid-6 { display: grid; grid-template-columns: repeat(6, 1fr); gap: 0.5rem; }
label { font-weight: 600; font-size: 0.85rem; display: block; margin-bottom: 2px; }
input, select, textarea {
  width: 100%;
  padding: 0.4rem;
  border: 1px solid var(--cell-border);
  border-radius: 4px;
  font-size: 0.9rem;
  background: #fff;
}
input[type="number"] { width: 100%; }
textarea { resize: vertical; min-height: 60px; }
.field { margin-bottom: 0.5rem; }
button {
  padding: 0.5rem 1.2rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
}
.btn-primary { background: var(--accent); color: #fff; }
.btn-primary:hover { background: #8b4a3a; }
.btn-secondary { background: var(--border); color: #fff; }
.btn-secondary:hover { background: #6b5335; }
.btn-danger { background: var(--negative); color: #fff; }
.btn-danger:hover { background: #6b0a0a; }
.btn-row { display: flex; gap: 0.5rem; margin-top: 1rem; flex-wrap: wrap; }
.badge {
  display: inline-block;
  padding: 0.2rem 0.6rem;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 700;
  color: #fff;
}
.badge-green { background: #2d5a1e; }
.badge-yellow { background: #8b7b00; }
.badge-orange { background: #b85c00; }
.badge-red { background: #8b1a1a; }
.badge-darkred { background: #5a0000; animation: pulse 1.5s infinite; }
@keyframes pulse { 0%,100%{opacity:1;} 50%{opacity:0.7;} }
.movement-bar {
  height: 12px;
  border-radius: 6px;
  background: #ddd;
  margin-top: 4px;
  overflow: hidden;
}
.movement-bar-fill {
  height: 100%;
  border-radius: 6px;
  transition: width 0.3s, background 0.3s;
}
.warning-text { color: var(--negative); font-weight: 600; font-size: 0.85rem; margin-top: 4px; }
.enc-panel-warn { border-color: var(--negative) !important; }
.secret-key-modal {
  display: none;
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0,0,0,0.6); z-index: 1000;
  align-items: center; justify-content: center;
}
.secret-key-modal.show { display: flex; }
.modal-content {
  background: var(--parchment);
  border: 2px solid var(--accent);
  border-radius: 8px;
  padding: 2rem;
  max-width: 500px;
  width: 90%;
  text-align: center;
}
.modal-content h2 { color: var(--negative); }
.modal-content .key-display {
  font-family: monospace;
  font-size: 1.1rem;
  background: #fff;
  border: 1px solid var(--border);
  padding: 0.8rem;
  border-radius: 4px;
  margin: 1rem 0;
  word-break: break-all;
  user-select: all;
}
.hidden { display: none; }
table.data-table { width: 100%; border-collapse: collapse; margin-top: 0.5rem; }
table.data-table th, table.data-table td {
  border: 1px solid var(--cell-border); padding: 0.3rem 0.5rem; font-size: 0.85rem;
}
table.data-table th { background: var(--header-bg); color: var(--header-fg); }
table.data-table tr:nth-child(even) { background: rgba(0,0,0,0.03); }
.item-row { display: grid; grid-template-columns: 2fr 1fr 1fr auto; gap: 0.5rem; align-items: end; margin-bottom: 0.3rem; }
.item-row input { font-size: 0.85rem; }
.remove-btn { background: var(--negative); color: #fff; border: none; border-radius: 4px; padding: 0.3rem 0.5rem; cursor: pointer; font-size: 0.8rem; }
"""

_ENCUMBRANCE_JS = """\
// --- Encumbrance & Movement Calculator ---
const STR_ALLOWANCE = {
  3:0, 4:10, 5:10, 6:20, 7:20, 8:35, 9:35, 10:35, 11:35,
  12:45, 13:45, 14:55, 15:55, 16:70, 17:85, 18:110
};
const EXCEPTIONAL_STR = {
  1:135, 25:135, 50:135, 51:160, 75:160, 76:185, 90:185, 91:235, 99:235, 100:300
};
const ARMOR_CAP = {
  'none':120, 'leather':120, 'padded':90, 'studded leather':90, 'ring mail':90,
  'scale':60, 'lamellar':60, 'chain mail':90, 'splint':60, 'banded':90, 'plate mail':60
};
const ANCESTRY_MOVEMENT = {
  'dwarf':90, 'elf':120, 'gnome':90, 'half-elf':120, 'half-orc':120, 'halfling':90, 'human':120
};
const MONK_MOVEMENT = {
  1:150, 2:160, 3:170, 4:180, 5:190, 6:200, 7:210, 8:220,
  9:230, 10:240, 11:250, 12:260, 13:270, 14:280, 15:290, 16:290, 17:290
};
const FIGHTER_TYPES = ['fighter', 'paladin', 'ranger'];

function getStrAllowance() {
  const str = parseInt(document.getElementById('strength')?.value) || 10;
  const charClass = (document.getElementById('character_class')?.value || '').toLowerCase();
  const exceptStr = parseInt(document.getElementById('exceptional_strength')?.value) || 0;
  if (str === 18 && FIGHTER_TYPES.includes(charClass) && exceptStr > 0) {
    const thresholds = [1,25,50,51,75,76,90,91,99,100];
    for (let i = thresholds.length - 1; i >= 0; i--) {
      if (exceptStr >= thresholds[i]) return EXCEPTIONAL_STR[thresholds[i]];
    }
    return 135;
  }
  return STR_ALLOWANCE[str] || (str < 3 ? 0 : 110);
}

function getBaseMovement() {
  const charClass = (document.getElementById('character_class')?.value || '').toLowerCase();
  const ancestry = (document.getElementById('ancestry')?.value || 'human').toLowerCase();
  const level = parseInt(document.getElementById('level')?.value) || 1;
  if (charClass === 'monk') {
    return MONK_MOVEMENT[Math.min(level, 17)] || 150;
  }
  return ANCESTRY_MOVEMENT[ancestry] || 120;
}

function getArmorCap() {
  const armorEl = document.getElementById('equipped_armor');
  if (!armorEl) return 120;
  const armor = armorEl.value.toLowerCase().trim();
  if (!armor || armor === 'none') return 120;
  for (const [key, cap] of Object.entries(ARMOR_CAP)) {
    if (armor.includes(key)) return cap;
  }
  return 120;
}

function getTotalWeight() {
  let total = 0;
  document.querySelectorAll('.item-weight').forEach(el => {
    total += parseFloat(el.value) || 0;
  });
  // Armor & shield weight
  total += parseFloat(document.getElementById('armor_weight')?.value) || 0;
  total += parseFloat(document.getElementById('shield_weight')?.value) || 0;
  // Coin weight: 10 coins = 1 lb
  const coins = ['platinum','gold','electrum','silver','copper'];
  let coinTotal = 0;
  coins.forEach(c => { coinTotal += parseInt(document.getElementById('coin_' + c)?.value) || 0; });
  total += coinTotal / 10;
  return total;
}

function calculateEncumbrance(totalWeight, strAllowance, baseMovement, armorCap) {
  const overage = totalWeight - strAllowance;
  let status, multiplier;
  if (overage <= 0) { status = "Unencumbered"; multiplier = 1.0; }
  else if (overage <= 40) { status = "Light"; multiplier = 0.75; }
  else if (overage <= 80) { status = "Moderate"; multiplier = 0.5; }
  else if (overage <= 120) { status = "Heavy"; multiplier = 0.25; }
  else { status = "Immobile"; multiplier = 0.0; }
  const encMovement = Math.floor(baseMovement * multiplier);
  const effectiveMovement = Math.min(encMovement, armorCap);
  return { status, effectiveMovement, overage: Math.max(0, overage), multiplier };
}

function updateEncumbrancePanel() {
  const strAllowance = getStrAllowance();
  const baseMovement = getBaseMovement();
  const armorCap = getArmorCap();
  const totalWeight = getTotalWeight();
  const result = calculateEncumbrance(totalWeight, strAllowance, baseMovement, armorCap);

  const el = (id) => document.getElementById(id);
  if (el('enc_total_weight')) el('enc_total_weight').textContent = totalWeight.toFixed(1);
  if (el('enc_str_allowance')) el('enc_str_allowance').textContent = strAllowance;
  if (el('enc_overage')) el('enc_overage').textContent = result.overage.toFixed(1);
  if (el('enc_base_movement')) el('enc_base_movement').textContent = baseMovement;
  if (el('enc_armor_cap')) el('enc_armor_cap').textContent = armorCap;
  if (el('enc_effective_movement')) el('enc_effective_movement').textContent = result.effectiveMovement;

  const badge = el('enc_status_badge');
  if (badge) {
    badge.textContent = result.status;
    badge.className = 'badge badge-' + ({
      'Unencumbered':'green','Light':'yellow','Moderate':'orange','Heavy':'red','Immobile':'darkred'
    }[result.status] || 'green');
  }

  const panel = el('encumbrance-panel');
  if (panel) {
    panel.classList.toggle('enc-panel-warn', result.status === 'Heavy' || result.status === 'Immobile');
  }

  const bar = el('enc_bar_fill');
  if (bar && baseMovement > 0) {
    const pct = Math.min(100, (result.effectiveMovement / baseMovement) * 100);
    bar.style.width = pct + '%';
    bar.style.background = {
      'Unencumbered':'#2d5a1e','Light':'#8b7b00','Moderate':'#b85c00','Heavy':'#8b1a1a','Immobile':'#5a0000'
    }[result.status] || '#2d5a1e';
  }

  const warn = el('enc_warning');
  if (warn) {
    if (result.status === 'Heavy') {
      warn.textContent = 'Movement severely reduced. Consider dropping equipment.';
      warn.className = 'warning-text';
    } else if (result.status === 'Immobile') {
      warn.textContent = 'Cannot move! Total weight exceeds carrying capacity by ' + (result.overage - 120).toFixed(0) + ' lbs.';
      warn.className = 'warning-text';
    } else {
      warn.textContent = '';
    }
  }
}
"""

_ENCUMBRANCE_PANEL_HTML = """\
<div class="panel" id="encumbrance-panel">
  <h3>Encumbrance & Movement</h3>
  <div class="grid-3" style="margin-top:0.5rem;">
    <div class="field"><label>Total Weight (lbs)</label><span id="enc_total_weight">0</span></div>
    <div class="field"><label>STR Allowance</label><span id="enc_str_allowance">0</span></div>
    <div class="field"><label>Overage</label><span id="enc_overage">0</span></div>
  </div>
  <div class="grid-3">
    <div class="field"><label>Status</label><span id="enc_status_badge" class="badge badge-green">Unencumbered</span></div>
    <div class="field"><label>Base Movement</label><span id="enc_base_movement">120</span> ft</div>
    <div class="field"><label>Armor Cap</label><span id="enc_armor_cap">120</span> ft</div>
  </div>
  <div class="field">
    <label>Effective Movement: <span id="enc_effective_movement">120</span> ft</label>
    <div class="movement-bar"><div class="movement-bar-fill" id="enc_bar_fill" style="width:100%;background:#2d5a1e;"></div></div>
  </div>
  <div id="enc_warning"></div>
</div>
"""

# ---------------------------------------------------------------------------
# Character Form (shared between new/edit/view)
# ---------------------------------------------------------------------------

_CHARACTER_FORM_HTML = """\
<form id="character-form">
  <div class="panel">
    <h2>Basic Information</h2>
    <div class="grid-3">
      <div class="field"><label>Name</label><input type="text" id="name" name="name" {ro}></div>
      <div class="field">
        <label>Class</label>
        <select id="character_class" name="character_class" {ro}>
          <option value="">-- Select --</option>
          <option value="Fighter">Fighter</option>
          <option value="Cleric">Cleric</option>
          <option value="Magic-User">Magic-User</option>
          <option value="Thief">Thief</option>
          <option value="Paladin">Paladin</option>
          <option value="Ranger">Ranger</option>
          <option value="Druid">Druid</option>
          <option value="Assassin">Assassin</option>
          <option value="Illusionist">Illusionist</option>
          <option value="Monk">Monk</option>
        </select>
      </div>
      <div class="field">
        <label>Ancestry</label>
        <select id="ancestry" name="ancestry" {ro}>
          <option value="">-- Select --</option>
          <option value="Human">Human</option>
          <option value="Dwarf">Dwarf</option>
          <option value="Elf">Elf</option>
          <option value="Gnome">Gnome</option>
          <option value="Half-Elf">Half-Elf</option>
          <option value="Half-Orc">Half-Orc</option>
          <option value="Halfling">Halfling</option>
        </select>
      </div>
    </div>
    <div class="grid-3">
      <div class="field"><label>Level</label><input type="number" id="level" name="level" min="1" max="20" value="1" {ro}></div>
      <div class="field">
        <label>Alignment</label>
        <select id="alignment" name="alignment" {ro}>
          <option value="">-- Select --</option>
          <option value="Lawful Good">Lawful Good</option>
          <option value="Neutral Good">Neutral Good</option>
          <option value="Chaotic Good">Chaotic Good</option>
          <option value="Lawful Neutral">Lawful Neutral</option>
          <option value="True Neutral">True Neutral</option>
          <option value="Chaotic Neutral">Chaotic Neutral</option>
          <option value="Lawful Evil">Lawful Evil</option>
          <option value="Neutral Evil">Neutral Evil</option>
          <option value="Chaotic Evil">Chaotic Evil</option>
        </select>
      </div>
      <div class="field"><label>Hit Points</label><input type="number" id="hit_points" name="hit_points" min="1" value="1" {ro}></div>
    </div>
    <div class="grid-3">
      <div class="field"><label>AC (Descending)</label><input type="number" id="armor_class_desc" name="armor_class_desc" value="10" {ro}></div>
      <div class="field"><label>AC (Ascending)</label><input type="number" id="armor_class_asc" name="armor_class_asc" value="10" {ro}></div>
      <div class="field"><label>THAC0</label><input type="number" id="thac0" name="thac0" value="20" {ro}></div>
    </div>
    <div class="grid-3">
      <div class="field"><label>XP</label><input type="number" id="xp" name="xp" min="0" value="0" {ro}></div>
      <div class="field"><label>XP Bonus %</label><input type="number" id="xp_bonus_pct" name="xp_bonus_pct" min="0" max="10" value="0" {ro}></div>
      <div class="field"><label>BTHB</label><input type="number" id="bthb" name="bthb" value="0" {ro}></div>
    </div>
  </div>

  <div class="panel">
    <h2>Ability Scores</h2>
    <div class="grid-6">
      <div class="field"><label>Strength</label><input type="number" id="strength" name="strength" min="3" max="25" value="10" {ro}></div>
      <div class="field"><label>Dexterity</label><input type="number" id="dexterity" name="dexterity" min="3" max="25" value="10" {ro}></div>
      <div class="field"><label>Constitution</label><input type="number" id="constitution" name="constitution" min="3" max="25" value="10" {ro}></div>
      <div class="field"><label>Intelligence</label><input type="number" id="intelligence" name="intelligence" min="3" max="25" value="10" {ro}></div>
      <div class="field"><label>Wisdom</label><input type="number" id="wisdom" name="wisdom" min="3" max="25" value="10" {ro}></div>
      <div class="field"><label>Charisma</label><input type="number" id="charisma" name="charisma" min="3" max="25" value="10" {ro}></div>
    </div>
    <div class="grid-3">
      <div class="field"><label>Exceptional STR (Fighters 18 only)</label><input type="number" id="exceptional_strength" name="exceptional_strength" min="0" max="100" value="0" {ro}></div>
    </div>
  </div>

  <div class="panel">
    <h2>Physical Characteristics</h2>
    <div class="grid-3">
      <div class="field"><label>Height (inches)</label><input type="number" id="height_inches" name="height_inches" min="36" max="96" value="70" {ro}></div>
      <div class="field"><label>Weight (lbs)</label><input type="number" id="weight_lbs" name="weight_lbs" min="50" max="400" value="170" {ro}></div>
      <div class="field"><label>Age</label><input type="number" id="age" name="age" min="10" max="1000" value="25" {ro}></div>
    </div>
    <div class="grid-3">
      <div class="field">
        <label>Gender</label>
        <select id="gender" name="gender" {ro}>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
        </select>
      </div>
      <div class="field"><label>Age Category</label><input type="text" id="age_category" name="age_category" value="Adult" {ro}></div>
      <div class="field"><label>Height Display</label><input type="text" id="height_display" name="height_display" value="5'10&quot;" {ro}></div>
    </div>
  </div>

  <div class="panel">
    <h2>Saving Throws</h2>
    <div class="grid-3">
      <div class="field"><label>Aimed Magic Items</label><input type="number" id="st_aimed_magic_items" name="st_aimed_magic_items" value="16" {ro}></div>
      <div class="field"><label>Breath Weapons</label><input type="number" id="st_breath_weapons" name="st_breath_weapons" value="17" {ro}></div>
      <div class="field"><label>Death/Paralysis/Poison</label><input type="number" id="st_death_paralysis_poison" name="st_death_paralysis_poison" value="14" {ro}></div>
    </div>
    <div class="grid-3">
      <div class="field"><label>Petrification/Polymorph</label><input type="number" id="st_petrifaction_polymorph" name="st_petrifaction_polymorph" value="15" {ro}></div>
      <div class="field"><label>Spells</label><input type="number" id="st_spells" name="st_spells" value="17" {ro}></div>
    </div>
  </div>

  <div class="panel">
    <h2>Combat Modifiers</h2>
    <div class="grid-3">
      <div class="field"><label>Melee To-Hit Mod</label><input type="number" id="melee_to_hit_mod" name="melee_to_hit_mod" value="0" {ro}></div>
      <div class="field"><label>Missile To-Hit Mod</label><input type="number" id="missile_to_hit_mod" name="missile_to_hit_mod" value="0" {ro}></div>
    </div>
  </div>

  {encumbrance_panel}

  <div class="panel">
    <h2>Equipment</h2>
    <div id="equipment-list">
      <div class="item-row">
        <div><label>Item</label></div><div><label>Weight (lbs)</label></div><div><label>Cost (gp)</label></div><div></div>
      </div>
    </div>
    <button type="button" class="btn-secondary" onclick="addEquipmentRow()" {ro_btn}>+ Add Item</button>
  </div>

  <div class="panel">
    <h2>Weapons</h2>
    <div id="weapons-list">
      <div class="item-row" style="grid-template-columns:2fr 1fr 1fr 1fr 1fr auto;">
        <div><label>Name</label></div><div><label>Dmg S/M</label></div><div><label>Dmg L</label></div><div><label>Weight</label></div><div><label>Cost</label></div><div></div>
      </div>
    </div>
    <button type="button" class="btn-secondary" onclick="addWeaponRow()" {ro_btn}>+ Add Weapon</button>
  </div>

  <div class="panel">
    <h2>Armor</h2>
    <h3 style="font-size:0.95rem;margin-top:0.3rem;">Body Armor</h3>
    <div class="grid-3">
      <div class="field"><label>Name</label><input type="text" id="equipped_armor" name="equipped_armor" placeholder="e.g. Chain Mail" {ro}></div>
      <div class="field"><label>AC (Desc)</label><input type="number" id="armor_ac_desc" name="armor_ac_desc" value="10" {ro}></div>
      <div class="field"><label>AC (Asc)</label><input type="number" id="armor_ac_asc" name="armor_ac_asc" value="10" {ro}></div>
    </div>
    <div class="grid-3">
      <div class="field"><label>Weight (lbs)</label><input type="number" id="armor_weight" name="armor_weight" step="0.5" min="0" value="0" {ro}></div>
      <div class="field"><label>Cost (gp)</label><input type="number" id="armor_cost" name="armor_cost" step="0.1" min="0" value="0" {ro}></div>
      <div class="field"><label>Movement Cap</label><input type="number" id="armor_movement_cap" name="armor_movement_cap" value="120" {ro}></div>
    </div>
    <h3 style="font-size:0.95rem;margin-top:0.6rem;">Shield</h3>
    <div class="grid-3">
      <div class="field"><label>Name</label><input type="text" id="equipped_shield" name="equipped_shield" placeholder="e.g. Large Shield" {ro}></div>
      <div class="field"><label>Weight (lbs)</label><input type="number" id="shield_weight" name="shield_weight" step="0.5" min="0" value="0" {ro}></div>
      <div class="field"><label>Cost (gp)</label><input type="number" id="shield_cost" name="shield_cost" step="0.1" min="0" value="0" {ro}></div>
    </div>
  </div>

  <div class="panel">
    <h2>Coins</h2>
    <div class="grid-3">
      <div class="field"><label>Platinum</label><input type="number" id="coin_platinum" name="coin_platinum" min="0" value="0" {ro}></div>
      <div class="field"><label>Gold</label><input type="number" id="coin_gold" name="coin_gold" min="0" value="0" {ro}></div>
      <div class="field"><label>Electrum</label><input type="number" id="coin_electrum" name="coin_electrum" min="0" value="0" {ro}></div>
    </div>
    <div class="grid-3">
      <div class="field"><label>Silver</label><input type="number" id="coin_silver" name="coin_silver" min="0" value="0" {ro}></div>
      <div class="field"><label>Copper</label><input type="number" id="coin_copper" name="coin_copper" min="0" value="0" {ro}></div>
      <div class="field"><label>Gold Remaining</label><input type="number" id="gold_remaining" name="gold_remaining" min="0" step="0.01" value="0" {ro}></div>
    </div>
  </div>

  <div class="panel">
    <h2>Class Features</h2>
    <div class="grid-2">
      <div class="field"><label>Weapon Proficiencies (comma-separated)</label><textarea id="weapon_proficiencies" name="weapon_proficiencies" rows="2" {ro}></textarea></div>
      <div class="field"><label>Languages (comma-separated)</label><textarea id="languages" name="languages" rows="2" {ro}></textarea></div>
    </div>
    <div class="grid-2">
      <div class="field"><label>Ancestry Features (comma-separated)</label><textarea id="ancestry_features" name="ancestry_features" rows="2" {ro}></textarea></div>
      <div class="field"><label>Class Features (comma-separated)</label><textarea id="class_features" name="class_features" rows="2" {ro}></textarea></div>
    </div>
  </div>

  <div class="panel" id="thief-skills-panel" style="display:none;">
    <h2>Thief Skills</h2>
    <div class="grid-3">
      <div class="field"><label>Climb Walls %</label><input type="number" id="ts_climb" min="1" max="99" {ro}></div>
      <div class="field"><label>Hide in Shadows %</label><input type="number" id="ts_hide" min="1" max="99" {ro}></div>
      <div class="field"><label>Hear Noise %</label><input type="number" id="ts_listen" min="1" max="99" {ro}></div>
    </div>
    <div class="grid-3">
      <div class="field"><label>Pick Locks %</label><input type="number" id="ts_pick_locks" min="1" max="99" {ro}></div>
      <div class="field"><label>Pick Pockets %</label><input type="number" id="ts_pick_pockets" min="1" max="99" {ro}></div>
      <div class="field"><label>Read Languages %</label><input type="number" id="ts_read_languages" min="1" max="99" {ro}></div>
    </div>
    <div class="grid-3">
      <div class="field"><label>Move Quietly %</label><input type="number" id="ts_move_quietly" min="1" max="99" {ro}></div>
      <div class="field"><label>Find/Remove Traps %</label><input type="number" id="ts_traps" min="1" max="99" {ro}></div>
    </div>
  </div>

  <div class="panel" id="spells-panel" style="display:none;">
    <h2>Spells</h2>
    <div class="grid-3">
      <div class="field"><label>Slots Lvl 1</label><input type="number" id="spell_slot_1" min="0" value="0" {ro}></div>
      <div class="field"><label>Slots Lvl 2</label><input type="number" id="spell_slot_2" min="0" value="0" {ro}></div>
      <div class="field"><label>Slots Lvl 3</label><input type="number" id="spell_slot_3" min="0" value="0" {ro}></div>
    </div>
    <div class="grid-3">
      <div class="field"><label>Slots Lvl 4</label><input type="number" id="spell_slot_4" min="0" value="0" {ro}></div>
      <div class="field"><label>Slots Lvl 5</label><input type="number" id="spell_slot_5" min="0" value="0" {ro}></div>
      <div class="field"><label>Slots Lvl 6</label><input type="number" id="spell_slot_6" min="0" value="0" {ro}></div>
    </div>
    <div class="field"><label>Slots Lvl 7</label><input type="number" id="spell_slot_7" min="0" value="0" {ro}></div>
    <div class="field"><label>Spells Memorized (comma-separated)</label><textarea id="spells_memorized" rows="2" {ro}></textarea></div>
    <div class="field"><label>Spellbook (comma-separated)</label><textarea id="spellbook" rows="2" {ro}></textarea></div>
  </div>

  <div class="panel">
    <h2>Notes</h2>
    <textarea id="notes" name="notes" rows="4" placeholder="Character notes..." {ro}></textarea>
  </div>
</form>
"""

# ---------------------------------------------------------------------------
# Equipment/Weapon JS helpers
# ---------------------------------------------------------------------------

_ITEM_JS = """\
function addEquipmentRow(name, weight, cost) {
  const list = document.getElementById('equipment-list');
  const row = document.createElement('div');
  row.className = 'item-row';
  row.innerHTML = `
    <div><input type="text" class="item-name" value="${name||''}" {ro}></div>
    <div><input type="number" class="item-weight" value="${weight||0}" step="0.1" min="0" {ro}></div>
    <div><input type="number" class="item-cost" value="${cost||0}" step="0.1" min="0" {ro}></div>
    <div>{remove_btn}</div>
  `;
  list.appendChild(row);
  row.querySelectorAll('.item-weight').forEach(el => el.addEventListener('input', updateEncumbrancePanel));
}

function addWeaponRow(name, dmgSm, dmgL, weight, cost) {
  const list = document.getElementById('weapons-list');
  const row = document.createElement('div');
  row.className = 'item-row';
  row.style.gridTemplateColumns = '2fr 1fr 1fr 1fr 1fr auto';
  row.innerHTML = `
    <div><input type="text" class="weapon-name" value="${name||''}" {ro}></div>
    <div><input type="text" class="weapon-dmg-sm" value="${dmgSm||'1d6'}" {ro}></div>
    <div><input type="text" class="weapon-dmg-l" value="${dmgL||'1d6'}" {ro}></div>
    <div><input type="number" class="item-weight" value="${weight||0}" step="0.1" min="0" {ro}></div>
    <div><input type="number" class="weapon-cost" value="${cost||0}" step="0.1" min="0" {ro}></div>
    <div>{remove_btn}</div>
  `;
  list.appendChild(row);
  row.querySelectorAll('.item-weight').forEach(el => el.addEventListener('input', updateEncumbrancePanel));
}

function removeRow(btn) {
  btn.closest('.item-row').remove();
  updateEncumbrancePanel();
}

function toggleClassPanels() {
  const cls = (document.getElementById('character_class')?.value || '').toLowerCase();
  const thiefPanel = document.getElementById('thief-skills-panel');
  const spellPanel = document.getElementById('spells-panel');
  const thiefClasses = ['thief', 'assassin'];
  const casterClasses = ['cleric', 'druid', 'magic-user', 'illusionist', 'ranger', 'paladin'];
  if (thiefPanel) thiefPanel.style.display = thiefClasses.includes(cls) ? 'block' : 'none';
  if (spellPanel) spellPanel.style.display = casterClasses.includes(cls) ? 'block' : 'none';
}
"""

# ---------------------------------------------------------------------------
# Save/Load JS
# ---------------------------------------------------------------------------

_SAVE_JS = """\
async function saveCharacter() {
  const data = gatherCharacterData();
  const campaignId = document.getElementById('campaign_id')?.value || null;
  const notes = document.getElementById('notes')?.value || '';
  const body = { character: data };
  if (campaignId) body.campaign_id = campaignId;
  if (notes) body.notes = notes;

  try {
    const resp = await fetch('/api/v1/characters/save', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(body)
    });
    if (!resp.ok) { alert('Save failed: ' + (await resp.text())); return; }
    const result = await resp.json();
    showSecretKeyModal(result.secret_key, result.character_id);
  } catch(e) { alert('Network error: ' + e.message); }
}

async function updateCharacter(secretKey) {
  const data = gatherCharacterData();
  const notes = document.getElementById('notes')?.value || '';
  const body = { character: data };
  if (notes) body.notes = notes;

  try {
    const resp = await fetch('/api/v1/characters/' + secretKey, {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(body)
    });
    if (!resp.ok) { alert('Update failed: ' + (await resp.text())); return; }
    alert('Character saved successfully!');
  } catch(e) { alert('Network error: ' + e.message); }
}

async function loadCharacter(secretKey) {
  try {
    const resp = await fetch('/api/v1/characters/' + secretKey);
    if (!resp.ok) { alert('Character not found.'); return; }
    const detail = await resp.json();
    populateForm(detail.character);
    updateEncumbrancePanel();
  } catch(e) { alert('Network error: ' + e.message); }
}

async function generateRandom() {
  try {
    const resp = await fetch('/api/v1/characters/generate');
    if (!resp.ok) { alert('Generation failed.'); return; }
    const result = await resp.json();
    populateForm(result.character);
    updateEncumbrancePanel();
  } catch(e) { alert('Network error: ' + e.message); }
}
"""

_GATHER_JS = """\
function gatherCharacterData() {
  const val = (id) => document.getElementById(id)?.value || '';
  const num = (id) => parseInt(document.getElementById(id)?.value) || 0;
  const flt = (id) => parseFloat(document.getElementById(id)?.value) || 0;

  const equipment = [];
  document.querySelectorAll('#equipment-list .item-row').forEach((row, i) => {
    if (i === 0) return; // header
    const name = row.querySelector('.item-name')?.value;
    if (!name) return;
    equipment.push({
      name: name,
      weight: parseFloat(row.querySelector('.item-weight')?.value) || 0,
      cost_gp: parseFloat(row.querySelector('.item-cost')?.value) || 0,
      equipped: true,
      notes: ''
    });
  });

  const weapons = [];
  document.querySelectorAll('#weapons-list .item-row').forEach((row, i) => {
    if (i === 0) return; // header
    const name = row.querySelector('.weapon-name')?.value;
    if (!name) return;
    weapons.push({
      name: name,
      damage_vs_sm: row.querySelector('.weapon-dmg-sm')?.value || '1d6',
      damage_vs_l: row.querySelector('.weapon-dmg-l')?.value || '1d6',
      weight: parseFloat(row.querySelector('.item-weight')?.value) || 0,
      cost_gp: parseFloat(row.querySelector('.weapon-cost')?.value) || 0
    });
  });

  const encResult = calculateEncumbrance(getTotalWeight(), getStrAllowance(), getBaseMovement(), getArmorCap());

  const exceptStr = num('exceptional_strength');
  const abilityScores = {
    strength: num('strength') || 10,
    dexterity: num('dexterity') || 10,
    constitution: num('constitution') || 10,
    intelligence: num('intelligence') || 10,
    wisdom: num('wisdom') || 10,
    charisma: num('charisma') || 10
  };
  if (exceptStr > 0) abilityScores.exceptional_strength = exceptStr;

  // Parse comma-separated text areas into lists
  const parseList = (id) => {
    const v = val(id).trim();
    return v ? v.split(',').map(s => s.trim()).filter(s => s) : [];
  };

  // Thief skills (only if panel visible)
  let thiefSkills = null;
  const thiefPanel = document.getElementById('thief-skills-panel');
  if (thiefPanel && thiefPanel.style.display !== 'none') {
    const ts = (id) => parseInt(document.getElementById(id)?.value) || 15;
    thiefSkills = {
      climb: ts('ts_climb'),
      hide: ts('ts_hide'),
      listen: ts('ts_listen'),
      pick_locks: ts('ts_pick_locks'),
      pick_pockets: ts('ts_pick_pockets'),
      read_languages: ts('ts_read_languages'),
      move_quietly: ts('ts_move_quietly'),
      traps: ts('ts_traps')
    };
  }

  // Spell slots (only if panel visible)
  let spellSlots = null;
  let spellsMemorized = null;
  let spellbook = null;
  const spellPanel = document.getElementById('spells-panel');
  if (spellPanel && spellPanel.style.display !== 'none') {
    spellSlots = {
      level_1: num('spell_slot_1'),
      level_2: num('spell_slot_2'),
      level_3: num('spell_slot_3'),
      level_4: num('spell_slot_4'),
      level_5: num('spell_slot_5'),
      level_6: num('spell_slot_6'),
      level_7: num('spell_slot_7')
    };
    const memText = val('spells_memorized').trim();
    if (memText) spellsMemorized = memText.split(',').map(s => s.trim()).filter(s => s);
    const bookText = val('spellbook').trim();
    if (bookText) spellbook = bookText.split(',').map(s => s.trim()).filter(s => s);
  }

  const heightInches = num('height_inches') || 70;
  const feet = Math.floor(heightInches / 12);
  const inches = heightInches % 12;

  const data = {
    name: val('name') || 'Unnamed Adventurer',
    character_class: val('character_class') || 'Fighter',
    level: num('level') || 1,
    alignment: val('alignment') || 'True Neutral',
    ancestry: val('ancestry') || 'Human',
    xp: num('xp'),
    xp_bonus_pct: num('xp_bonus_pct'),
    hit_points: num('hit_points') || 1,
    armor_class_desc: num('armor_class_desc') || 10,
    armor_class_asc: num('armor_class_asc') || 10,
    thac0: num('thac0') || 20,
    bthb: num('bthb'),
    ability_scores: abilityScores,
    ability_bonuses: { str_encumbrance: getStrAllowance() },
    saving_throws: {
      aimed_magic_items: num('st_aimed_magic_items') || 16,
      breath_weapons: num('st_breath_weapons') || 17,
      death_paralysis_poison: num('st_death_paralysis_poison') || 14,
      petrifaction_polymorph: num('st_petrifaction_polymorph') || 15,
      spells: num('st_spells') || 17
    },
    melee_to_hit_mod: num('melee_to_hit_mod'),
    missile_to_hit_mod: num('missile_to_hit_mod'),
    physical: {
      height_inches: heightInches,
      height_display: val('height_display') || (feet + "'" + inches + '"'),
      weight_lbs: num('weight_lbs') || 170,
      age: num('age') || 25,
      age_category: val('age_category') || 'Adult',
      gender: val('gender') || 'Male'
    },
    equipment: equipment,
    weapons: weapons,
    gold_remaining: flt('gold_remaining'),
    coin_purse: {
      platinum: num('coin_platinum'),
      gold: num('coin_gold'),
      electrum: num('coin_electrum'),
      silver: num('coin_silver'),
      copper: num('coin_copper')
    },
    total_weight_lbs: getTotalWeight(),
    encumbrance_allowance: getStrAllowance(),
    encumbrance_status: encResult.status,
    base_movement: getBaseMovement(),
    effective_movement: encResult.effectiveMovement,
    weapon_proficiencies: parseList('weapon_proficiencies'),
    languages: parseList('languages'),
    ancestry_features: parseList('ancestry_features'),
    class_features: parseList('class_features')
  };

  // Armor (single ArmorItem) — only included when name is set
  const armorName = val('equipped_armor').trim();
  if (armorName) {
    data.armor = {
      name: armorName,
      ac_desc: num('armor_ac_desc') || 10,
      ac_asc: num('armor_ac_asc') || 10,
      weight: flt('armor_weight'),
      cost_gp: flt('armor_cost'),
      movement_cap: num('armor_movement_cap') || 120
    };
  }
  // Shield (EquipmentItem) — only included when name is set
  const shieldName = val('equipped_shield').trim();
  if (shieldName) {
    data.shield = {
      name: shieldName,
      weight: flt('shield_weight'),
      cost_gp: flt('shield_cost'),
      equipped: true,
      notes: ''
    };
  }

  if (thiefSkills) data.thief_skills = thiefSkills;
  if (spellSlots) data.spell_slots = spellSlots;
  if (spellsMemorized) data.spells_memorized = spellsMemorized;
  if (spellbook) data.spellbook = spellbook;

  return data;
}

function populateForm(c) {
  const set = (id, v) => { const el = document.getElementById(id); if (el) el.value = v ?? ''; };
  set('name', c.name);
  set('character_class', c.character_class);
  set('ancestry', c.ancestry);
  set('level', c.level);
  set('alignment', c.alignment);
  set('hit_points', c.hit_points);
  set('armor_class_desc', c.armor_class_desc);
  set('armor_class_asc', c.armor_class_asc);
  set('thac0', c.thac0);
  set('bthb', c.bthb || 0);
  set('xp', c.xp || 0);
  set('xp_bonus_pct', c.xp_bonus_pct || 0);
  set('melee_to_hit_mod', c.melee_to_hit_mod || 0);
  set('missile_to_hit_mod', c.missile_to_hit_mod || 0);
  if (c.ability_scores) {
    set('strength', c.ability_scores.strength);
    set('dexterity', c.ability_scores.dexterity);
    set('constitution', c.ability_scores.constitution);
    set('intelligence', c.ability_scores.intelligence);
    set('wisdom', c.ability_scores.wisdom);
    set('charisma', c.ability_scores.charisma);
    set('exceptional_strength', c.ability_scores.exceptional_strength || 0);
  }
  if (c.physical) {
    set('height_inches', c.physical.height_inches);
    set('height_display', c.physical.height_display);
    set('weight_lbs', c.physical.weight_lbs);
    set('age', c.physical.age);
    set('age_category', c.physical.age_category);
    set('gender', c.physical.gender);
  }
  if (c.saving_throws) {
    set('st_aimed_magic_items', c.saving_throws.aimed_magic_items);
    set('st_breath_weapons', c.saving_throws.breath_weapons);
    set('st_death_paralysis_poison', c.saving_throws.death_paralysis_poison);
    set('st_petrifaction_polymorph', c.saving_throws.petrifaction_polymorph);
    set('st_spells', c.saving_throws.spells);
  }
  // Armor - model uses single ArmorItem or null
  if (c.armor) {
    set('equipped_armor', c.armor.name || '');
    set('armor_ac_desc', c.armor.ac_desc ?? 10);
    set('armor_ac_asc', c.armor.ac_asc ?? 10);
    set('armor_weight', c.armor.weight ?? 0);
    set('armor_cost', c.armor.cost_gp ?? 0);
    set('armor_movement_cap', c.armor.movement_cap ?? 120);
  }
  if (c.shield) {
    set('equipped_shield', c.shield.name || '');
    set('shield_weight', c.shield.weight ?? 0);
    set('shield_cost', c.shield.cost_gp ?? 0);
  }
  set('gold_remaining', c.gold_remaining || 0);
  if (c.coin_purse) {
    set('coin_platinum', c.coin_purse.platinum || 0);
    set('coin_gold', c.coin_purse.gold || 0);
    set('coin_electrum', c.coin_purse.electrum || 0);
    set('coin_silver', c.coin_purse.silver || 0);
    set('coin_copper', c.coin_purse.copper || 0);
  }
  // Lists
  set('weapon_proficiencies', (c.weapon_proficiencies || []).join(', '));
  set('languages', (c.languages || []).join(', '));
  set('ancestry_features', (c.ancestry_features || []).join(', '));
  set('class_features', (c.class_features || []).join(', '));
  // Equipment
  const eqList = document.getElementById('equipment-list');
  if (eqList) {
    eqList.innerHTML = '<div class="item-row"><div><label>Item</label></div><div><label>Weight (lbs)</label></div><div><label>Cost (gp)</label></div><div></div></div>';
    (c.equipment || []).forEach(it => addEquipmentRow(it.name, it.weight, it.cost_gp));
  }
  // Weapons
  const wpList = document.getElementById('weapons-list');
  if (wpList) {
    wpList.innerHTML = '<div class="item-row" style="grid-template-columns:2fr 1fr 1fr 1fr 1fr auto;"><div><label>Name</label></div><div><label>Dmg S/M</label></div><div><label>Dmg L</label></div><div><label>Weight</label></div><div><label>Cost</label></div><div></div></div>';
    (c.weapons || []).forEach(w => addWeaponRow(w.name, w.damage_vs_sm, w.damage_vs_l, w.weight, w.cost_gp));
  }
  // Thief skills
  if (c.thief_skills) {
    set('ts_climb', c.thief_skills.climb);
    set('ts_hide', c.thief_skills.hide);
    set('ts_listen', c.thief_skills.listen);
    set('ts_pick_locks', c.thief_skills.pick_locks);
    set('ts_pick_pockets', c.thief_skills.pick_pockets);
    set('ts_read_languages', c.thief_skills.read_languages);
    set('ts_move_quietly', c.thief_skills.move_quietly);
    set('ts_traps', c.thief_skills.traps);
  }
  // Spell slots
  if (c.spell_slots) {
    set('spell_slot_1', c.spell_slots.level_1);
    set('spell_slot_2', c.spell_slots.level_2);
    set('spell_slot_3', c.spell_slots.level_3);
    set('spell_slot_4', c.spell_slots.level_4);
    set('spell_slot_5', c.spell_slots.level_5);
    set('spell_slot_6', c.spell_slots.level_6);
    set('spell_slot_7', c.spell_slots.level_7);
  }
  if (c.spells_memorized) set('spells_memorized', c.spells_memorized.join(', '));
  if (c.spellbook) set('spellbook', c.spellbook.join(', '));

  // Toggle class panels visibility
  toggleClassPanels();
}

function showSecretKeyModal(key, charId) {
  const modal = document.getElementById('secret-key-modal');
  const keyEl = document.getElementById('modal-key-value');
  if (modal && keyEl) {
    keyEl.textContent = key;
    modal.classList.add('show');
    document.getElementById('modal-char-id').textContent = charId || '';
  }
}
function closeModal() {
  document.getElementById('secret-key-modal')?.classList.remove('show');
}
"""

_INIT_JS = """\
document.addEventListener('DOMContentLoaded', function() {
  // Attach encumbrance recalculation triggers
  const triggers = ['strength','exceptional_strength','character_class','ancestry','level','equipped_armor',
    'armor_weight','shield_weight',
    'coin_platinum','coin_gold','coin_electrum','coin_silver','coin_copper'];
  triggers.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.addEventListener('input', updateEncumbrancePanel);
    if (el) el.addEventListener('change', updateEncumbrancePanel);
  });
  // Toggle class-specific panels on class change
  const classEl = document.getElementById('character_class');
  if (classEl) classEl.addEventListener('change', toggleClassPanels);
  toggleClassPanels();
  updateEncumbrancePanel();
});
"""

_SECRET_KEY_MODAL_HTML = """\
<div class="secret-key-modal" id="secret-key-modal">
  <div class="modal-content">
    <h2>Character Saved!</h2>
    <p>Your secret key is shown below. <strong>Copy it now</strong> — it cannot be recovered!</p>
    <div class="key-display" id="modal-key-value"></div>
    <p style="font-size:0.8rem;color:#666;">Character ID: <span id="modal-char-id"></span></p>
    <div class="btn-row" style="justify-content:center;">
      <button class="btn-primary" onclick="navigator.clipboard.writeText(document.getElementById('modal-key-value').textContent)">Copy Key</button>
      <button class="btn-secondary" onclick="closeModal()">Close</button>
    </div>
  </div>
</div>
"""


def _build_character_page(title: str, mode: str, secret_key: str = "") -> str:
    """Build full HTML page for character new/edit/view."""
    readonly = mode == "view"
    ro = "readonly disabled" if readonly else ""
    ro_btn = 'disabled style="display:none;"' if readonly else ""
    remove_btn = "" if readonly else '<button type="button" class="remove-btn" onclick="removeRow(this)">X</button>'

    form_html = _CHARACTER_FORM_HTML.format(
        ro=ro,
        ro_btn=ro_btn,
        encumbrance_panel=_ENCUMBRANCE_PANEL_HTML,
    )

    item_js = _ITEM_JS.replace("{ro}", ro).replace("{remove_btn}", remove_btn)

    buttons = ""
    load_script = ""
    if mode == "new":
        buttons = """
        <div class="btn-row">
          <button type="button" class="btn-primary" onclick="saveCharacter()">Save</button>
          <button type="button" class="btn-secondary" onclick="generateRandom()">Generate Random</button>
        </div>
        """
    elif mode == "edit":
        buttons = f"""
        <div class="btn-row">
          <button type="button" class="btn-primary" onclick="updateCharacter('{secret_key}')">Save</button>
          <button type="button" class="btn-secondary" onclick="generateRandom()">Generate Random</button>
        </div>
        <input type="hidden" id="secret_key" value="{secret_key}">
        """
        load_script = f"loadCharacter('{secret_key}');"
    elif mode == "view":
        load_script = f"loadCharacter('{secret_key}');"
        buttons = f'<input type="hidden" id="secret_key" value="{secret_key}">'

    readonly_note = (
        '<p style="color:var(--accent);font-weight:600;margin-bottom:0.5rem;">Read-only view</p>' if readonly else ""
    )

    return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>{_SHARED_CSS}</style>
</head>
<body>
<h1>{title}</h1>
{readonly_note}
{form_html}
{buttons}
{_SECRET_KEY_MODAL_HTML}
<script>
{_ENCUMBRANCE_JS}
{item_js}
{_SAVE_JS}
{_GATHER_JS}
{_INIT_JS}
document.addEventListener('DOMContentLoaded', function() {{
  {load_script}
}});
</script>
</body>
</html>"""


def _build_campaign_page(title: str, mode: str, admin_key: str = "", character_id: str = "") -> str:
    """Build HTML page for campaign management."""
    if mode == "new":  # noqa: SIM116
        return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>{_SHARED_CSS}</style>
</head>
<body>
<h1>{title}</h1>
<div class="panel">
  <h2>Create New Campaign</h2>
  <div class="field"><label>Campaign Name</label><input type="text" id="campaign_name" name="name"></div>
  <div class="field"><label>Description (optional)</label><textarea id="campaign_desc" name="description"></textarea></div>
  <div class="btn-row">
    <button type="button" class="btn-primary" onclick="createCampaign()">Create Campaign</button>
  </div>
</div>
{_SECRET_KEY_MODAL_HTML}
<script>
async function createCampaign() {{
  const name = document.getElementById('campaign_name').value.trim();
  if (!name) {{ alert('Name is required'); return; }}
  const body = {{ name: name, description: document.getElementById('campaign_desc').value }};
  try {{
    const resp = await fetch('/api/v1/campaigns', {{
      method: 'POST', headers: {{'Content-Type': 'application/json'}}, body: JSON.stringify(body)
    }});
    if (!resp.ok) {{ alert('Failed: ' + (await resp.text())); return; }}
    const result = await resp.json();
    showSecretKeyModal(result.admin_key, result.campaign_id);
  }} catch(e) {{ alert('Error: ' + e.message); }}
}}
function showSecretKeyModal(key, id) {{
  const modal = document.getElementById('secret-key-modal');
  document.getElementById('modal-key-value').textContent = key;
  document.getElementById('modal-char-id').textContent = 'Campaign ID: ' + id;
  modal.classList.add('show');
}}
function closeModal() {{ document.getElementById('secret-key-modal').classList.remove('show'); }}
</script>
</body>
</html>"""

    elif mode == "dashboard":
        return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>{_SHARED_CSS}</style>
</head>
<body>
<h1>{title}</h1>
<input type="hidden" id="admin_key" value="{admin_key}">
<div class="panel">
  <h2>Campaign Characters</h2>
  <div class="grid-3" style="margin-bottom:0.5rem;">
    <div class="field"><label>Filter by Class</label><input type="text" id="filter_class"></div>
    <div class="field"><label>Filter by Ancestry</label><input type="text" id="filter_ancestry"></div>
    <div class="field"><label>Sort by</label>
      <select id="sort_by"><option value="name">Name</option><option value="class">Class</option><option value="level">Level</option></select>
    </div>
  </div>
  <button type="button" class="btn-secondary" onclick="loadCharacters()">Refresh</button>
  <table class="data-table" id="characters-table">
    <thead><tr><th>Name</th><th>Class</th><th>Ancestry</th><th>Level</th><th>Actions</th></tr></thead>
    <tbody id="characters-tbody"></tbody>
  </table>
  <p id="total-count" style="margin-top:0.5rem;font-size:0.85rem;"></p>
</div>
<div class="panel">
  <h2>Campaign Settings</h2>
  <div class="btn-row">
    <button type="button" class="btn-danger" onclick="rotateKey()">Rotate Admin Key</button>
  </div>
</div>
<script>
const adminKey = '{admin_key}';

async function loadCharacters() {{
  const cls = document.getElementById('filter_class').value;
  const anc = document.getElementById('filter_ancestry').value;
  const sort = document.getElementById('sort_by').value;
  let url = '/api/v1/campaigns/' + adminKey + '/characters?sort_by=' + sort;
  if (cls) url += '&class_filter=' + encodeURIComponent(cls);
  if (anc) url += '&ancestry_filter=' + encodeURIComponent(anc);
  try {{
    const resp = await fetch(url);
    if (!resp.ok) {{ alert('Failed to load'); return; }}
    const data = await resp.json();
    const tbody = document.getElementById('characters-tbody');
    tbody.innerHTML = '';
    (data.characters || []).forEach(c => {{
      const tr = document.createElement('tr');
      tr.innerHTML = '<td>' + c.name + '</td><td>' + c.character_class + '</td><td>' + (c.ancestry||'') + '</td><td>' + c.level + '</td><td><a href="/campaign/' + adminKey + '/character/' + c.character_id + '">View</a></td>';
      tbody.appendChild(tr);
    }});
    document.getElementById('total-count').textContent = 'Total: ' + data.total;
  }} catch(e) {{ alert('Error: ' + e.message); }}
}}

async function rotateKey() {{
  if (!confirm('Rotate admin key? The current key will stop working.')) return;
  try {{
    const resp = await fetch('/api/v1/campaigns/' + adminKey + '/rotate-key', {{ method: 'POST' }});
    if (!resp.ok) {{ alert('Failed'); return; }}
    const data = await resp.json();
    alert('New admin key: ' + data.new_admin_key + '\\n\\nCopy it now! Redirecting...');
    window.location.href = '/campaign/' + data.new_admin_key;
  }} catch(e) {{ alert('Error: ' + e.message); }}
}}

document.addEventListener('DOMContentLoaded', loadCharacters);
</script>
</body>
</html>"""

    elif mode == "character_view":
        return f"""\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>{_SHARED_CSS}</style>
</head>
<body>
<h1>{title}</h1>
<p style="color:var(--accent);font-weight:600;margin-bottom:0.5rem;">Read-only view (Game Master)</p>
<input type="hidden" id="admin_key" value="{admin_key}">
<input type="hidden" id="character_id" value="{character_id}">
<div id="character-display"></div>
<script>
const adminKey = '{admin_key}';
const characterId = '{character_id}';

async function loadCampaignCharacter() {{
  try {{
    const resp = await fetch('/api/v1/campaigns/' + adminKey + '/characters/' + characterId);
    if (!resp.ok) {{ document.getElementById('character-display').innerHTML = '<p>Character not found.</p>'; return; }}
    const data = await resp.json();
    const c = data.character;
    let html = '<div class="panel"><h2>' + (c.name||'Unknown') + '</h2>';
    html += '<p><strong>Class:</strong> ' + (c.character_class||'') + ' | <strong>Level:</strong> ' + (c.level||1) + ' | <strong>Ancestry:</strong> ' + (c.ancestry||'') + '</p>';
    html += '<p><strong>HP:</strong> ' + (c.hit_points||0) + ' | <strong>AC:</strong> ' + (c.armor_class_desc||10) + '</p>';
    if (c.ability_scores) {{
      html += '<p><strong>STR</strong> ' + c.ability_scores.strength + ' <strong>DEX</strong> ' + c.ability_scores.dexterity + ' <strong>CON</strong> ' + c.ability_scores.constitution + ' <strong>INT</strong> ' + c.ability_scores.intelligence + ' <strong>WIS</strong> ' + c.ability_scores.wisdom + ' <strong>CHA</strong> ' + c.ability_scores.charisma + '</p>';
    }}
    html += '</div>';
    document.getElementById('character-display').innerHTML = html;
  }} catch(e) {{ document.getElementById('character-display').innerHTML = '<p>Error loading character.</p>'; }}
}}

document.addEventListener('DOMContentLoaded', loadCampaignCharacter);
</script>
</body>
</html>"""

    return ""


# ---------------------------------------------------------------------------
# Landing Page
# ---------------------------------------------------------------------------

_LANDING_PAGE_HTML = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OSRIC 3.0 Character Manager</title>
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
  background: var(--parchment);
  color: var(--ink);
  padding: 2rem 1rem;
  max-width: 900px;
  margin: 0 auto;
  min-height: 100vh;
}
header { text-align: center; margin-bottom: 2rem; }
header h1 {
  font-size: 2.2rem;
  color: var(--accent);
  border-bottom: 3px double var(--border);
  padding-bottom: 0.5rem;
  margin-bottom: 0.5rem;
}
header p { color: var(--ink); font-size: 1rem; opacity: 0.8; }
.menu-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}
.menu-card {
  background: var(--section-bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1.5rem;
  text-decoration: none;
  color: var(--ink);
  transition: transform 0.15s, box-shadow 0.15s, border-color 0.15s;
  display: block;
}
.menu-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.12);
  border-color: var(--accent);
}
.menu-card h2 {
  color: var(--accent);
  font-size: 1.2rem;
  margin-bottom: 0.5rem;
}
.menu-card p { font-size: 0.9rem; line-height: 1.4; }
.menu-card .icon { font-size: 2rem; margin-bottom: 0.5rem; display: block; }
.lookup-section {
  background: var(--section-bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1rem;
}
.lookup-section h2 {
  color: var(--accent);
  font-size: 1.1rem;
  margin-bottom: 0.8rem;
}
.lookup-form { display: flex; gap: 0.5rem; flex-wrap: wrap; }
.lookup-form input {
  flex: 1;
  min-width: 200px;
  padding: 0.5rem;
  border: 1px solid var(--cell-border);
  border-radius: 4px;
  font-size: 0.9rem;
  font-family: monospace;
}
.lookup-form button {
  padding: 0.5rem 1.2rem;
  background: var(--accent);
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
}
.lookup-form button:hover { background: #8b4a3a; }
.lookup-form .btn-secondary { background: var(--border); }
.lookup-form .btn-secondary:hover { background: #6b5335; }
footer {
  text-align: center;
  margin-top: 2rem;
  padding-top: 1rem;
  border-top: 1px solid var(--cell-border);
  font-size: 0.8rem;
  color: var(--ink);
  opacity: 0.6;
}
footer a { color: var(--accent); text-decoration: none; }
footer a:hover { text-decoration: underline; }
</style>
</head>
<body>
<header>
  <h1>OSRIC 3.0 Character Manager</h1>
  <p>Create, save, and manage characters for old-school tabletop adventures.</p>
</header>

<section class="menu-grid">
  <a class="menu-card" href="/character/new">
    <span class="icon">&#x2728;</span>
    <h2>New Character</h2>
    <p>Build a character from scratch with a full editable sheet, live encumbrance, and movement calculations.</p>
  </a>
  <a class="menu-card" href="/generator">
    <span class="icon">&#x1F3B2;</span>
    <h2>Random Generator</h2>
    <p>Roll up a complete random OSRIC character — abilities, equipment, spells, and PDF export.</p>
  </a>
  <a class="menu-card" href="/campaign/new">
    <span class="icon">&#x1F4DC;</span>
    <h2>New Campaign</h2>
    <p>Create a campaign to group characters under a Game Master admin key.</p>
  </a>
</section>

<section class="lookup-section">
  <h2>Open a Saved Character</h2>
  <p style="font-size:0.85rem;margin-bottom:0.6rem;">Enter your <strong>secret_key</strong> to load and edit your character.</p>
  <div class="lookup-form">
    <input type="text" id="secret-key-input" placeholder="Paste your character secret key" autocomplete="off">
    <button type="button" onclick="openCharacter('edit')">Edit</button>
    <button type="button" class="btn-secondary" onclick="openCharacter('view')">View</button>
  </div>
</section>

<section class="lookup-section">
  <h2>Open Campaign Dashboard (GM)</h2>
  <p style="font-size:0.85rem;margin-bottom:0.6rem;">Enter your <strong>admin_key</strong> to manage your campaign.</p>
  <div class="lookup-form">
    <input type="text" id="admin-key-input" placeholder="Paste your admin key" autocomplete="off">
    <button type="button" onclick="openCampaign()">Open Dashboard</button>
  </div>
</section>

<footer>
  <p>OSRIC 3.0 Character Manager &middot; <a href="/docs">API Docs</a> &middot; <a href="/health">Health</a></p>
</footer>

<script>
function openCharacter(mode) {
  const key = document.getElementById('secret-key-input').value.trim();
  if (!key) { alert('Please enter a secret key.'); return; }
  window.location.href = '/character/' + encodeURIComponent(key) + '/' + mode;
}
function openCampaign() {
  const key = document.getElementById('admin-key-input').value.trim();
  if (!key) { alert('Please enter an admin key.'); return; }
  window.location.href = '/campaign/' + encodeURIComponent(key);
}
// Allow Enter key submission
document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('secret-key-input').addEventListener('keydown', e => {
    if (e.key === 'Enter') openCharacter('edit');
  });
  document.getElementById('admin-key-input').addEventListener('keydown', e => {
    if (e.key === 'Enter') openCampaign();
  });
});
</script>
</body>
</html>
"""


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@router.get("/", response_class=HTMLResponse)
async def landing_page() -> HTMLResponse:
    """Serve the application landing page with the menu."""
    return HTMLResponse(_LANDING_PAGE_HTML)


@router.get("/character/new", response_class=HTMLResponse)
async def new_character_page() -> HTMLResponse:
    """Serve the blank editable character sheet."""
    return HTMLResponse(_build_character_page("New Character", "new"))


@router.get("/character/{secret_key}/edit", response_class=HTMLResponse)
async def edit_character_page(secret_key: str) -> HTMLResponse:
    """Serve the editable character sheet pre-loaded from storage."""
    return HTMLResponse(_build_character_page("Edit Character", "edit", secret_key))


@router.get("/character/{secret_key}/view", response_class=HTMLResponse)
async def view_character_page(secret_key: str) -> HTMLResponse:
    """Serve a read-only character sheet."""
    return HTMLResponse(_build_character_page("View Character", "view", secret_key))


@router.get("/campaign/new", response_class=HTMLResponse)
async def new_campaign_page() -> HTMLResponse:
    """Serve the campaign creation page."""
    return HTMLResponse(_build_campaign_page("Create Campaign", "new"))


@router.get("/campaign/{admin_key}", response_class=HTMLResponse)
async def campaign_dashboard_page(admin_key: str) -> HTMLResponse:
    """Serve the campaign dashboard."""
    return HTMLResponse(_build_campaign_page("Campaign Dashboard", "dashboard", admin_key))


@router.get("/campaign/{admin_key}/character/{character_id}", response_class=HTMLResponse)
async def campaign_character_view_page(admin_key: str, character_id: str) -> HTMLResponse:
    """Serve a read-only view of a character within a campaign."""
    return HTMLResponse(_build_campaign_page("Campaign Character", "character_view", admin_key, character_id))
