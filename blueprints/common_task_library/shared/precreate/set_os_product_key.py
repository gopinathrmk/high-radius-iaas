OS='@@{OS}@@'

if OS=="WIN2019":
  os_product_key = ""
elif OS=="WIN2016":
  os_product_key = ""
else:
  print "OS Selected is not supported by this Calm blueprint."
  exit(1)

print "os_product_key=",os_product_key