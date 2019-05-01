import json
import os
import shutil

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

for filename in os.listdir(os.path.dirname(os.path.realpath(__file__))):
   if filename.endswith(".endcity"):
      f = open(filename)
      print "Compiling", filename
      lang = load("lang.json")
      lines = f.read().splitlines()
      # Setup
      i = 1
      Compile = True
      mcf = []
      namespace = "endcity"
      name = filename.split(".endcity")[0]
      for line in lines:
         # Reading
         firstsplit = line.split("--")
         split = line.split(" ")
         if len(firstsplit) > 1:
            firstsplit = firstsplit[1].split(":")
            if firstsplit[0] == "namespace":
               namespace = firstsplit[1]
            if firstsplit[0] == "name":
               name = firstsplit[1]
         elif split[0] == "":
            continue
         elif split[0] in lang["commands"]:
           mcf.append(line)
         else:
            try:
               newcmd = ""
               if lang["code"][split[0]] != None:
                  if len(split)-1 < lang["code"][split[0]]["requiredarguments"]:
                     print "[ERROR]", split[0], "takes at least", str(lang["code"][split[0]]["requiredarguments"]), "arguments and at most", str(lang["code"][split[0]]["arguments"]), "arguments"
                  else:
                     try:
                        if lang["code"][split[0]]["addtoe"] != None:
                           if newcmd.split(" ")[0] != "execute":
                              newcmd = "execute as " + decode(split, split[1])
                     except KeyError:
                        cmd = lang["code"][split[0]]["cmd"]
                        splitcmd = cmd.split(" ")
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
               print split
               print lang["code"][split[0]]
               print "[ERROR] Unknown \"" + split[0] + "\" on line", str(i+1)
               Compile = False
         i += 1
      # Compile
      if Compile == False:
         print "Unable to Compile", filename + ". Fix all errors."
      if Compile == True:
         if not os.path.exists("datapack"):
            os.mkdir("datapack")
         if not os.path.exists("datapack/data"):
            os.mkdir("datapack/data")
         mcmeta = open("datapack/pack.mcmeta", "w+")
         mcmeta.write("{ \"pack\": { \"pack_format\": 1, \"description\": \"Datapack made with END-CITY\"} }")
         mcmeta.close()
         namespaces = namespace.split("/")
         ogns = namespaces[0]
         del(namespaces[0])
         if not os.path.exists("datapack/data/" + ogns):
            os.mkdir("datapack/data/" + ogns)
         if not os.path.exists("datapack/data/" + ogns + "/functions"):
            os.mkdir("datapack/data/" + ogns + "/functions")
         addon = ""
         for i in namespaces:
            if not os.path.exists("datapack/data/" + ogns + "/functions/" + addon + i):
               os.mkdir("datapack/data/" + ogns + "/functions/" + addon + i)
            if i != namespaces[-1]:
               addon += i + "/"
            else:
               addon += i
         newfile = open("datapack/data/" + ogns + "/functions/" + addon + "/" + name + ".mcfunction", "w+")
         for line in mcf:
            newfile.write(line + "\n")
         newfile.close()
         print "Compiled!"

   else:
      continue
