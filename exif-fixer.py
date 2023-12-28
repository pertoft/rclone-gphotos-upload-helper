#!/usr/bin/python3
import os
import re
from datetime import datetime
from PIL import Image, ExifTags
from PIL.ExifTags import TAGS
import piexif


def get_exif_DateTimeOriginal(image_path):
    image = Image.open(image_path)
    exif_data = image._getexif()
    if exif_data is not None:
        for tag, value in exif_data.items():
            tag_name = TAGS.get(tag, tag)
            #print(f"{tag_name}: {value}")
            if tag_name == "DateTimeOriginal":
                return value
            if tag_name == "DateTime":
                return value



def update_exif_date(image_path, date_taken):
    # load the metadata from the original file
    exif_dict = piexif.load(image_path)

    # change various dates
    exif_dict['0th'][piexif.ImageIFD.DateTime] = bytes(date_taken.strftime("%Y:%m:%d %H:%M:%S"), 'utf-8')
    exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = bytes(date_taken.strftime("%Y:%m:%d %H:%M:%S"), 'utf-8')
    exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = bytes(date_taken.strftime("%Y:%m:%d %H:%M:%S"), 'utf-8')

    # dump the changes
    exif_bytes = piexif.dump(exif_dict)

    # write the changes the the JPEG file
    piexif.insert(exif_bytes, image_path)
    print(f"Updated image {image_path}")


def process_photos(root_folder):
    for folder_path, _, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                #print(f" ==== {filename} === ")
                image_path = os.path.join(folder_path, filename)

                # Check if the image has EXIF data
                try:
                    old_date = get_exif_DateTimeOriginal(image_path)
                    if old_date !=  None:
                        continue

                except (AttributeError, KeyError, IndexError, IOError):
                    print(f"No EXIF data found for {filename}")

                pattern = re.compile(r'(\d{8})_(\d{9})_iOS.*')   
                match = pattern.match(filename)

                if match:
                    date = match.group(1)
                    timestamp = match.group(2)
                else:
                    print(f"Could not parse filename: {filename}")
                    next
                
                # Convert to datetime object in the format YYYYMMDD_HHMMSSmmm
                date_taken = datetime.strptime(date + timestamp, "%Y%m%d%H%M%S%f")

                # Update EXIF data with the parsed date
                print(f"Updaing image {image_path} with date {date_taken}")
                try:
                    update_exif_date(image_path, date_taken)
                except Exception as ex:
                    print(ex)


if __name__ == "__main__":
    root_folder = "."
    process_photos(root_folder)