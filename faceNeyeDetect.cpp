#include <iostream>
#include <opencv2/opencv.hpp>
#include <stdlib.h>
#include <stdio.h>

#ifndef CV_RGB2GRAY
#define CV_RGB2GRAY cv::COLOR_RGB2GRAY
#endif

using namespace std;
using namespace cv;

int main(int argc, char *argv[])
{

	int a = 0;
	//Mat img;
	VideoCapture capture(0);

	if (!capture.isOpened()) {
		std::cerr << "Could not open camera" << std::endl;
		return -1;
	}

	namedWindow("webcam", 1);

	CascadeClassifier eye;
	CascadeClassifier face;
	String face_cascade = "C:/opencv/data/haarcascades/haarcascade_frontalface_alt.xml";
	String eye_cascade = "C:/opencv/data/haarcascades/haarcascade_eye.xml";


	if (!face.load(face_cascade) || !eye.load(eye_cascade)) {
		cout << "Cascade ���� ���� ����" << endl;
		return -1;
	}

	Mat frame;

	while (1) {
		bool frame_valid = true;

		try {
			// get a new frame from webcam
			capture >> frame;
		}

		catch (Exception& e) {
			cerr << "Exception occurred. Ignoring frame... " << e.err << std::endl;
			frame_valid = false;
		}

		if (frame_valid) {
			try {

				Mat gray;
				cvtColor(frame, gray, CV_RGB2GRAY);

				vector<Rect> face_pos; // �� ��ġ ����
				face.detectMultiScale(gray, face_pos, 1.1, 3, 0 | CASCADE_SCALE_IMAGE, Size(10, 10)); // �� ����

				// �� ���� ǥ��
				for (int i = 0; i < (int)face_pos.size(); i++) {
					rectangle(frame, face_pos[i], Scalar(0, 255, 0), 2);
				}

				for (int i = 0; i < (int)face_pos.size(); i++) {
					vector<Rect> eye_pos; // �� ��ġ ����

					Mat roi = gray(face_pos[i]); // ���ɿ��� ����
					eye.detectMultiScale(roi, eye_pos, 1.1, 3, 0 | CASCADE_SCALE_IMAGE, Size(10, 10)); // �� ����

					// �� ���� ǥ��
					for (int j = 0; j < (int)eye_pos.size(); j++) {
						Point center(face_pos[i].x + eye_pos[j].x + (eye_pos[j].width / 2),
							face_pos[i].y + eye_pos[j].y + (eye_pos[j].height / 2));

						int radius = cvRound((eye_pos[j].width + eye_pos[j].height) * 0.2);
						circle(frame, center, radius, Scalar(0, 0, 255), 2);
					}
				}
			}

			catch (Exception& e) {
				cerr << "Exception occurred. Ignoring frame... " << e.err << std::endl;
			}

		}
		namedWindow("����");
		imshow("����", frame);
		if (waitKey(30) >= 0) break;

	}

	return 0;

}