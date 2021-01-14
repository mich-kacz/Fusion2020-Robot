import cv2
import socket
from flask import Flask, render_template, Response

app=Flask(__name__)

def gen_frames():
	cap=cv2.VideoCapture(0, cv2.CAP_V4L2)
	while True:
		succes, frame=cap.read()
		if not succes:
			break
		else:
			ret, buff= cv2.imencode(".jpg", frame)
			frame=buff.tobytes()
			yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n')
			
@app.route('/')
def index():
	return render_template('index.html')
		
@app.route('/video_feed')
def video_feed():
	return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')




if __name__ == '__main__':
    app.run(host=socket.gethostbyname(socket.gethostname()), use_reloader=False)
    gen_frames()
