#-----------------------------------------------------
# @author: DANDE TEJA          <cs17b010@iittp.ac.in>
# @date: 21/05/2021
#-----------------------------------------------------

import fitz
import io
from PIL import Image
  
file = "/home/iit/Desktop/kowndinya/annotator-web-tool/annotator/PDF_AS_INPUT.pdf"
  
pdf_file = fitz.open(file)
  
for page_index in range(len(pdf_file)):
    
    page = pdf_file[page_index]
    image_list = page.getImageList()
      
    if image_list:
        print(f"[+] Found a total of {len(image_list)} images in page {page_index}")
        for x in image_list:
            print(x)
    else:
        print("[!] No images found on page", page_index)
    for image_index, img in enumerate(page.getImageList(), start=1):
        
        xref = img[0]
          
        base_image = pdf_file.extractImage(xref)
        image_bytes = base_image["image"]
          
        image_ext = base_image["ext"]
        
