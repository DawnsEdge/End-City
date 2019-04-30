import json

def save(d, filename):
   file = open(filename,'w')
   json.dump(d, file)
   file.close

def load(filename):
   file = open(filename, 'r')
   d = json.load(file)
   file.close()
   return d

noerror = False
while noerror == False:
    filename = raw_input("Name of file to compile.\n> ")
    try:
        f = open(filename + ".endcity")
        noerror = True
    except IOError:
        print "That file doesn't exsist"

lang = load("lang.json")

lines = f.read().splitlines()
i = 1
Compile = True
for line in lines:
    split = line.split(" ")
    if split[0] in lang["commands"]:
        print line
    else:
        try:
            if lang["code"][split[0]] != None:
                if len(split) < lang["code"][split[0]]["parameters"]:
                    print "[ERROR]", split[0], "takes at least", str(lang["code"][split[0]]["requiredparameters"]), "at most", str(lang["code"][split[0]]["parameters"])
                #print lang["code"][split[0]]["cmd"]
        except KeyError:
            print "[ERROR] Unknown \"" + split[0] + "\" on line", str(i)
            Compile = False
    i += 1

if Compile == False:
    print "Unable to Compile. Fix all errors."
