import base64
from io import BytesIO
from PIL import Image
import json

# Assume the base64 string is stored in variable `base64_str`
with open('env/DOOM-style-Game/data.json', 'r') as f:
    # Load the contents of the file as a Python object
    data = json.load(f)




'''load player loc'''
print('Player Locations')
print(data["Player_Loc"])
print('\n\n\n')
'''load enemies'''
print("Enemies")
print(data['Enemies'])
print('\n\n\n')
'''load kills'''
print('Kills')
print(data['Kills'])
print('\n\n\n')


'''load img'''
# Decode the base64 string into bytes
image_data = base64.b64decode(data['Img'])

# Create a BytesIO object from the decoded bytes
bytes_io = BytesIO(image_data)

# Use PIL to open the image from the BytesIO object
image = Image.open(bytes_io)
# Show the image
image.show()