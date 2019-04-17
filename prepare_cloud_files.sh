ibmcloud fn action delete map
ibmcloud fn action delete reduce

cp map.py __main__.py
zip -r map.zip __main__.py cos_backend.py

cp reduce.py __main__.py
zip -r reduce.zip __main__.py cos_backend.py

ibmcloud fn action create map --kind python:3.6 map.zip
ibmcloud fn action create reduce --kind python:3.6 reduce.zip

rm *.zip __main__.py