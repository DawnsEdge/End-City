import json
import os

def save(d, filename):
   file = open(filename,'w')
   json.dump(d, file)
   file.close

def load(filename):
   file = open(filename, 'r')
   d = json.load(file)
   file.close()
   return d

def decode(split, part):
   ret = part
   spart = ["", "", ""]
   spart2 = ["", "", ""]
   try:
      spart = part.split("{")
      if len(spart) > 1:
         spart2 = spart[1].split("}")
         if len(split)-1 >= int(spart2[0])+1:
            ret = split[int(spart2[0])+1]
   except KeyError:
      return "!!--==ERROR==--!!"
   return ret + spart2[1]

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
mcf = []
for line in lines:
   split = line.split(" ")
   if split[0] in lang["commands"]:
     mcf.append(line)
   else:
      try:
         if lang["code"][split[0]] != None:
            if len(split)-1 < lang["code"][split[0]]["requiredarguments"]:
               print "[ERROR]", split[0], "takes at least", str(lang["code"][split[0]]["requiredarguments"]), "arguments and at most", str(lang["code"][split[0]]["arguments"]), "arguments"
            else:
               cmd = lang["code"][split[0]]["cmd"]
               splitcmd = cmd.split(" ")
               newcmd = ""
               for part in splitcmd:
                  add = part
                  spart = part.split("|")
                  if len(spart) > 1:
                     d1 = decode(split, spart[0])
                     d2 = decode(split, spart[1])
                     if d1[0] == "{":
                        add = d2
                     else:
                        add = d1
                  else:
                     add = decode(split, part)
                  newcmd += add + " "
               mcf.append(newcmd)
      except KeyError:
         print "[ERROR] Unknown \"" + split[0] + "\" on line", str(i)
         Compile = False
   i += 1

if Compile == False:
   print "Unable to Compile. Fix all errors."
if Compile == True:
   os.mkdir("compiled")
   newfile = open("compiled/" + filename + ".mcfunction", "w+")
   for line in mcf:
      newfile.write(line + "\n")
   newfile.close()
   print "Compiled!"
