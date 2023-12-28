#!/usr/bin/python3
import os
import argparse
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("-y",help="Postfix year to album",type=int)
parser.add_argument("-u",help="Upload without album", action="store_true")
parser.add_argument("-a",help="Upload folder to album with same name", type=str)
parser.add_argument("-d",help="Dry run, print rclone command only", action="store_true")
args = parser.parse_args()
rclone_opts = "-P"

def run_rclone(rclone_cmd):
  print(rclone_cmd)
  if args.d:
      return
  process = subprocess.Popen(rclone_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  while True:
    output = process.stdout.readline()
    if process.poll() is not None:
        break
    if output:
         print(output.strip())
  rc = process.poll()
  return rc

if args.u:
    print("Upload only")
    rclone_cmd = f'rclone copy {rclone_opts}  . pto-google-photos:upload'
    run_rclone(rclone_cmd)
    exit()

# if args.u:
#     print(args.a)
#     items = os.listdir(args.a)
#     for item in items:
#         if os.path.isdir(item):

#             rclone_cmd = f'rclone copy {rclone_opts}  "{item}" pto-google-photos:album/"{item.name}"'
#             if args.y:
#                 if str(args.y) not in item:
#                     rclone_cmd = f'rclone copy {rclone_opts} "{item}" pto-google-photos:album/"{item} {args.y}"'
#             run_rclone(rclone_cmd)
#         else:
#             print(f"{item} is a file!")

if args.a:
    base_dir = Path(args.a)

    print(f"Uploading folder {base_dir} into album")
    for item in base_dir.glob("*"):
        print(f"==> {item}")
        if item.is_dir():
            if args.a == ".":
                rclone_cmd = f'rclone copy {rclone_opts}  "./{item}" "pto-google-photos:album/{item.name}"'
            else:
                rclone_cmd = f'rclone copy {rclone_opts}  "./{item}" "pto-google-photos:album/{base_dir.name}/{item.name}"'
            run_rclone(rclone_cmd)        


    
    # for item in items:
    #     if os.path.isdir(item):
    #         rclone_cmd = f'rclone copy {rclone_opts}  "{item}" pto-google-photos:album/"{item}"'
    #         if args.y:
    #             if str(args.y) not in item:
    #                 rclone_cmd = f'rclone copy {rclone_opts} "{item}" pto-google-photos:album/"{item} {args.y}"'
    #         print("x")
    #         run_rclone(rclone_cmd)
    #     else:
    #         print(f"{item} is a file!")
