import cadquery as cq

# =========================
# ВТУЛКА — ПАРАМЕТРЫ
# =========================
L = 94.0          # высота/длина втулки
OD = 11.0         # внешний диаметр

# Верх (магнит)
mag_d = 4.0       # отверстие под магнит
mag_depth = 6.0   # глубина отверстия под магнит (подгони под свой магнит)

# Низ (впаиваемая резьба)
insert_d = 6.0    # отверстие под впаиваемую резьбу
insert_depth = 12.0  # глубина под вставку (подгони под свою вставку)

# Закругление верха
cap_style = "hemisphere"  # "hemisphere" или "fillet"
top_fillet_r = 5.0        # если выберешь fillet

# Небольшой запас под печать
# (можешь поставить -0.05 если хочешь плотнее)
od_adjust = 0.0


# =========================
# ПОСТРОЕНИЕ ВТУЛКИ
# =========================
r = (OD + od_adjust) / 2

# Основной цилиндр (без верхушки)
core_h = L - r if cap_style == "hemisphere" else L
body = cq.Workplane("XY").circle(r).extrude(core_h)

# Закруглённая верхушка
if cap_style == "hemisphere":
    # Сфера радиуса r, центр на верхней плоскости цилиндра
    cap = cq.Workplane("XY").sphere(r).translate((0, 0, core_h))
    body = body.union(cap)
else:
    # Просто скругляем верхний край
    body = body.edges("|Z and >Z").fillet(min(top_fillet_r, r - 0.2))

# Отверстие снизу под впаиваемую резьбу Ø6
body = (
    body
    .faces("<Z")
    .workplane()
    .hole(insert_d, insert_depth)
)

# Отверстие сверху под магнит Ø4
# Важно: отверстие делаем с самой верхней точки вниз
body = (
    body
    .faces(">Z")
    .workplane()
    .hole(mag_d, mag_depth)
)

# =========================
# ЭКСПОРТ
# =========================
cq.exporters.export(body, "bushing_L94_OD11.step")
cq.exporters.export(body, "bushing_L94_OD11.stl")

print("Готово: bushing_L94_OD11.step и bushing_L94_OD11.stl")
