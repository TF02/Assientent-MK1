import pathlib
import cv2
import pickle


def recognize_face():
    cascade_path = pathlib.Path(cv2.__file__).parent.absolute()/ "data/haarcascade_frontalface_default.xml"
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read("trainer.yml")
    clf = cv2.CascadeClassifier(str(cascade_path))

    labels = {}
    with open("labels.pickle", "rb") as f:
        og_labels = pickle.load(f)
        labels = {v:k for k,v in og_labels.items()}

    camera = cv2.VideoCapture(0)

    consensice_count = 0
    last_person_id = None
    while True:
        _, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = clf.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30,30),
            flags=cv2.CASCADE_SCALE_IMAGE
        

        )
        
        
        for (x, y, width, height) in faces:
            roi_gray = gray[y:y+height, x:x+width]
            id_, conf= recognizer.predict(roi_gray)   
           
            if conf >=45 and conf <=85:
                #print(id_)
                #print(labels[id_])
                if id_ == last_person_id:
                    consecutive_count += 1
                
                    if consecutive_count >= 20:
                        print(name + " recognized 20 times in a row")
                        consecutive_count = 0
                        img_item = f"{name}_recognized.png"
                        cv2.imwrite(img_item, frame)
                        return name
                        
                else:
                    last_person_id = id_
                    consecutive_count = 1


                
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = labels[id_]
                color = (255,255,255)
                stroke = 2
                cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)

            # img_item = "my-img4.png"
            # cv2.imwrite(img_item,roi_gray)
            cv2.rectangle(frame,(x, y), (x+width, y+height), (255, 255, 0), 2)
        
        cv2.imshow("Faces", frame)
        if cv2.waitKey(1) == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()
    return name 



 