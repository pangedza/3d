import cadquery as cq

# =========================
# PARAMETERS (mm)
# =========================
# Base envelope
A = 120.0
B = 100.0
H_base = 12.0

# Round bearing zone (rim)
D_outer = 99.0
D_inner = 91.0
h_rim = 0.5

# Bearing seat for 635Z (OD 19, ID 5, B 6) + print clearance
Db = 19.2      # pocket diameter
Hb = 6.2       # pocket depth
D_shaft = 5.2  # through hole

# Bushing storage slot
bush_L = 94.0
bush_OD = 11.0
slot_clear = 0.4
slot_depth = 8.0
X_slot = A * 0.28
Y_slot = B * 0.50

# Neck (retention) parameters
neck_depth = 2.0
neck_d = 10.4

# Platform outline (rectangle + semicircle)
R_end = B / 2
L_rect = A - R_end

# Bearing zone center
Xc = A * 0.58
Yc = B * 0.50

# Optional bottom pockets
D_pocket = 10.0
h_pocket = 0.6
pocket_coords = [
    (15.0, 15.0),
    (A - 15.0, 15.0),
    (15.0, B - 15.0),
    (A - 15.0, B - 15.0),
]

# =========================
# BUILD BASE PLATFORM
# =========================
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(L_rect, 0)
    .threePointArc((A, B / 2), (L_rect, B))
    .lineTo(0, B)
    .close()
)

body = profile.extrude(H_base)

# Rim for bearing zone
rim = (
    cq.Workplane("XY")
    .moveTo(Xc, Yc)
    .circle(D_outer / 2)
    .circle(D_inner / 2)
    .extrude(h_rim)
    .translate((0, 0, H_base))
)
body = body.union(rim)

# Bearing pocket and shaft hole
body = (
    body
    .faces(">Z")
    .workplane()
    .moveTo(Xc, Yc)
    .hole(Db, Hb)
)
body = (
    body
    .faces("<Z")
    .workplane()
    .moveTo(Xc, Yc)
    .hole(D_shaft)
)

# =========================
# BUSHING STORAGE SLOT
# =========================
slot_d = bush_OD + slot_clear
body = (
    body
    .faces(">Z")
    .workplane(centerOption="CenterOfBoundBox")
    .moveTo(X_slot - A / 2, Y_slot - B / 2)
    .slot2D(bush_L, slot_d)
    .cutBlind(slot_depth)
)

# Rounded niche at one end of slot (for bushing cap)
r_cap = slot_d / 2
cap_center_x = (X_slot - A / 2) + bush_L / 2
cap_center_y = (Y_slot - B / 2)
cap_center_z = H_base - slot_depth + r_cap
sphere_cut = cq.Workplane("XY").sphere(r_cap).translate(
    (cap_center_x, cap_center_y, cap_center_z)
)
body = body.cut(sphere_cut)

# Neck (retention) slot from top
body = (
    body
    .faces(">Z")
    .workplane(centerOption="CenterOfBoundBox")
    .moveTo(X_slot - A / 2, Y_slot - B / 2)
    .slot2D(bush_L, max(1.0, neck_d))
    .cutBlind(neck_depth)
)

# =========================
# OPTIONAL BOTTOM POCKETS
# =========================
if D_pocket > 0 and h_pocket > 0:
    for (px, py) in pocket_coords:
        body = (
            body
            .faces("<Z")
            .workplane(centerOption="CenterOfBoundBox")
            .moveTo(px - A / 2, py - B / 2)
            .hole(D_pocket, h_pocket)
        )

# =========================
# EXPORT
# =========================
cq.exporters.export(body, "platform_main.step")
cq.exporters.export(body, "platform_main.stl")

print("Created: platform_main.step, platform_main.stl")
