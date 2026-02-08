import cadquery as cq

# =========================
# ПЛАТФОРМА — ТВОИ РАЗМЕРЫ (как раньше)
# =========================
A = 120.0
B = 100.0
H = 14.0
H_base = 12.0

D_inner = 91.0
D_outer = 99.0
h_rim   = 0.5

# Паз (старые значения)
Lp = 94.0
Bp = 11.0
Hp = 11.0

# Низ (карманы)
D_pocket = 10.0
h_pocket = 0.1

# =========================
# ХРАНЕНИЕ ВТУЛКИ — ПАРАМЕТРЫ (под твою втулку)
# =========================
bush_L = 94.0
bush_OD = 11.0

# зазор под печать, чтобы нормально входила
clear = 0.4                  # общий зазор (0.3–0.6 обычно норм)
slot_d = bush_OD + clear     # "диаметр" канала

# глубина канала
slot_depth = min(Hp, max(2.0, H_base - 1.0))  # безопасно в пределах тела

# Горловина-пережим сверху (чтобы втулка не вылетала)
neck_depth = 2.0              # глубина узкого участка сверху
neck_d = bush_OD - 0.6        # узкое "горло" (меньше Ø втулки) — подгони, если слишком туго

# Где расположен канал (по фото он слева; оставляю как было “в районе паза”)
X_slot = A * 0.28
Y_slot = B * 0.50

# Конец платформы полукругом
R_end = B / 2
L_rect = A - R_end

# Центр чаши (примерно)
Xc = A * 0.58
Yc = B * 0.50

# Толщина тела
t_base = max(2.0, H_base - h_rim)

# Ножки (пример)
offset = 15.0
feet = [
    (offset, offset),
    (A - offset, offset),
    (offset, B - offset),
    (A - offset, B - offset),
]

# =========================
# ПОСТРОЕНИЕ ПЛАТФОРМЫ
# =========================
# Контур: прямоугольник + дуга справа
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(L_rect, 0)
    .threePointArc((A, B/2), (L_rect, B))
    .lineTo(0, B)
    .close()
)

body = profile.extrude(t_base)

# Борт чаши (как было)
rim = (
    cq.Workplane("XY")
    .moveTo(Xc, Yc)
    .circle(D_outer / 2)
    .circle(D_inner / 2)
    .extrude(h_rim)
    .translate((0, 0, t_base))
)
body = body.union(rim)

# =========================
# ДОБАВЛЯЕМ МЕСТО ХРАНЕНИЯ ВТУЛКИ
# =========================
# Канал-капсула (slot2D): длина bush_L, ширина slot_d
# Вырезаем с верхней плоскости вниз на slot_depth
body = (
    body
    .faces(">Z")
    .workplane(centerOption="CenterOfBoundBox")
    .moveTo(X_slot - A/2, Y_slot - B/2)
    .slot2D(bush_L, slot_d)      # капсула
    .cutBlind(slot_depth)
)

# Полусфера под закруглённый верх втулки:
# делаем на одном конце слота углубление сферой радиуса slot_d/2
r_cap = slot_d / 2
# Центр сферы ставим на дальний конец слота по +X (можно поменять направление, если нужно)
cap_center_x = (X_slot - A/2) + bush_L/2
cap_center_y = (Y_slot - B/2)

# Вырез сферой: чтобы не резать всё — пересекаем сферу с “коробкой” и вычитаем
sphere_cut = (
    cq.Workplane("XY")
    .sphere(r_cap)
    .translate((cap_center_x, cap_center_y, t_base - slot_depth + r_cap))
)
body = body.cut(sphere_cut)

# Горловина-пережим сверху:
# 1) Сначала режем узкий слот только на небольшую глубину (neck_depth)
# Это оставит “вход” уже, чем основной канал.
body = (
    body
    .faces(">Z")
    .workplane(centerOption="CenterOfBoundBox")
    .moveTo(X_slot - A/2, Y_slot - B/2)
    .slot2D(bush_L, max(1.0, neck_d))
    .cutBlind(neck_depth)
)

# =========================
# НОЖКИ СНИЗУ (как было)
# =========================
for (fx, fy) in feet:
    body = (
        body
        .faces("<Z")
        .workplane(centerOption="CenterOfBoundBox")
        .moveTo(fx - A/2, fy - B/2)
        .hole(D_pocket, h_pocket)
    )

# =========================
# ЭКСПОРТ
# =========================
cq.exporters.export(body, "platform_with_bushing_storage.step")
cq.exporters.export(body, "platform_with_bushing_storage.stl")

print("Готово: platform_with_bushing_storage.step и platform_with_bushing_storage.stl")
