## [2026-04-21T19:35:53Z] Session Start - Bug Fixes & Improvements

### Tasks
1. Weapon proficiencies not scaling with level
2. Coin denomination display (pp/gp/ep/sp/cp)
3. Level-based starting gold (500 GP per level above 1)

### Research Findings
- `calculate_proficiency_slots` correctly calculates slots but character_generator only assigns proficiencies from purchased weapons (max 2)
- `gold_remaining` is a single float, needs CoinPurse model
- Starting gold is dice-rolled only, no level bonus

