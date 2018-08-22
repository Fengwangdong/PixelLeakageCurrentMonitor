import os

inputFileName = "leakageCurrents.txt"
moduleFileName = "powermap.list"
moduleOutputName = "moduleCurrents.txt"

if(os.path.exists(inputFileName) and os.path.exists(moduleFileName)):
    fin = open(inputFileName, "r+")
    lines = fin.readlines()

    fModule = open(moduleFileName, "r+")
    moduleList = fModule.readlines()

    fout = open(moduleOutputName, "w")

    for l in lines:
        line = l.split()

        alias = line[0].replace("PixelEndCap","FPix")
        alias = alias.replace("ROG","PG")

        for iModule in moduleList:
            module = iModule.split()

            if (module[2] in alias) and (module[0][-4:] in alias):
                moduleCurrent = float(line[1])*16.0
                fout.write(module[0] + " " + str(moduleCurrent) + "\n")

    fout.close()
    fModule.close()
    fin.close()
