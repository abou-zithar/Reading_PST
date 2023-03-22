from libratom.lib.pff import PffArchive
from pathlib import Path
import pandas as pd
import re


pst_file=r"Amal Shalaby.pst"



archive = PffArchive(pst_file)
eml_out = Path(Path.cwd() / "emls")

if not eml_out.exists():
  eml_out.mkdir()

def get_to_and_from(body):
    
      To = re.findall('(?=To:).*',body,re.DOTALL)
      From = re.findall('(?=From:).*',body,re.DOTALL)
      if To == [] or From ==[]:
         return "",""
      else:
         To=To[0].split("\n")[0]
         From=From[0].split("\n")[0]

      return From , To
    


print("Writing messages to .eml")

To_list=[]
From_list=[]

for folder in archive.folders():
    # print(folder.get_number_of_sub_messages());
  for i,message in enumerate (folder.sub_messages):
    body=str(archive.format_message(message))
    target_folder = eml_out/str(i)
    target_folder.mkdir(parents=True, exist_ok=True)

    From , To= get_to_and_from(body)
    From_list.append(From)
    To_list.append(To)
    with open( target_folder/ "EMAIL_BODY.txt", "w", encoding="utf-8") as f:
      f.write(body)
          
            # name = message.subject.replace(" ", "_")
            # name = name.replace("/","-")
            # filename = eml_out / f"{message.identifier}_{name}.eml"
            # filename.write_text(archive.format_message(message))


dict={
  "From":From_list,
  "To":To_list
}

eml_out = Path(Path.cwd() / pst_file.split(" ")[0])

if not eml_out.exists():
  eml_out.mkdir()



df=pd.DataFrame(dict)
df.to_csv(eml_out/"emls.csv")
print("Done!")


