
safe_height = 20 # mm

pnp_instructions = []
bom_instructions = []
tapes_positions = []
instructions = []

def get_mm(nice_string):
    if nice_string[-3:] == "mil": # mil
        return round(float(nice_string[:-3])*0.0254, 5)
    else: # mm
        return round(float(nice_string[:-2]), 5)

with open("pnp.csv") as fp:
    _ = fp.readline()
    while (True):
        line = fp.readline()
        if not line or line == "\x00":
            break
        line = [l.replace('\x00', "") for l in line.replace('"', '').split()]
        line[2] = get_mm(line[2])
        line[3] = get_mm(line[3])
        line[9] = int(line[9])
        pnp_instructions.append(line)

with open("bom.csv") as fp:
    _ = fp.readline()
    while (True):
        line = fp.readline()
        if not line or line == "\x00":
            break
        line = [l.replace('\x00', "") for l in line.split()]
        line[2] = line[2].split(",")
        bom_instructions.append(line)

with open("tapes_positions.csv") as fp:
    _ = fp.readline()
    while (True):
        line = fp.readline()
        if not line or line == "\x00":
            break
        line = [l.replace('\x00', "") for l in line.split()]
        line[1] = get_mm(line[1])
        line[2] = get_mm(line[2])
        line[3] = get_mm(line[3])
        line[4] = float(line[4])
        line[5] = get_mm(line[5])
        line[6] = float(line[6])
        tapes_positions.append(line)
    

print("")
print("PNP")
for pnp_instruction in pnp_instructions:
    print(pnp_instruction)
print("")
print("BOM")
for bom_instruction in bom_instructions:
   print(bom_instruction)
print("")
print("tapes_positions")
for tapes_position in tapes_positions:
    print(tapes_position)
print("")

print("CREATING INSTRUCTIONS FOR THE MACHINE")
for pnp_instruction in pnp_instructions:
    designator = pnp_instruction[0]

    instructions.append("== "+str(designator))
    instructions.append("calibrate")
    instructions.append("zmove "+str(safe_height))
    
    for bom_comp in bom_instructions:
        if designator in bom_comp[2]:
            manafacture_part = bom_comp[5]
            for tape_reel in tapes_positions:
                if (tape_reel[0] == manafacture_part):
                    instructions.append("xmove "+str(tape_reel[1]))
                    instructions.append("ymove "+str(tape_reel[2]))
                    instructions.append("zmove "+str(tape_reel[3]))
                    instructions.append("startsuction")
                    instructions.append("zmove "+str(safe_height))
                    instructions.append("xmove "+str(pnp_instruction[2]))
                    instructions.append("ymove "+str(pnp_instruction[3]))
                    
                    from_pos = tape_reel[6]         # 320  90
                    to_pos = pnp_instruction[9]     # 90   270

                    forward = (360-from_pos) + to_pos if from_pos > to_pos else to_pos - from_pos
                    backward = from_pos - to_pos if from_pos > to_pos else from_pos + (360 - to_pos)
                    to_rotate = forward if forward < backward else backward * -1

                    if (to_rotate != 0):
                        instructions.append("rotate "+str(to_rotate)) 

                    instructions.append("zmove "+str(tape_reel[3]))
                    instructions.append("stopsuction")
                    instructions.append("zmove "+str(safe_height))
                

for instruction in instructions:
    print(instruction)

print("")