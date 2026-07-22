from PIL import Image, ImageDraw

# Create a white background image
img = Image.new('RGB', (600, 300), color=(255, 255, 255))
d = ImageDraw.Draw(img)

# Add Lab Report Text designed to match your regex parser
text = """
CITY PATHOLOGY LABS
====================================
Hemoglobin    11.2   g/dL    13.0 - 17.0
Glucose       185.0  mg/dL   70.0 - 100.0
HbA1c         8.1    %       4.0 - 5.6
====================================
"""

d.text((40, 40), text, fill=(0, 0, 0))
img.save('lab_report_test.png')
print("Sample OCR file 'lab_report_test.png' created!")