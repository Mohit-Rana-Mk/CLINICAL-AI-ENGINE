from PIL import Image, ImageDraw

# Create a 400x400 image simulating a skin rash/lesion
img = Image.new('RGB', (400, 400), color=(240, 210, 200))
d = ImageDraw.Draw(img)

# Draw a red circular spot to simulate a rash
d.ellipse([140, 140, 260, 260], fill=(190, 50, 50))
d.text((20, 20), "SKIN RASH TEST IMAGE", fill=(0, 0, 0))

# Save with 'skin' in the filename to trigger the Skin Vision route
img.save('skin_rash_test.png')
print("Sample Medical Image 'skin_rash_test.png' created!")