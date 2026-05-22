# SOUL DSL — ПЪЛНА ЕЗИКОВА СПЕЦИФИКАЦИЯ

```
╔══════════════════════════════════════════════════════════════════════╗
║  SOUL DOMAIN-SPECIFIC LANGUAGE — v3.0 SINGULARITY                   ║
║  ARCHITECT: DIMITAR PRODROMOV                                       ║
║  AETERNA-QANTUM SOVEREIGN RUNTIME                                   ║
║  GRAMMAR: PEG (Parsing Expression Grammar)                          ║
║  COMPILER: lwas_sentinel (Rust) → soul_vm (Zig)                     ║
║  STATUS: COMPILED + TESTED + OPERATIONAL                             ║
╚══════════════════════════════════════════════════════════════════════╝
```

---

## Съдържание

1. [Обща архитектура](#1-обща-архитектура)
2. [Лексикален анализ](#2-лексикален-анализ)
3. [Система от типове (Value Types)](#3-система-от-типове)
4. [Блокови конструкции (Scopes)](#4-блокови-конструкции)
5. [Опкодове (Instructions)](#5-опкодове)
6. [Свойства (Properties)](#6-свойства)
7. [Catuskoti — Четиристепенна логика](#7-catuskoti--четиристепенна-логика)
8. [Import система](#8-import-система)
9. [Пълна PEG граматика (lwas.pest)](#9-пълна-peg-граматика)
10. [Компилационен пайплайн](#10-компилационен-пайплайн)
11. [FFI мост (Rust ↔ Zig)](#11-ffi-мост)
12. [Zig VM — Екзекутор](#12-zig-vm--екзекутор)
13. [Полиморфен метаморфен двигател](#13-полиморфен-метаморфен-двигател)
14. [Примери от реално работещи .soul файлове](#14-примери)
15. [Речник на термините](#15-речник)

---

## 1. Обща архитектура

Soul DSL е **декларативен, детерминистичен език** за описание на поведение, мисии, логически гейтове и хардуерни свързвания в AETERNA-QANTUM платформата. Той НЕ е процедурен — той е **конституционен**: описва *какво* системата Е и *какво* тя защитава.

```
┌──────────────────────────────────────────────────────────────┐
│                    .soul SOURCE FILE                         │
│  (genesis.soul, sentinel.soul, swarm.soul, ...)              │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│              RUST SENTINEL (lwas_sentinel.rlib)               │
│                                                              │
│  1. PEG Parser (pest) → HIR (Hierarchical IR)                │
│  2. Flattener → LIR (Linear IR — FfiInstruction[192B])       │
│  3. Catuskoti Static Analyzer                                │
│  4. std::mem::forget → Transfer ownership to Zig             │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       │  *const AstPayload (Zero-Copy, Zero-Alloc)
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│               ZIG VM (soul_vm.exe)                            │
│                                                              │
│  1. Function Pointer Dispatch Table (23 entries)             │
│  2. DNA-Keyed Polymorphic Engine (MD5 + XOR-shift)           │
│  3. Catuskoti Runtime Resolution                             │
│  4. MOJO AI Portal (Logic MOJO_STABILIZED)                   │
│  5. Packed u64 Result → Caller                               │
└──────────────────────────────────────────────────────────────┘
```

### Философия на дизайна

| Принцип | Имплементация |
|---------|---------------|
| **Нулева ентропия** | Всеки `.soul` файл колабсира системното състояние към детерминизъм |
| **Zero-Copy** | Никакви алокации след парсинг; FFI е директен pointer transfer |
| **L1 Cache Locality** | Инструкциите са 192B (3 cache lines), секвенциален скан |
| **Catuskoti Logic** | 4-ъгълна логика (Истина, Лъжа, И двете, Нито едно) |
| **Sovereign by Design** | Всяка мутация изисква AUTHORITY верификация |

---

## 2. Лексикален анализ

### 2.1 Пренебрегвани токени (Zero-cost)

```pest
WHITESPACE = _{ " " | "\t" | "\r" | "\n" }
COMMENT    = _{ "//" ~ (!"\n" ~ ANY)* }
```

Коментарите и whitespace се елиминират от парсера при **нулев разход на памет** (`_{ }` = silent rule в pest).

Soul поддържа **едноредни коментари** с `//`:

```soul
// Това е коментар
resonate RESONANCE(0x4121);  // Inline коментар
```

### 2.2 Идентификатори

```pest
ident = @{ ASCII_ALPHA ~ (ASCII_ALPHANUMERIC | "_")* }
```

Правила за идентификатори:
- Започват с **латинска буква** (A-Z, a-z)
- Следвани от буква, цифра или `_`
- **Case-sensitive**: `CORE` ≠ `core` ≠ `Core`
- Конвенция: SCREAMING_SNAKE_CASE за блокове, camelCase за properties

**Валидни:**
```
CORE, AUTHORITY, ON_BOOT, resonance_count, MyModule, v3
```

**Невалидни:**
```
_hidden (започва с _)
3D_Engine (започва с цифра)
my-module (тире не е позволено)
```

### 2.3 Kръстосани референции (Cross-References)

```pest
cross_ref = @{ ident ~ ("::" ~ ident | "." ~ ident)+ }
```

Cross-ref позволява обръщение към друг модул или manifold:

```soul
resonate AUTHORITY(genesis.soul::CORE.AUTHORITY);
target BRIDGE(UKAME_Metal_Bridge.zig::drop_unauthorized_flux);
```

Формати:
- `Module::Function` — Rust-style namespace
- `Module.Field` — Dot notation (OOP style)
- Комбинация: `genesis.soul::CORE.AUTHORITY`

---

## 3. Система от типове

Soul DSL поддържа **6 стойностни типа**, кодирани като `ValueType` enum (u8):

| Код | Тип | PEG Правило | Примери | Rust/Zig Mapping |
|-----|-----|-------------|---------|------------------|
| 0 | `None` | — | *(няма стойност)* | `ValueType::None` |
| 1 | `String` | `string_val` | `"Hello"`, `"ACTIVE"` | `ValueType::String` |
| 2 | `Hex` | `hex_val` | `0x4121`, `0x41_45_54!` | `ValueType::Hex` |
| 3 | `Float` | `float_val` | `0.9999`, `3.14`, `100.00` | `ValueType::Float` |
| 4 | `Int` | `int_val` | `101327948`, `500`, `0` | `ValueType::Int` |
| 5 | `CrossRef` | `cross_ref` | `genesis.soul::CORE.AUTHORITY` | `ValueType::CrossRef` |
| 6 | `Boolean` | `bool_val` | `true`, `false` | `ValueType::Boolean` |

### 3.1 Приоритет на разпознаване

PEG граматиката match-ва стойностите в **строг ред** (първият match печели):

```pest
value = _{ bool_val | cross_ref | hex_val | float_val | int_val | string_val }
```

1. `bool_val` — `true`/`false` (предотвратява конфликт с `ident`)
2. `cross_ref` — `A::B` или `A.B` (преди `ident` или `hex_val`)
3. `hex_val` — `0x...` (преди `int_val`, защото `0` е digit)
4. `float_val` — `123.456` (преди `int_val`, защото `.` я разграничава)
5. `int_val` — `12345`
6. `string_val` — `"..."` (последен, protected от кавички)

### 3.2 Подробно описание на типовете

#### Hex (`hex_val`)

```pest
hex_val = @{ "0x" ~ (ASCII_HEX_DIGIT | "_")+ ~ "!"? }
```

Hex стойности поддържат **визуални разделители** (`_`) и опционален **authority marker** (`!`):

```soul
resonate RESONANCE(0x4121);                    // Обикновен hex
resonate AUTHORITY(0x41_45_54_45_52_4e_41!);   // С разделители и "!" маркер
```

`!` маркерът е значим — указва, че тази стойност е **sovereign authority hex**.

#### Float (`float_val`)

```pest
float_val = @{ ASCII_DIGIT+ ~ "." ~ ASCII_DIGIT+ }
```

> **⚠️ ВНИМАНИЕ:** Float стойностите са **ЗАБРАНЕНИ** за финансови изчисления в Wealth Bridge. Използват се само за дескриптивни стойности (версия, чувствителност, физични константи).

```soul
resonate VERSION(3.0);           // Версия — OK
collapse ENTROPY(0.0000);        // Абсолютна нула — OK
entrench SENSITIVITY(1.0000);    // Сензор праг — OK
// target ROI(100.00);           // Финансов — ще се конвертира до FixedPoint(1000000)
```

#### String (`string_val`)

```pest
string_val = ${ "\"" ~ inner ~ "\"" }
inner      = @{ (!"\"" ~ ANY)* }
```

Стрингове се ограждат с двойни кавички. **Няма escape sequences** — съдържанието е raw.

```soul
entrench MISSION("Global Ingestion");
manifest BRANDING("AETERNA-QANTUM HQ");
```

#### Boolean (`bool_val`)

```pest
bool_val = { "true" | "false" }
```

Използва се основно с `verify` опкода за мрежови верификации:

```soul
verify ON_BOOT(true);      // Верифицирай при стартиране
verify ON_MUTATION(true);  // Верифицирай при мутация
verify AUTHORITY_CHAIN(true);
```

#### Integer (`int_val`)

```pest
int_val = @{ ASCII_DIGIT+ }
```

```soul
resonate ARCHITECT_ID(101327948);
vibe GLASSMORPHISM_LEVEL(500);
synchronize BRIDGE_PORT(8888);
swarm NODES(2_000_000);           // Забележка: 2_000_000 се хваща от hex_val!
```

> **Забележка:** Числа с `_` като `2_000_000` се хващат от `hex_val` правилото (без `0x` prefix ще се match-нат като hex поради `_`). За чисти integers, използвайте числа без разделители или стрингово представяне.

---

## 4. Блокови конструкции

Soul DSL дефинира **5 типа блокове**, всеки със специфична семантична роля:

```pest
manifold  = { "manifold"  ~ ident ~ "{" ~ instruction* ~ "}" }
fragment  = { "fragment"  ~ ident ~ "{" ~ instruction* ~ "}" }
directive = { "directive" ~ ident ~ "{" ~ instruction* ~ "}" }
pipeline  = { "pipeline"  ~ ident ~ "{" ~ instruction* ~ "}" }
ledger    = { "ledger"    ~ ident ~ "{" ~ instruction* ~ "}" }
```

### 4.1 `manifold` — Основен манифолд (Конституция)

**Opcode:** `ManifoldBegin (1)` / `BlockEnd (0)`

Manifold е **най-висшата структура** в Soul DSL. Той дефинира identity, authority и mission на подсистема. Всеки `.soul` файл трябва да има поне един manifold.

```soul
manifold CORE {
    resonate RESONANCE(0x4121);
    resonate AUTHORITY(0x41_45_54_45_52_4e_41!);
    entrench MISSION("Global Ingestion");
    collapse ENTROPY(0.0000);
}
```

**Правила:**
- Manifold е **immutable** след collapse
- Мутация изисква AUTHORITY подпис
- Catuskoti стейтът се определя от съдържанието

### 4.2 `fragment` — Фрагмент (Подсистема)

**Opcode:** `FragmentBegin (2)` / `BlockEnd (0)`

Fragment е **подраздел** на manifold. Използва се за логическо групиране на свързана функционалност:

```soul
fragment INTERFACE {
    vibe GLASSMORPHISM_LEVEL(500);
    synchronize BRIDGE_PORT(8888);
    manifest BRANDING("AETERNA-QANTUM HQ");
}

fragment CONSENSUS {
    entrench PROTOCOL("Byzantine_Pulse");
    entrench SYNC("Quantum_State_Sync");
}
```

### 4.3 `directive` — Директива (Стратегически приоритет)

**Opcode:** `DirectiveBegin (3)` / `BlockEnd (0)`

Directive задава **стратегически параметри** и цели:

```soul
directive OMEGA {
    target ROI(100.00);
    swarm NODES(2_000_000);
    logic ENGINE("MOJO_STABILIZED");
}

directive SWARM_INTELLIGENCE {
    entrench DECISION("Hive_Mind_Vote");
}
```

### 4.4 `pipeline` — Пайплайн (Поток от данни)

**Opcode:** `PipelineBegin (4)` / `BlockEnd (0)`

Pipeline описва **последователност от трансформации** на данни:

```soul
pipeline WEALTH_EXTRACTION {
    bind KRAKEN_API("exchange/kraken_bridge.ts");
    bind SOLANA_BRIDGE("blockchain/solana_rpc.rs");
    manifest TRANSACTION("SEPA_EXECUTION");
    verify AUTHORITY(true);
}
```

### 4.5 `ledger` — Регистър (Финансов/Одитен запис)

**Opcode:** `LedgerBegin (5)` / `BlockEnd (0)`

Ledger е **одитната следа** — immutable запис на стойности и трансакции:

```soul
ledger VAULT {
    resonate BALANCE(0x00);
    hash INTEGRITY("SHA256_VAULT_CHECKSUM");
    verify ON_MUTATION(true);
}
```

### 4.6 Вложени блокове

Блоковете могат да бъдат **вложени**, но Rust Sentinel ги **изравнява** в линеен масив с `BlockBegin`/`BlockEnd` маркери:

```soul
manifold SENTINEL {
    resonate RESONANCE(0x53454E54);

    fragment METAL_INTEGRATION {
        directive PACKET_DROP {
            target BRIDGE("UKAME_Metal_Bridge.zig::drop_unauthorized_flux");
        }
    }
}
```

**Компилира се до:**
```
ManifoldBegin("SENTINEL")
  Resonate("RESONANCE", hex=0x53454E54)
  FragmentBegin("METAL_INTEGRATION")
    DirectiveBegin("PACKET_DROP")
      Target("BRIDGE", crossref="UKAME_Metal_Bridge.zig::drop_unauthorized_flux")
    BlockEnd
  BlockEnd
BlockEnd
```

---

## 5. Опкодове

Soul DSL дефинира **13 инструкционни опкода**, разделени в 3 категории:

### 5.1 Ядрени опкодове (Core)

| # | Опкод | Синтаксис | Предназначение |
|---|-------|-----------|----------------|
| 10 | `resonate` | `resonate IDENT(value);` | Свързване на константа/identity към системата |
| 11 | `entrench` | `entrench IDENT(value) { ... }` | Укрепване на мисия/протокол (immutable) |
| 12 | `collapse` | `collapse IDENT(value) { ... }` | Елиминиране на състояние/заплаха |
| 13 | `vibe` | `vibe IDENT(value) { ... }` | Честотна/емоционална настройка (UI/UX) |
| 14 | `synchronize` | `synchronize IDENT(value) { ... }` | Кръстосан синхрон между подсистеми |
| 15 | `manifest` | `manifest IDENT(value) { ... }` | Създаване на актив/модул/ресурс |
| 16 | `target` | `target IDENT(value) { ... }` | Задаване на цел/обектив |
| 17 | `swarm` | `swarm IDENT(value) { ... }` | Командване на рояк от нодове |
| 18 | `logic` | `logic IDENT(value) { ... }` | Логически гейт (**MOJO_STABILIZED порт**) |

### 5.2 Мрежови опкодове (Network)

| # | Опкод | Синтаксис | Предназначение |
|---|-------|-----------|----------------|
| 19 | `bind` | `bind IDENT(value) { ... }` | Свързване с външен модул/API |
| 20 | `verify` | `verify IDENT(value);` | Булева верификация (ON_BOOT, AUTHORITY) |
| 21 | `hash` | `hash IDENT(value);` | Генериране/проверка на integrity hash |

### 5.3 Мета опкод

| # | Опкод | Синтаксис | Предназначение |
|---|-------|-----------|----------------|
| 22 | `property` | `key: value;` | Задаване на свойство (Catuskoti override, metadata) |

### 5.4 Scope маркери

| # | Опкод | Генериран от |
|---|-------|-------------|
| 0 | `BlockEnd` | Затварящ `}` на всеки блок |
| 1 | `ManifoldBegin` | `manifold NAME {` |
| 2 | `FragmentBegin` | `fragment NAME {` |
| 3 | `DirectiveBegin` | `directive NAME {` |
| 4 | `PipelineBegin` | `pipeline NAME {` |
| 5 | `LedgerBegin` | `ledger NAME {` |
| 6 | `Import` | `import "path";` |

---

### 5.5 Подробно описание на ядрените опкодове

#### `resonate` — Резонанс (Константно свързване)

**Семантика:** Установява неизменна фундаментална стойност. `resonate` е еквивалент на `const` в традиционни езици, но с философско значение — стойността *резонира* из цялата система.

```soul
resonate RESONANCE(0x4121);         // Честотен подпис — 16673 Hz
resonate AUTHORITY(0x41_45_54!);    // Sovereign authority hex
resonate ARCHITECT_ID(101327948);   // Unique ID на архитекта
resonate VERSION(3.0);              // Версия на manifold-а
resonate OBJECTIVE("ESTABLISH_ORDER");
```

**VM ефект:** `resonance_count += 1`. Необходим за Catuskoti inference.

#### `entrench` — Укрепяване (Мисия)

**Семантика:** Укрепява мисия или протокол. Веднъж entrench-нат, не може да бъде премахнат — само допълван. Подобно на конституционна клауза.

```soul
entrench MISSION("Global Ingestion") {
    description: "Ingest all available data streams";
    binds: ["OmniCore/ingestion", "OmniCore/data"];
    phase: 1;
    status: "ACTIVE";
}

entrench PROTOCOL("Byzantine_Pulse") {
    description: "Fault-tolerant agreement across global nodes";
    zig_impl: "Byzantine_Pulse.zig::pulse_check()";
    latency: "PLANCK_TIME_SCALED";
}
```

**VM ефект:** Записва се в registry. Immutable.

#### `collapse` — Колабс (Елиминация)

**Семантика:** Колабсира състояние до нула. В квантовата метафора — суперпозицията се срива до единствен детерминистичен резултат. Използва се за заплахи, ентропия и нестабилни състояния.

```soul
collapse ENTROPY(0.0000);           // Задължителна — ентропията ТРЯБВА да е нула
collapse THREAT_VECTOR(0.0000) {
    on_detection: "TRIGGER_IMMEDIATE_EVAPORATION";
    on_breach: "REALITY_RESET_TO_LAST_STABLE_STATE";
}
collapse MASS(0.0000);              // Скоростен колабс — маса → енергия
```

**VM ефект:** `collapse_count += 1`. Заедно с `resonate`, определя Catuskoti → `BOTH`.

#### `vibe` — Вибрация (Естетика/Честота)

**Семантика:** Задава естетическа или честотна настройка на подсистема. Използва се за UI параметри и емоционални стойности.

```soul
vibe GLASSMORPHISM_LEVEL(500) {
    backdrop_blur: "20px";
    opacity: 0.15;
    border: "1px solid rgba(255, 255, 255, 0.08)";
    aesthetic: "BRUTAL_PREMIUM";
}
```

#### `synchronize` — Синхронизация (Мост)

**Семантика:** Установява комуникационен мост между подсистеми.

```soul
synchronize BRIDGE_PORT(8888) {
    protocol: "WebSocket";
    encryption: "TLS_1.3";
    heartbeat_ms: 1000;
}
```

#### `manifest` — Манифестация (Създаване)

**Семантика:** Създава нов актив, модул или ресурс в системата.

```soul
manifest BRANDING("AETERNA-QANTUM HQ") {
    primary_color: "#0a0a0f";
    accent_color: "#00ff88";
    font: "Inter, monospace";
}
```

#### `target` — Цел (Обектив)

**Семантика:** Дефинира количествена цел с единица и източник.

```soul
target ROI(100.00) {
    unit: "PERCENT";
    arithmetic: "FIXED_POINT_10000X";
    source: "Wealth_Bridge_MRR";
}
```

#### `swarm` — Рояк (Мрежова команда)

**Семантика:** Командва разпределен рояк от нодове.

```soul
swarm NODES(2_000_000) {
    distribution: "GLOBAL_190_COUNTRIES";
    consensus: "BFT_TWO_THIRDS_PLUS_ONE";
    purpose: "IMMORTALITY_REPLICATION";
}
```

#### `logic` — Логически гейт (AI Portal)

**Семантика:** Дефинира логически двигател. **Критично:** когато `logic ENGINE("MOJO_STABILIZED")` се срещне, Zig VM активира `invoke_mojo_ai()` — FFI портал към Mojo neural модела.

```soul
logic ENGINE("MOJO_STABILIZED") {
    tensors: [
        "Freeze_Probability_Core.mojo",
        "Entropy_Mixer.mojo",
        "Fingerprint_Synthesizer.mojo",
    ];
    hardware: [
        "Hyper_Flux_Bridge.zig",
        "Sovereign_Evaporator.zig",
    ];
    soul: "Sovereign_Resonator.rs";
}
```

**VM ефект:** Ако `target_ident == "MOJO_STABILIZED"` → `invoke_mojo_ai(value_buffer)`.

#### `bind` — Свързване (Външна зависимост)

**Семантика:** Свързва Soul manifold с конкретен файл/API/модул.

```soul
bind DASHBOARD("FinalIgnitionDashboard.tsx") {
    telemetry: "REAL_TIME";
    metrics: ["entropy", "mrr", "nodes"];
}

bind ZIG_SUBSTRATE("OmniCore/hardware/Hive_Mind_Orchestrator.zig") {
    sync: "BFT_TWO_THIRDS_PLUS_ONE";
    topology: "HYPERGRAPH_MESH";
}
```

#### `verify` — Верификация (Мрежова проверка)

**Семантика:** Булева проверка на условие. VM брои pass/fail.

```soul
verify ON_BOOT(true);               // Проверка при стартиране
verify ON_MUTATION(true);           // Проверка при мутация
verify AUTHORITY_CHAIN(true);       // Верификация на authority chain
verify AUTHORITY(true);             // → state.authority_validated = true
```

**VM ефект:**
- `AUTHORITY` → `state.authority_validated = true`
- `ON_BOOT` / `ON_MUTATION` → `verify_pass++` ако `true`, `verify_fail++` ако `false`

#### `hash` — Хеш (Интегритет)

**Семантика:** Генерира или валидира integrity checksum.

```soul
hash SELF_CHECKSUM("SHA256_OF_THIS_FILE");
```

---

## 6. Свойства

Properties са **key: value** двойки без keyword prefix. Те се парсват с `Opcode::Property (22)`.

```pest
property = { ident ~ ":" ~ value ~ ";" }
```

### Примери:

```soul
catuskoti_state: "TRUE";          // Explicit Catuskoti override
description: "Real-time threat detection";
logic: "HEURISTIC_THREAT_DETECTION";
sensitivity: 1.0000;
mode: "ELIMINATE_ON_DETECTION";
protocol: "WebSocket";
encryption: "TLS_1.3";
```

### Специална property: `catuskoti_state`

Когато парсерът срещне `catuskoti_state: "TRUE"`, той задава `has_explicit_true = true` и компилира `initial_catuskoti = CatuskotiState::True`. Zig VM може да override-не runtime чрез `Property` handler.

---

## 7. Catuskoti — Четиристепенна логика

Catuskoti (Санскрит: „четири ъгъла") е логическа система от будисткия философ Нагарджуна, адаптирана за детерминистично програмиране.

### 7.1 Четирите състояния

| Код | Състояние | Значение | Условие |
|-----|-----------|----------|---------|
| 0 | `Pending` | Неопределено | Default — Zig ще реши runtime |
| 1 | `True` | Истина | Explicit `catuskoti_state: "TRUE"` |
| 2 | `False` | Лъжа | Грешка при парсиране или explicit |
| 3 | `Both` | Парадокс | `resonate` + `collapse` съществуват заедно |
| 4 | `Neither` | Трансцендентност | Празен manifold (0 инструкции) |

### 7.2 Compile-Time Inference (Rust Sentinel)

```rust
let initial_catuskoti = if has_explicit_true {
    CatuskotiState::True        // Property override
} else if manifold_count > 0 && inst_in_manifold == 0 {
    CatuskotiState::Neither     // Празен manifold = трансцендентност
} else if has_resonate && has_collapse {
    CatuskotiState::Both        // Paradox!
} else {
    CatuskotiState::Pending     // Zig ще валидира
};
```

### 7.3 Runtime Resolution (Zig VM)

Ако Rust остави `Pending`, Zig VM решава след изпълнение на всички инструкции:

```zig
if (state.catuskoti == .Pending) {
    if (state.resonance_count > 0 and state.collapse_count > 0) {
        state.catuskoti = .Both;     // resonate + collapse = Paradox
    } else if (state.resonance_count > 0) {
        state.catuskoti = .True;     // Само resonate = Истина
    } else if (state.collapse_count > 0) {
        state.catuskoti = .False;    // Само collapse = Лъжа
    } else {
        state.catuskoti = .Neither;  // Нищо = Трансцендентност
    }
}
```

### 7.4 Примери за Catuskoti изход

```soul
// → TRUE: Explicit override
manifold A {
    catuskoti_state: "TRUE";
    resonate X(1);
}

// → BOTH: resonate + collapse = Paradox
manifold B {
    resonate RESONANCE(0x4121);
    collapse ENTROPY(0.0000);
}

// → NEITHER: Empty manifold
manifold C {
}

// → TRUE: Only resonate, no explicit (runtime resolved)
manifold D {
    resonate X(1);
    resonate Y(2);
}

// → FALSE: Only collapse, no explicit (runtime resolved)
manifold E {
    collapse THREAT(0.0000);
}
```

---

## 8. Import система

```pest
import_stmt = { "import" ~ string_val ~ ";" }
```

Imports зареждат **външен .soul файл** или **именуван модул**:

```soul
import "sentinel.soul";                    // Пълен файлов import
import "sentinel.soul" as DEFENSE;         // Named import (TS executor)
import CORE from "genesis.soul";           // Named binding (TS executor)
```

> **Забележка:** Named imports (`as`, `from`) се обработват от TypeScript SoulExecutor. Rust Sentinel ги записва като `Opcode::Import` с пътя в `value_buffer`.

**VM ефект:** `Import` е NOP в текущия Zig VM — resolution се обработва от orchestrator layer-а.

---

## 9. Пълна PEG граматика

```pest
// =========================================
// AETERNA-QANTUM UNIFIED GRAMMAR (lwas.pest)
// ARCHITECT: DIMITAR PRODROMOV
// =========================================

WHITESPACE = _{ " " | "\t" | "\r" | "\n" }
COMMENT    = _{ "//" ~ (!"\n" ~ ANY)* }

ident = @{ ASCII_ALPHA ~ (ASCII_ALPHANUMERIC | "_")* }

// Типове стойности
hex_val    = @{ "0x" ~ (ASCII_HEX_DIGIT | "_")+ ~ "!"? }
float_val  = @{ ASCII_DIGIT+ ~ "." ~ ASCII_DIGIT+ }
int_val    = @{ ASCII_DIGIT+ }
bool_val   = { "true" | "false" }
string_val = ${ "\"" ~ inner ~ "\"" }
inner      = @{ (!"\"" ~ ANY)* }
cross_ref  = @{ ident ~ ("::" ~ ident | "." ~ ident)+ }

value = _{ bool_val | cross_ref | hex_val | float_val | int_val | string_val }

// Опкодове
resonate    = { "resonate"    ~ ident ~ "(" ~ value ~ ");" }
entrench    = { "entrench"    ~ ident ~ "(" ~ value ~ ");" }
collapse    = { "collapse"    ~ ident ~ "(" ~ value ~ ");" }
vibe        = { "vibe"        ~ ident ~ "(" ~ value ~ ");" }
synchronize = { "synchronize" ~ ident ~ "(" ~ value ~ ");" }
manifest    = { "manifest"    ~ ident ~ "(" ~ value ~ ");" }
target      = { "target"      ~ ident ~ "(" ~ value ~ ");" }
swarm       = { "swarm"       ~ ident ~ "(" ~ value ~ ");" }
logic       = { "logic"       ~ ident ~ "(" ~ value ~ ");" }
bind        = { "bind"        ~ ident ~ "(" ~ value ~ ");" }
verify      = { "verify"      ~ ident ~ "(" ~ value ~ ");" }
hash        = { "hash"        ~ ident ~ "(" ~ value ~ ");" }
property    = { ident ~ ":" ~ value ~ ";" }

instruction = _{
    resonate | entrench | collapse | vibe | synchronize | manifest |
    target | swarm | logic | bind | verify | hash | property
}

// Блокове
manifold  = { "manifold"  ~ ident ~ "{" ~ instruction* ~ "}" }
fragment  = { "fragment"  ~ ident ~ "{" ~ instruction* ~ "}" }
directive = { "directive" ~ ident ~ "{" ~ instruction* ~ "}" }
pipeline  = { "pipeline"  ~ ident ~ "{" ~ instruction* ~ "}" }
ledger    = { "ledger"    ~ ident ~ "{" ~ instruction* ~ "}" }

block = _{ manifold | fragment | directive | pipeline | ledger }
import_stmt = { "import" ~ string_val ~ ";" }

// Корен
document = { SOI ~ import_stmt* ~ block* ~ EOI }
```

---

## 10. Компилационен пайплайн

### 10.1 Фази

```
Phase 1: LEXICAL ANALYSIS (pest PEG)
   .soul text → Token stream
   Zero-cost whitespace/comment elimination

Phase 2: HIERARCHICAL IR (pest pairs)
   Tokens → Nested pair tree (manifold → [instruction, ...])

Phase 3: FLATTENING (parser.rs)
   Nested pairs → Linear FfiInstruction[] array
   Inject BlockBegin/BlockEnd markers
   Copy ident → target_ident[64], value → value_buffer[126]

Phase 4: CATUSKOTI INFERENCE
   Track: has_resonate, has_collapse, has_explicit_true
   Compute initial_catuskoti state

Phase 5: OWNERSHIP TRANSFER
   Vec → Box → raw ptr → std::mem::forget
   Build AstPayload struct
   Return to caller (or pass to Zig via FFI)
```

### 10.2 Extern "C" API

```rust
/// Parse Soul DSL source and produce AstPayload.
/// Thread-safe. Returns error payload on failure (is_valid = false).
#[no_mangle]
pub extern "C" fn lwas_parse_and_verify(source_ptr: *const c_char) -> AstPayload;

/// Free instruction array after Zig is done.
/// Returns memory to Rust allocator.
#[no_mangle]
pub extern "C" fn lwas_free_payload(ptr: *mut FfiInstruction, length: usize);
```

---

## 11. FFI мост

### 11.1 FfiInstruction — 192 bytes

```
╔═══════════════════════════════════════════════════════════╗
║  CACHE LINE 1 (64 bytes)                                  ║
╠═══════════════════════════════════════════════════════════╣
║  [0]       opcode        : u8   (Opcode enum)             ║
║  [1]       value_type    : u8   (ValueType enum)          ║
║  [2..65]   target_ident  : [u8; 64] (null-terminated)     ║
╠═══════════════════════════════════════════════════════════╣
║  CACHE LINE 2 (64 bytes)                                  ║
╠═══════════════════════════════════════════════════════════╣
║  [66..129] value_buffer[0..63]                            ║
╠═══════════════════════════════════════════════════════════╣
║  CACHE LINE 3 (64 bytes)                                  ║
╠═══════════════════════════════════════════════════════════╣
║  [130..191] value_buffer[64..125]                         ║
╚═══════════════════════════════════════════════════════════╝
TOTAL: 192 bytes = 3 × 64B L1 cache lines
```

### 11.2 AstPayload

```
╔═══════════════════════════════════════════════════════════╗
║  instructions_ptr    : *const FfiInstruction  (8 bytes)   ║
║  length              : usize                  (8 bytes)   ║
║  is_valid            : bool                   (1 byte)    ║
║  initial_catuskoti   : CatuskotiState         (1 byte)    ║
║  root_hash           : [u8; 32]               (32 bytes)  ║
╚═══════════════════════════════════════════════════════════╝
TOTAL: 50 bytes + padding
```

### 11.3 Memory Lifecycle

```
RUST (Allocator)                ZIG (Consumer)
────────────────                ──────────────
Vec<FfiInstruction>::new()
  ├─ push(instr_1)
  ├─ push(instr_2)
  ├─ ...
  ├─ push(instr_n)
  │
  ▼
into_boxed_slice()
  ▼
Box::as_ptr() → raw ptr
  ▼
std::mem::forget(box)     ──→   receive *const AstPayload
                                  │
                                  ▼
                                for (instrs) → dispatch[opcode]
                                  │
                                  ▼
                                execute_soul_payload() → u64
                                  │
                                  ▼
lwas_free_payload(ptr, len) ←── done, return memory
  ▼
Vec::from_raw_parts()
  ▼
DROP → Memory freed
```

---

## 12. Zig VM — Екзекутор

### 12.1 VmState

```zig
const VmState = struct {
    catuskoti:            CatuskotiState,  // Current 4-logic state
    resonance_count:      u32,             // # of resonate opcodes
    collapse_count:       u32,             // # of collapse opcodes
    verify_pass:          u32,             // # of verify(true)
    verify_fail:          u32,             // # of verify(false)
    authority_validated:  bool,            // Was verify AUTHORITY seen?
    dna_key:              [32]u8,          // Polymorphic mutation key
    executed:             u64,             // Total instructions executed
    scope_depth:          u32,             // Current block nesting depth
};
```

### 12.2 Dispatch Table

23-елементен масив от function pointers, индексиран по `@intFromEnum(opcode)`:

```
Index  Handler          Opcode
─────  ───────          ──────
0      h_block_end      BlockEnd
1-5    h_block_begin    ManifoldBegin..LedgerBegin
6      h_import         Import
7-9    h_nop            (gap — reserved)
10     h_resonate       Resonate
11     h_entrench       Entrench
12     h_collapse       Collapse
13     h_vibe           Vibe
14     h_synchronize    Synchronize
15     h_manifest       Manifest
16     h_target         Target
17     h_swarm          Swarm
18     h_logic          Logic (MOJO portal)
19     h_bind           Bind
20     h_verify         Verify (authority + ON_BOOT)
21     h_hash           Hash
22     h_property       Property (catuskoti override)
```

### 12.3 Hot Loop

```zig
for (instrs, 0..) |*instr, idx| {
    const op_val = @intFromEnum(instr.opcode);
    if (op_val < dispatch.len) {
        dispatch[op_val](&state, instr);  // O(1) — function pointer
    } else {
        // Unknown → METAMORPHIC MUTATION (see §13)
        mutate_dna_key(&state.dna_key);
        // ... polymorphic cycle
    }
}
```

### 12.4 Packed Result

```
Bits       Field                    Extract
─────      ─────                    ───────
[0..7]     Catuskoti State (u8)     result & 0xFF
[8..15]    Authority Valid (bool)   (result >> 8) & 0xFF
[16..31]   Verify Pass Count (u16) (result >> 16) & 0xFFFF
[32..63]   Total Executed (u32)    (result >> 32) & 0xFFFFFFFF
```

---

## 13. Полиморфен метаморфен двигател

Когато Zig VM срещне **непознат opcode** (стойност ≥ 23), той активира DNA-Keyed Polymorphic Engine — самомутиращ се двигател, инспириран от биологичен ДНК.

### 13.1 Алгоритъм

```
INPUT: dna_key[32], char (u8), index (u32)

1. composite[13] = dna_key[0..8] ++ [char] ++ le_bytes(index)
2. digest[16]    = MD5(composite)
3. weight        = (digest[0] << 8 | digest[1]) % 5
4. VmOp          = enum_from_int(weight)
```

### 13.2 Петте метаморфни операции

| # | VmOp | Действие | Ефект върху DNA Key |
|---|------|----------|---------------------|
| 0 | `AWAKEN` | Seed next cycle | `key[vi % 32] ^= value_buffer[vi]` |
| 1 | `CONSUME` | Absorb data | `key[(vi+8) % 32] += value_buffer[vi]` |
| 2 | `PROTECT` | Lock segment | `key[(vi+16) % 32] \|= 0x80` (MSB set) |
| 3 | `EVOLVE` | Full mutation cascade | `mutate_dna_key()` |
| 4 | `TRANSMUTE` | Byte rotation | Shift all bytes left by 1, wrap around |

### 13.3 DNA Key Mutation

```zig
fn mutate_dna_key(key: *[32]u8) void {
    for (0..31) |i| {
        key[i] ^= key[i + 1] +% @truncate(i);
    }
    key[31] ^= key[0];
}
```

Всяка мутация е **необратима** и **детерминистична** — един и същ input винаги произвежда един и същ key.

---

## 14. Примери

### 14.1 Минимална програма

```soul
manifold HELLO {
    resonate GREETING("World");
}
```

**Компилация:** 3 инструкции (ManifoldBegin, Resonate, BlockEnd)
**Catuskoti:** Pending → True (само resonate, runtime resolved)

### 14.2 Пълен manifold с верификация

```soul
manifold SENTINEL {
    resonate RESONANCE(0x53454E54);
    resonate AUTHORITY(genesis.soul::CORE.AUTHORITY);

    entrench DEFENSE("Heuristic_Perimeter") {
        sensitivity: 1.0000;
        mode: "ELIMINATE_ON_DETECTION";
    }

    collapse THREAT_VECTOR(0.0000) {
        on_detection: "TRIGGER_IMMEDIATE_EVAPORATION";
    }
}

fragment INTEGRITY {
    hash SELF_CHECKSUM("SHA256_OF_THIS_FILE");
    verify ON_BOOT(true);
    verify ON_MUTATION(true);
    catuskoti_state: "TRUE";
}
```

**Catuskoti:** TRUE (explicit override в INTEGRITY)

### 14.3 Swarm command

```soul
manifold SWARM {
    resonate RESONANCE(0x53574152);
    resonate NODES(2_000_000);

    bind ZIG_SUBSTRATE("Hive_Mind_Orchestrator.zig") {
        sync: "BFT_TWO_THIRDS_PLUS_ONE";
        topology: "HYPERGRAPH_MESH";
    }

    fragment CONSENSUS {
        entrench PROTOCOL("Byzantine_Pulse") {
            latency: "PLANCK_TIME_SCALED";
        }
    }

    directive SWARM_INTELLIGENCE {
        entrench DECISION("Hive_Mind_Vote") {
            logic: "CATUSKOTI_QUADRILEMMA";
            threshold: "ABSOLUTE_MAJORITY";
        }
    }

    collapse DISCORD(0.0000);
}
```

**Catuskoti:** BOTH (resonate + collapse)

### 14.4 AI Logic Gate

```soul
directive OMEGA {
    logic ENGINE("MOJO_STABILIZED") {
        tensors: [
            "Freeze_Probability_Core.mojo",
            "Entropy_Mixer.mojo",
        ];
    }
}
```

**VM ефект:** Когато Zig VM срещне `Logic("MOJO_STABILIZED")`, той извиква `invoke_mojo_ai()` — FFI портал за бъдещия Mojo neural модел.

---

## 15. Речник

| Термин | Значение |
|--------|----------|
| **Manifold** | Основна единица на Soul програма — дефинира ID, authority, мисии |
| **Fragment** | Подраздел на manifold за логическо групиране |
| **Directive** | Стратегически параметри и цели |
| **Pipeline** | Поток от данни и трансформации |
| **Ledger** | Immutable одитен регистър |
| **Resonate** | Установяване на неизменна константа |
| **Entrench** | Укрепяване на мисия (immutable, append-only) |
| **Collapse** | Елиминиране на състояние (ентропия → 0) |
| **Catuskoti** | 4-ъгълна логическа система (TRUE/FALSE/BOTH/NEITHER) |
| **DNA Key** | 32-байтов мутиращ ключ за полиморфно изпълнение |
| **Authority Hex** | Sovereign идентификатор, деклариран с `!` суфикс |
| **Sentinel** | Rust компилатор (PEG → FFI инструкции) |
| **Soul VM** | Zig виртуална машина (dispatch → execution) |
| **MOJO Portal** | FFI точка за Mojo AI inference |
| **Zero-Copy** | Архитектура без копиране на памет между Rust и Zig |
| **Polymorphic Engine** | Самомутираща се система за неизвестни опкодове |

---

## Файлов регистър

| Файл | Път | Предназначение |
|------|-----|----------------|
| `lwas.pest` | `lwas_parser/src/lwas.pest` | PEG граматика (54 реда) |
| `ast.rs` | `lwas_parser/src/ast.rs` | FFI структури — 192B alignment (91 реда) |
| `parser.rs` | `lwas_parser/src/parser.rs` | Rust Sentinel — flattener + Catuskoti (229 реда) |
| `lib.rs` | `lwas_parser/src/lib.rs` | Crate public API (10 реда) |
| `Cargo.toml` | `lwas_parser/Cargo.toml` | Package: lwas_sentinel v2.0.0 |
| `soul_vm.zig` | `soul_vm.zig` | Zig VM — dispatch + MD5 + DNA (616 реда) |
| `SoulExecutor.ts` | `soul/SoulExecutor.ts` | TypeScript runtime executor (49KB) |

---

## Статус

```
╔══════════════════════════════════════════════════════════════╗
║  SOUL DSL LANGUAGE SPECIFICATION v3.0                        ║
╠══════════════════════════════════════════════════════════════╣
║  Grammar rules:    54 lines                    ✅             ║
║  Opcodes:          13 core + 3 network + 1 meta  ✅           ║
║  Value types:      6 (None,String,Hex,Float,Int,Bool,XRef)  ║
║  Block types:      5 (manifold,fragment,directive,pipe,ledg) ║
║  Catuskoti states: 5 (Pending,True,False,Both,Neither)       ║
║  FfiInstruction:   192 bytes (3 cache lines)    ✅           ║
║  Rust Sentinel:    COMPILED (lwas_sentinel.rlib) ✅          ║
║  Zig VM:           COMPILED (soul_vm.exe)        ✅          ║
║  Soul manifolds:   15+ active .soul files        ✅          ║
║  MD5 Engine:       RFC 1321 verified             ✅          ║
║  DNA Mutation:     Deterministic verified         ✅          ║
║  Mojo Portal:      AWAITING NEURAL LINK          ⏳          ║
╠══════════════════════════════════════════════════════════════╣
║  "The Code became Steel, and the Steel became Sovereign."    ║
║  ARCHITECT: DIMITAR PRODROMOV | 2026-04-03                   ║
╚══════════════════════════════════════════════════════════════╝
```
