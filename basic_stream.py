from flask import Flask, render_template, Response
import cv2
import mediapipe as mp

app = Flask(__name__)

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
drawing_styles = mp.solutions.drawing_styles

camera = cv2.VideoCapture("http://10.0.0.178:5000/video_feed")

def gen_frames():  # generate frame by frame from camera
    while True:

        with mp_hands.Hands(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
            
            while camera.isOpened():
                success, image = camera.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    # If loading a video, use 'break' instead of 'continue'.
                    continue

                image = cv2.resize(image, ((1152,864)))
                # Flip the image horizontally for a later selfie-view display, and convert
                # the BGR image to RGB.
                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                image = cv2.flip(image, 1)
                # To improve performance, optionally mark the image as not writeable to
                # pass by reference.
                image.flags.writeable = False
                results = hands.process(image)

                # Draw the hand annotations on the image.
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(
                            image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                            drawing_styles.get_default_hand_landmark_style(),
                            drawing_styles.get_default_hand_connection_style())

                #image = cv2.resize(image, ((240,180)), interpolation=cv2.INTER_NEAREST)    #1.8.2021
                image = cv2.resize(image, ((480,360)), interpolation=cv2.INTER_NEAREST)    #1.8.2021

                ret, buffer = cv2.imencode('.jpg', image)
                frame = buffer.tobytes()

                #cv2.imshow("Image", img)

                yield (b'--frame\r\n'
                    b'Content-Type:image/jpeg\r\n'
                    b'Content-Length: ' + f"{len(frame)}".encode() + b'\r\n'
                    b'\r\n' + frame + b'\r\n')


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
            <img id="stream" heigth="100%" width="100%" src="http://10.0.0.115:5000/video_feed" onerror="javascript: alert('failure')"/>
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
    app.run(debug=True,host="0.0.0.0")
