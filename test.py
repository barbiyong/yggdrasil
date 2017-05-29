import pyimgur

CLIENT_ID = "3c233163a097e9e"
PATH = "temp.png"

im = pyimgur.Imgur(CLIENT_ID)
uploaded_image = im.upload_image(PATH, title="Chart with PyImgur")
print(uploaded_image.link)
print(uploaded_image.title)
print(uploaded_image.link)
print(uploaded_image.size)
print(uploaded_image.type)