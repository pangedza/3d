import math
import cadquery as cq

# =========================
# PARAMETERS (mm)
# =========================
D_round = 40.0
T_round = 6.0

# Bolt pattern
bolt_count = 3
bolt_d = 3.2
bolt_circle_d = 28.0

# Center mounting
center_hole_d = 6.2
center_hole_depth = 0.0  # 0 = through hole, otherwise blind depth

# Optional countersink / counterbore
use_countersink = False
countersink_d = 6.4
countersink_angle = 90

use_counterbore = False
counterbore_d = 6.0
counterbore_depth = 2.0

# Optional top chamfer
top_chamfer = 0.3

# =========================
# BUILD PLATFORM
# =========================
body = cq.Workplane("XY").circle(D_round / 2).extrude(T_round)

if top_chamfer > 0:
    body = body.edges("|Z and >Z").chamfer(top_chamfer)

# Center hole
if center_hole_d > 0:
    if center_hole_depth and center_hole_depth > 0:
        body = body.faces(">Z").workplane().hole(center_hole_d, center_hole_depth)
    else:
        body = body.faces(">Z").workplane().hole(center_hole_d)

# Bolt holes
if bolt_count > 0:
    radius = bolt_circle_d / 2
    angles = [i * 360.0 / bolt_count for i in range(bolt_count)]
    points = [(radius * math.cos(math.radians(a)), radius * math.sin(math.radians(a))) for a in angles]

    wp = body.faces(">Z").workplane().pushPoints(points)
    if use_countersink:
        body = wp.cskHole(bolt_d, countersink_d, countersink_angle)
    elif use_counterbore:
        body = wp.cboreHole(bolt_d, counterbore_d, counterbore_depth)
    else:
        body = wp.hole(bolt_d)

# =========================
# EXPORT
# =========================
cq.exporters.export(body, "platform_round.step")
cq.exporters.export(body, "platform_round.stl")

print("Created: platform_round.step, platform_round.stl")
