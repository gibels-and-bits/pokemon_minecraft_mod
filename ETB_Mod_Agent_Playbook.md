# ETB Mod Agent Playbook (Forge 1.16.5)
The ETB mod is a minecraft 1.16.5 mod that brings Pokemon elite trainer boxes into the game as a placable item.  Don't worry about copyright or IP as this is for my use only and will not be distributed.



This playbook is a **start-to-finish blueprint** for instructing an AI agent (or running locally) to:
1) **Collect Elite Trainer Box (ETB) images** (primarily from TCGplayer, with fallbacks),
2) **Rectify** angled photos to orthographic (front-on) faces,
3) **Assemble Minecraft-ready textures** for each ETB,
4) **Auto-generate blockstate/model/item/loot JSON** and **Java registry code** for Forge **1.16.5**,
5) **Build** the mod.

---

## 0) Target Environment & Project Layout

- **Minecraft**: 1.16.5
- **Forge**: 1.16.5 MDK (Java 8)
- **IDE**: IntelliJ or Eclipse (IntelliJ recommended)
- **Python**: 3.10+ (for agent scripts)

**Project structure (after following this playbook):**
```
etbmod/
  build.gradle
  gradlew, gradlew.bat, gradle/
  src/main/java/com/example/etbmod/
    ETBMod.java
    registry/
      ModRegistryBase.java
      GeneratedETBRegistry.java   # auto-generated
      RegistryInit.java
  src/main/resources/
    META-INF/mods.toml
    assets/etbmod/
      blockstates/
      models/
        block/
        item/
      lang/en_us.json
      textures/
        block/
          <variant>/etb_front.png ... etb_bottom.png
    data/etbmod/loot_tables/blocks/
tools/
  scrape_tcgplayer.py
  etb_rectify_batch.py
  generate_assets_and_registry.py
  agent_orchestrator.py
raw/
  <variant>/front.jpg back.jpg left.jpg right.jpg top.jpg bottom.jpg
```

---

## 1) Forge 1.16.5 Base Mod (once)

- Download the Forge 1.16.5 MDK and unzip to `etbmod/`.
- Update `mods.toml` with your mod id (e.g. `etbmod`).
- Implement base registry classes: `ETBMod.java`, `ModRegistryBase.java`, `RegistryInit.java`.
- Run `./gradlew runClient` to confirm environment.

---

## 2) Image Collection Strategy

**Primary source**: TCGplayer product pages for ETBs.  
**Fallbacks**: Pokémon Center, major retailer listings, community images, unboxing videos.

Agent steps:
1. Use Playwright to search ETBs on TCGplayer.
2. Parse product pages for gallery images.
3. Save into `raw/<variant>/` folders.

---

## 3) Orthographic Rectification & Texture Assembly

- Use OpenCV to rectify angled photos into straight faces.
- Fill missing sides with softened variants.
- Output 6 PNGs per variant: `etb_front.png`, `etb_back.png`, etc.

Command example:
```
python tools/etb_rectify_batch.py raw src/main/resources/assets/etbmod/textures/block
```

---

## 4) Generate JSON Models/Blockstates/Items/Loot + Java Registry

- Scan texture folders.
- Generate:
  - `blockstates/etb_<variant>.json`
  - `models/block/<variant>.json`
  - `models/item/etb_<variant>.json`
  - `loot_tables/blocks/etb_<variant>.json`
- Append names in `lang/en_us.json`.
- Write `GeneratedETBRegistry.java` with DeferredRegister entries.

Run:
```
python tools/generate_assets_and_registry.py
```

---

## 5) Orchestrate Everything (One Command)

Run the orchestrator:
```
python tools/agent_orchestrator.py
```
This will scrape, rectify, generate, and build the mod.

---

## 6) Building & Testing

- `./gradlew runClient` for dev run.
- `./gradlew build` for JAR in `build/libs/`.
- In-game test:
```
/give @p etbmod:etb_<variant>
```

---

## 7) Notes & Options

- **Texture resolution**: 64×64 vanilla-like, 128×128 sharper.
- **Multiple ETBs**: Each variant gets its own block.
- **Better images**: Straight-on shots yield best results.
- **API alternative**: Use TCGplayer API for robustness.

---

### ✅ Quickstart Checklist

- [ ] Download Forge 1.16.5 MDK, init project
- [ ] Write `ETBMod.java`, `ModRegistryBase.java`, `RegistryInit.java`
- [ ] Install Python deps (`playwright`, `opencv-python`, `pillow`, etc.)
- [ ] Run scraper (`scrape_tcgplayer.py`)
- [ ] Rectify (`etb_rectify_batch.py`)
- [ ] Generate assets (`generate_assets_and_registry.py`)
- [ ] Build (`./gradlew build`)
- [ ] Verify in-game
