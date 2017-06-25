import os

hu = 0
bu = 0
bp = 0
dc = 0
ti = 0
lo = 0
ch = 0
sc = 0
dk = 0

for path, dirs, files in os.walk('C:\\Project\\2017Hackthon\\data\\audio\\Full'):
    for f in files:
        if f.endswith('hu.wav'):
            hu+=1
        if f.endswith('bu.wav'):
            bu+=1
        if f.endswith('bp.wav'):
            bp += 1
        if f.endswith('dc.wav'):
            dc += 1
        if f.endswith('ti.wav'):
            ti += 1
        if f.endswith('lo.wav'):
            lo += 1
        if f.endswith('ch.wav'):
            ch += 1
        if f.endswith('sc.wav'):
            sc += 1
        if f.endswith('dk.wav'):
            dk += 1

sum = hu + bu + bp + dc + ti + lo + ch + sc + dk
print  ("hu (%d) %f" %(hu,hu/sum))
print  ("bu (%d) %f" %(bu,bu/sum))
print  ("bp (%d) %f" %(bp,bp/sum))
print  ("dc (%d) %f" %(dc,dc/sum))
print  ("ti (%d) %f" %(ti,ti/sum))
print  ("lo (%d) %f" %(lo,lo/sum))
print  ("ch (%d) %f" %(ch,ch/sum))
print  ("sc (%d) %f" %(sc,sc/sum))
print  ("dk (%d) %f" %(dk,dk/sum))
