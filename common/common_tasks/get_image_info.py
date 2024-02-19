OS = '@@{OS}@@'

if OS=="WIN2022":
    image_info = "WIN2022_CALM - " + '@@{WIN2022_IMAGE_LOCATION}@@' + " - 1.0.1"
elif OS=="WIN2019":
    image_info = "WIN2019_CALM - " + '@@{WIN2019_IMAGE_LOCATION}@@' + " - 1.0.1"
elif OS=="RHEL8":
    image_info = "RHEL8_CALM - " + '@@{RHEL8_IMAGE_LOCATION}@@' + " - 1.0.1"
elif OS=="RHEL9":
    image_info = "RHEL9_CALM - " + '@@{RHEL9_IMAGE_LOCATION}@@' +  " - 1.0.1"

print(image_info)