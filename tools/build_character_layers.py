"""Build deterministic semantic SVG layers from AFRITOON character masters."""
from __future__ import annotations
import argparse, copy
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT = Path(__file__).resolve().parents[1]
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)
LAYERS = ("back_hair","legs","shoes","torso","left_arm","right_arm","neck","head","ears","front_hair","left_eye","right_eye","left_brow","right_brow","nose","mouth")

# Each current master is a compact SVG. These indices refer to its drawing
# elements in source order; shared elements are deliberately duplicated where
# the source has not yet separated the left/right component.
MAP = {
 "tunde":{"back_hair":[],"legs":[0],"shoes":[1,2],"torso":[3,4],"left_arm":[5],"right_arm":[6],"neck":[7],"head":[10],"ears":[8,9],"front_hair":[11],"left_eye":[12,14],"right_eye":[13,15],"left_brow":[16],"right_brow":[17],"nose":[18],"mouth":[19]},
 "seyi":{"back_hair":[],"legs":[0],"shoes":[1,2],"torso":[3],"left_arm":[],"right_arm":[],"neck":[4],"head":[7],"ears":[5,6],"front_hair":[8],"left_eye":[9],"right_eye":[10],"left_brow":[11],"right_brow":[11],"nose":[12],"mouth":[13]},
 "mama":{"back_hair":[],"legs":[0],"shoes":[1,2],"torso":[3],"left_arm":[18],"right_arm":[19],"neck":[4],"head":[7],"ears":[5,6],"front_hair":[8,9],"left_eye":[10],"right_eye":[11],"left_brow":[12],"right_brow":[12],"nose":[13],"mouth":[14]},
}

def children(master):
 root=ET.parse(master).getroot(); groups=[n for n in root if n.tag.rsplit("}",1)[-1]=="g"]
 if not groups: raise ValueError(f"No drawing group found: {master}")
 return root,list(groups[0])

def write_layer(root,nodes,target):
 out=ET.Element(f"{{{NS}}}svg",{"viewBox":root.attrib.get("viewBox","0 0 600 1100")}); group=ET.SubElement(out,f"{{{NS}}}g")
 for node in nodes: group.append(copy.deepcopy(node))
 target.parent.mkdir(parents=True,exist_ok=True); ET.ElementTree(out).write(target,encoding="utf-8",xml_declaration=True)

def build(cid):
 master=ROOT/"assets"/"characters"/cid/"art"/f"{cid}_front.svg"; root,nodes=children(master)
 for layer in LAYERS:
  selected=[nodes[i] for i in MAP[cid][layer] if i<len(nodes)]
  write_layer(root,selected,ROOT/"assets"/"characters"/cid/"layers"/"front"/f"{layer}.svg")
 print(f"built {cid}: {len(LAYERS)}/16 semantic layer files")

def main():
 p=argparse.ArgumentParser(); p.add_argument("--character",choices=("tunde","seyi","mama","all"),default="all"); args=p.parse_args()
 for cid in (("tunde","seyi","mama") if args.character=="all" else (args.character,)): build(cid)
if __name__=="__main__": main()
