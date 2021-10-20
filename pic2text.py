import filter_scheme as fs
import io, requests, cv2, numpy as np
from quote import quote 

def pic2text(url,filter=False):
    img_stream = io.BytesIO(requests.get(url).content)
    img = cv2.imdecode(np.frombuffer(img_stream.read(), np.uint8), 1)
    if filter==True:
        img=fs.crop(img)
        img=fs.gray(img)
        img=fs.filter_by_mode(img)
    message=fs.translate_image(img)
    return message 

def randomQuote(search):
    result=quote(search,limit=10)
    x=np.random.randint(0,len(result))
    out=result[x]
    print_this=out["quote"] + "\n" + "--"+out["author"]
    if out["book"] !="":
        print_this+=", "+out["book"]
    return print_this








