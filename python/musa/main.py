from musa.waves import Wave
from musa.wavers import Basic
from musa.generators import sin
from musa.scales import genscale

print("Hello musa")
scale = genscale()

basic = Basic(generator=sin, duration=1.0 / 2.0)
wave = Wave(duration=0)
for j in range(12):
    for i in range(0, 3):
        wave += basic.gen(180.0 * scale[i * 2])
wave *= 0.75
wave.save()
