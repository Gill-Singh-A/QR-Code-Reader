#!/usr/bin/env python3

import cv2
from datetime import date
from optparse import OptionParser
from time import strftime, localtime
from colorama import Fore, Back, Style

GREEN = (0, 255, 0)

status_color = {
	'+': Fore.GREEN,
	'-': Fore.RED,
	'*': Fore.YELLOW,
	':': Fore.CYAN,
	' ': Fore.WHITE,
}

def get_time():
	return strftime("%H:%M:%S", localtime())
def display(status, data):
	print(f"{status_color[status]}[{status}] {Fore.BLUE}[{date.today()} {get_time()}] {status_color[status]}{Style.BRIGHT}{data}{Fore.RESET}{Style.RESET_ALL}")

def get_arguments(*args):
	parser = OptionParser()
	for arg in args:
		parser.add_option(arg[0], arg[1], dest=arg[2], help=arg[3])
	return parser.parse_args()[0]

if __name__ == "__main__":
	data = get_arguments(('-s', "--save", "save", "Name of the file to save Data extracted from the QR Code"),
						 ('-i', "--image", "image", "Load Image from the given file"))
	all_data = set()
	if data.image:
		try:
			image = cv2.imread(data.image)
			cv2.imshow("Image", image)
		except:
			display('-', f"Error while reading {Back.MAGENTA}{data.image}{Back.RESET}")
		detector = cv2.QRCodeDetector()
		data_qr, box, qrcode_image = detector.detectAndDecode(image)
		if data_qr:
			all_data.add(data_qr)
			display('+', f"Data extracted from QR Code = {Back.MAGENTA}{data_qr}{Back.RESET}")
			cv2.imshow("QR Code", qrcode_image)
			box = box[0]
			box = box.astype(int)
			dimensions = len(box)
			for i in range(dimensions):
				cv2.line(image, box[i], box[(i+1)%dimensions], GREEN, 2)
			cv2.imshow("Image", image)
			cv2.waitKey()
		else:
			display('*', "No QR Code Detected in this Image")
			exit(0)
	else:
		video_capture = cv2.VideoCapture(0)
		detector = cv2.QRCodeDetector()
		prev_data = ""
		while True:
			ret, frame = video_capture.read()
			if not ret:
				display('-', "Can't get the Frame from the Camera")
				break
			data_qr, box, qrcode_image = detector.detectAndDecode(frame)
			if data_qr:
				all_data.add(data_qr)
				if prev_data != data_qr:
					display('+', f"Data extracted from QR Code = {Back.MAGENTA}{data_qr}{Back.RESET}")
					prev_data = data_qr
				cv2.imshow("QR Code", qrcode_image)
				box = box[0]
				box = box.astype(int)
				dimensions = len(box)
				for i in range(dimensions):
					cv2.line(frame, box[i], box[(i+1)%dimensions], GREEN, 2)
			else:
				try:
					cv2.destroyWindow("QR Code")
				except:
					pass
			cv2.imshow("Camera", frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
		video_capture.release()
		cv2.destroyAllWindows()
	all_data = list(all_data)
	if not data.save:
		data.save = f"{date.today()} {get_time()}"
	if len(all_data) > 0:
		with open(data.save, 'w') as file:
			file.write('\n'.join(all_data))