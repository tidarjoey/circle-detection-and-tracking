



import numpy as np
import cv2
import cv2.cv as cv
import picamera
import picamera.array
import serial
#pengujian
import time

#capture frame dari pi cam
#kamera = PiCamera()
#cap = cv2.VideoCapture(0)
#set ukuran cap/frame(x,y)
#ukuranframe = cap.set(3,320)
#ukuranframe = cap.set(4,240)
#time.sleep(0.1)

#ser = serial.Serial('/dev/ttyACM0',9600)

with picamera.PiCamera() as kamera:
    with picamera.array.PiRGBArray(kamera) as stream:
        kamera.resolution = (320,240)

        #set i jumlah frame untuk pengujian
        i = 1

        #loop frame read dan operasi pada input dari pi cam
        while(i<181):

            #capture frame dengan ret attribut ukuranframe
            #ukuranframe,frameasli = cap.read()

            kamera.capture(stream,'bgr',use_video_port=True)
            frameasli = stream.array 
    
            #convert frames ke color space grayscale (8 bit single channel)
            abu = cv2.cvtColor(frameasli,cv2.COLOR_BGR2GRAY)
            #implementasi median filter untuk mengurangi noise
            median = cv2.medianBlur(abu,9)
    
            #tampilkan frame abu, pengujian & analisis
            #cv2.imshow('GREYSCALE',abu)
            #if cv2.waitKey(1) & 0xFF == ord('q'):
                #break

            #tampilkan frameasli, pengujian & analisis
            #cv2.imshow('RGB',frameasli)
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break

            #mulai stopwatch untuk pengukuran performasi
            mulai = time.time()

            #implementasi Hough circle transform, dengan parameter dp=2 accumulator threshold 200
            lingkaran = cv2.HoughCircles(median,cv.CV_HOUGH_GRADIENT,3,320,param1=250,param2=100,minRadius=10,maxRadius=120)

            #fungsi untuk terus menjalankan operasi saat tidak ada objek yang terdeteksi
            if lingkaran is None:
                hasil = median
        
                #tampilkan hasil operasi, pengujian & analisis
                cv2.imshow('hasil',hasil)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
                print "tidak ada objek yang terdeteksi"


                #melihat waktu eksekusi untuk satu frame
                #print (time.time()-mulai)
        
                #menyimpan frame untuk data pengujian & analisis dalam JPEG
                #namafile = "framehasil%d.jpg"%i
                #cv2.imwrite(namafile,hasil)

                i = i + 1

                stream.seek(0)
                stream.truncate()
                
                continue
    
            else:
                #hasil Hough circle detection
                hasil = cv2.cvtColor(median,cv2.COLOR_GRAY2BGR)
                #print lingkaran
                #plot hasil deteksi objek, pengujian
                for j in lingkaran[0,:]:
                    #gambar outline objek, warna 0-255-0 (hijau)
                    cv2.circle(hasil,(j[0],j[1]),j[2],(0,255,0),2)
                    #pin titik tengah objek, warna 0-0-255 (merah)
                    cv2.circle(hasil,(j[0],j[1]),2,(0,0,255),3)
                x = j[0]
                x1 = round(x)
                y = j[1]
                y1 = round (y)
                print "koordinat objek X=%s,Y=%s" %(x1,y1)
                #ser.write("%s,%s" %(x1,y1))
                #ser.write(x)
                #ser.write(y)
                
            #tampilkan hasil operasi, pengujian & analisis
            cv2.imshow('hasil',hasil)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


            #melihat waktu eksekusi untuk satu frame
            #print (time.time() - mulai)

            #namafile = "framehasil%d.jpg"%i
            #cv2.imwrite(namafile,hasil)

            i = i + 1

            stream.seek(0)
            stream.truncate()
            
        #Release pi cam capture setelah loop "selesai" 
        cv2.destroyAllWindows()
