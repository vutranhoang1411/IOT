import face_recognition
import cv2
import numpy as np
from os import listdir
import simple_lock
import threading
from time import sleep
import base64
def UnlockLock(lock):
    sleep(30)
    lock.Unlock()
class AICam:
    def __init__(self,employee_folder,client):

        self.known_face_encodings=[]
        self.known_face_names=[]
        self.exist=[]
        self.video_capture=cv2.VideoCapture(0)

        img_files=listdir(employee_folder)
        for img_file in img_files:
        #get img name
            name=img_file.split(".")[0]
            self.known_face_names.append(name)

            #get encode
            img=face_recognition.load_image_file("./employee/"+img_file)
            encode=face_recognition.face_encodings(img)[0]
            self.known_face_encodings.append(encode)
            self.exist.append(False)
            
            self.client=client

    def StartRecord(self):
        lock=simple_lock.Lock()
        process_this_frame=True
        while True:
            ret, frame = self.video_capture.read()
            if process_this_frame:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = cv2.cvtColor(small_frame,cv2.COLOR_BGR2RGB)
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"

                    # # If a match was found in known_face_encodings, just use the first one.
                    # if True in matches:
                    #     first_match_index = matches.index(True)
                    #     name = known_face_names[first_match_index]

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]: #detect a employee
                        name = self.known_face_names[best_match_index]
                        if not self.exist[best_match_index]:
                            self.client.publish("iot-hk222.ai",f'{name} go to work')
                            img_bytes=cv2.imencode('.jpg',small_frame)[1].tobytes()
                            data=base64.b64encode(img_bytes)
                            self.client.publish("iot-hk222.image-recognize",data)
                            self.exist[best_match_index]=True

                        if lock.Locked==False:
                            lock.Lock()
                            threading.Thread(target=UnlockLock,args=(lock,)).start()
                            self.client.publish("iot-hk222.pump","1")
                            img_bytes=cv2.imencode('.jpg',small_frame)[1].tobytes()
                            data=base64.b64encode(img_bytes)
                            self.client.publish("iot-hk222.image-recognize",data)
                        
                            
                    face_names.append(name)

            process_this_frame = not process_this_frame
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Display the resulting image
            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.video_capture.release()
        cv2.destroyAllWindows()
