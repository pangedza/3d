import cadquery as cq

# =========================
# PARAMETERS (mm)
# =========================
L = 94.0
OD = 11.0

# Bottom insert hole
insert_d = 6.0
insert_depth = 12.0

# Top magnet hole
mag_d = 4.0
mag_depth = 6.0

# Top cap style
cap_style = "hemisphere"  # "hemisphere" or "fillet"
top_fillet_r = 4.5

# Print fit tweak
od_adjust = 0.0

# =========================
# BUILD BUSHING
# =========================
r = (OD + od_adjust) / 2
core_h = L - r if cap_style == "hemisphere" else L

body = cq.Workplane("XY").circle(r).extrude(core_h)

if cap_style == "hemisphere":
    cap = cq.Workplane("XY").sphere(r).translate((0, 0, core_h))
    body = body.union(cap)
else:
    body = body.edges("|Z and >Z").fillet(min(top_fillet_r, r - 0.2))

# Bottom hole for insert
body = body.faces("<Z").workplane().hole(insert_d, insert_depth)

# Top hole for magnet
body = body.faces(">Z").workplane().hole(mag_d, mag_depth)

# =========================
# EXPORT
# =========================
cq.exporters.export(body, "bushing.step")
cq.exporters.export(body, "bushing.stl")

print("Created: bushing.step, bushing.stl")
