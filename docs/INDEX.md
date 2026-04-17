# OSRIC 3.0 Character Generator — Specification Index

**Version**: 1.1.0
**Date**: 2025-07-12

---

## Specification Documents

| # | Document | Description | Path |
|---|----------|-------------|------|
| 01 | [Functional Specification](specs/01-functional-specification.md) | Business requirements, character creation workflow, step-by-step algorithms, edge cases, data validation rules | `docs/specs/01-functional-specification.md` |
| 02 | [Technical Specification](specs/02-technical-specification.md) | Architecture, technology stack, project structure, data models (Pydantic), API contract, domain module interfaces, testing strategy, configuration, deployment | `docs/specs/02-technical-specification.md` |
| 03 | [Game Data Reference](specs/03-game-data-reference.md) | Complete OSRIC 3.0 rule data tables: ability bonuses, class definitions, ancestry definitions, saving throws, THAC0, thief skills, turn undead, equipment, spells, encumbrance | `docs/specs/03-game-data-reference.md` |

---

## Diagrams

All diagrams use Mermaid syntax and are embedded inline in the specification documents.

| Diagram | Location | Type |
|---------|----------|------|
| Character Creation Workflow | Functional Spec §3 | Flowchart |
| System Architecture | Technical Spec §2.1 | Component Graph |
| Component Architecture | Technical Spec §2.2 | Module Dependency Graph |
| Deployment Architecture | Technical Spec §2.3 | Infrastructure Graph |
| Dependency Graph | Technical Spec §15 | Directed Dependency Graph |

---

## Summary

| Metric | Value |
|--------|-------|
| Requirements documented | 33 (FR-001 through FR-033) |
| Character creation steps specified | 16 |
| Classes covered | 10 |
| Ancestries covered | 7 |
| Data tables defined | 30+ |
| API endpoints | 3 (POST /generate, POST /generate/pdf, GET /health) |
| Pydantic models | 15 |
| Domain modules | 8 |
| Test categories | 4 (unit, integration, API, data integrity) |
| Estimated test cases | 110+ |
| Coverage target | ≥ 85% overall |
| Diagrams | 5 |
| PDF form fields | ~155 (across 2 pages) |

---

## Assumptions

1. Level 1 characters only — no advancement logic
2. Single-class only for v1.0 — multi-class deferred
3. Dual-classing excluded (advancement feature)
4. No name generation — placeholder used
5. No persistent storage — stateless generation
6. No house rules except ascending AC inclusion
7. Weapon specialization excluded for v1.0
8. Equipment auto-purchase uses deterministic priority, not random
9. Coins contribute to encumbrance (10 coins = 1 lb)
10. REST API with JSON and PDF output formats
11. Scroll artwork from PDF page 13 is not reproduced — plain bordered box used
12. PDF character sheet replicates the layout from OSRIC 3.0 Player Guide pages 12–13

---

## Source Material

- **OSRIC 3.0 Player Guide PDF** (264 pages)
  - Character Creation: Pages 11–83
  - Encumbrance: Page 89
  - Turn Undead: Page 99
  - Cleric Spells: Page 127
  - Druid Spells: Page 161
  - Illusionist Spells: Page 183
  - Magic-User Spells: Page 200
