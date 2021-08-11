from flask import Flask, render_template, Response
import cv2
import pyautogui
import numpy as np

app = Flask(__name__)

camera = cv2.VideoCapture(0)  # use 0 for web camera

def gen_frames():  # generate frame by frame from camera
    while True:
        suc, img = camera.read()
        if suc:
            # HIGH RES BUT SLOW?
            #img = cv2.resize(img, ((480,320)), interpolation=cv2.INTER_AREA)
            #img = cv2.resize(img, ((480,480)), interpolation=cv2.INTER_AREA)
            #img = cv2.resize(img, ((480,360)), interpolation=cv2.INTER_NEAREST)
            img = cv2.resize(img, ((240,180)), interpolation=cv2.INTER_NEAREST)    #1.8.2021
            img = cv2.rotate(img, cv2.ROTATE_180)
            #img = cv2.resize(img, ((120,90)), interpolation=cv2.INTER_AREA)
            #img = cv2.resize(img, ((60,45)), interpolation=cv2.INTER_NEAREST)

            ret, buffer = cv2.imencode('.jpg', img)

            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type:image/jpeg\r\n'
                   b'Content-Length: ' + f"{len(frame)}".encode() + b'\r\n'
                   b'\r\n' + frame + b'\r\n')
        else:
            print(suc)
            breakpoint()


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video')
def video():
    page = """
    <html>
        <head>
            <title>Video Streaming Demonstration</title>
        </head>
        <body style="background-color:black;">
            <img id="stream" heigth="100%" width="100%" src="http://10.0.0.178:5000/video_feed" onerror="javascript: alert('failure')"/>
        </body>
    
    <script>
        let stateCheck = setInterval(() => {
        if (document.readyState === 'complete') {
            clearInterval(stateCheck);
            // document ready
        }
        console.log(document.readyState);
        }, 100);
    
    </script>
    
    </html>
    """

    return page


if __name__ == '__main__':
    app.run(debug=False,host="0.0.0.0")
