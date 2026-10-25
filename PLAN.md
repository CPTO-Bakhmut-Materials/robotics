# Plan: full Webots / entry-level robotics course (21 lessons × 35 min)

## Context
The site (MkDocs + Material, `docs/`, GitHub Pages at cpto-bakhmut-materials.github.io/robotics) currently
holds one introduction (chapters 01–08: what a robot is, simulation, install, interface, first world with
e-puck). The user wants a full course to get a real hand of Webots and entry-level robotics.
Decisions (from the user): **35-min lessons, Python controllers, extended scope (camera, arm, ROS 2 intro),
simulation only**. Audience: Ukrainian vocational learners (prof. 4113), near-zero robotics background,
self-study, Linux, Webots R2025a.

**Answer: 21 lessons × 35 min ≈ 12 hours**, in 6 modules. Fewer than ~14 lessons gives only "can use
Webots"; the extra 7 cover camera, navigation, arm, ROS 2 and a final project.

## Course structure

| # | Lesson (35 min) | Robotics concept | Webots assets |
|---|---|---|---|
| **Module 1. Знайомство** (existing content, regrouped) |||
| 1 | Роботи і симуляція, інтерфейс Webots (ch. 01, 02, 04; install ch. 03 = preparation before lesson) | sense–think–act | Guided Tour |
| 2 | Перший світ і перший робот (ch. 05, 06, 07) | world, node, field, controller | RectangleArena, WoodenBox, E-puck |
| **Module 2. Перші програми на Python** |||
| 3 | Перший контролер: wizard *New Robot Controller*, `Robot()`, `step()` loop, `print` | control loop, time step | Python controller |
| 4 | Мотори: їхати прямо, повертати, коло | differential drive, velocity control | e-puck motors |
| 5 | Датчики відстані: читаємо ps0–ps7, поріг | sensors, noise, thresholds | DistanceSensor |
| 6 | Власний об'їзд перешкод (if/else) | reactive behaviour | own `avoid.py` vs built-in |
| 7 | Керування з клавіатури + світлодіоди | teleoperation, actuators | Keyboard, LED |
| **Module 3. Рух за правилами** |||
| 8 | Слідування по лінії (датчики землі) | line following, bang-bang | E-puckGroundSensors, line floor |
| 9 | Плавне слідування: П-регулятор | feedback, proportional control | same world |
| 10 | Енкодери й одометрія: рівно 30 см, поворот 90° | odometry, error accumulation | PositionSensor |
| 11 | Машина станів: робот-патрульний (міні-проєкт) | state machine | arena + boxes |
| **Module 4. Робот бачить** |||
| 12 | Камера: вмикаємо, читаємо пікселі, рахуємо колір (uses the `05-camera-on` finding: built-in `e-puck_avoid_obstacles` leaves the camera black) | image = array of pixels | e-puck Camera |
| 13 | Їдемо до червоного об'єкта | visual servoing | Camera + coloured ball |
| 14 | Розпізнавання об'єктів (Recognition) | object recognition | camera_recognition |
| **Module 5. Навігація, маніпулятори, інші роботи** |||
| 15 | GPS + компас: доїхати до точки | localisation, heading | GPS, Compass |
| 16 | Маніпулятор UR5e: суглоби й позиції | joints, degrees of freedom | UR5e |
| 17 | Взяти й покласти (pick & place) | gripper, sequence of poses | UR5e + gripper |
| 18 | Інший робот — ті самі навички (TurtleBot3) | transferring code between platforms | TurtleBot3Burger |
| 19 | Знайомство з ROS 2 (огляд + демо `webots_ros2`, optional install) | nodes, topics | webots_ros2 |
| **Module 6. Фінальний проєкт** |||
| 20 | Проєкт: «робот-кур'єр» (line + obstacles + stop at target), work session | integration | own world |
| 21 | Завершення проєкту, самоперевірка, підсумок курсу | — | — |

## Lesson page template (every new lesson)
Мета · Час 35 хв · Що знадобиться (link to starter project) · Коротко теорія (≤ 8 хв) ·
Практика кроками зі скріншотами (≈ 20 хв) · Код Python (copyable block, fully commented in Ukrainian) ·
Перевірте себе (`??? success "Відповідь"`) · Чек-лист · Якщо щось пішло не так · Додаткове завдання.
Material conventions as in the README: `!!! info|warning|danger|success`, 4-space list continuation.

## Repo / site changes
- **Nav**: `docs/SUMMARY.md` becomes nested by module → lesson (literate-nav supports nesting). Existing
  chapter files keep their names (no broken links); Lesson 1–2 sections just group them.
  Glossary `08-slovnyk.md` becomes a course-wide appendix and grows with each lesson.
- **New pages**: `docs/modul-2/urok-03-pershyi-kontroler.md` … (transliterated names, one page per lesson).
- **Starter projects for self-study**: `projects/urok-NN/` (Webots project: `worlds/*.wbt` +
  `controllers/<name>/<name>.py` solution), linked from each lesson; learners download via GitHub.
- **Screenshot tooling** saved in repo `tools/screenshots/` (`ui.py` driver, `annotate.py`, `specs.py`),
  output fixed to `docs/images/` (today it still writes to root `images/`).
- **Carry-over cleanup**: move stray `images/05-camera-on.png`, `images/05-controller-choice.png` to
  `docs/images/`; use them in Lesson 12; delete root `images/`.
- Update `docs/index.md` (course overview: modules, 21 lessons, ~12 h) and memory notes.

## Delivery in phases (review with the user after each)
1. Restructure nav + template + tooling + Lesson 3 as a pilot.
2. Lessons 4–7 → 3. Lessons 8–11 → 4. Lessons 12–14 → 5. Lessons 15–19 → 6. Lessons 20–21 + overview.

## Verification (per lesson)
- Run the starter world + solution controller in the user's Webots R2025a (driven via ydotool/grim as
  before); confirm the described behaviour and console output; capture/annotate screenshots from it.
- Python controllers start without errors (console shows no traceback).
- `.venv/bin/mkdocs build --strict` passes; visual check via headless Firefox; push → GitHub Actions deploy.
