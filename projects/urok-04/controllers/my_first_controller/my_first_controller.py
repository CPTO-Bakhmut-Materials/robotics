"""my_first_controller: мій перший контролер робота."""

from controller import Robot

# Створюємо робота: через цей об'єкт програма спілкується з Webots
robot = Robot()

# Крок симуляції в мілісекундах (поле basicTimeStep вузла WorldInfo)
timestep = int(robot.getBasicTimeStep())

print("Привіт! Мене звати", robot.getName())
print("Крок симуляції:", timestep, "мс")

step = 0  # лічильник виконаних кроків

# Головний цикл: кожен виклик robot.step() просуває симуляцію на timestep мс
while robot.step(timestep) != -1:
    step = step + 1

    # Друкуємо не кожен крок, а кожен 30-й (30 × 32 мс ≈ 1 секунда)
    if step % 30 == 0:
        print("Крок", step, "| час", round(robot.getTime(), 2), "с")

    # Через 5 секунд симуляції виходимо з циклу
    if robot.getTime() >= 5:
        print("Минуло 5 секунд. Завершую роботу.")
        break

print("Контролер завершено.")
