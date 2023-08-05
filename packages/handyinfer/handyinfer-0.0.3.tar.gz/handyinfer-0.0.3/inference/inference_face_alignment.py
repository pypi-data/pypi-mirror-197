import argparse
import cv2
import torch

from handyinfer.face_alignment import init_face_alignment_model, landmark_98_to_68
from handyinfer.visualization import vis_face_alignment


def main(args):
    # initialize model
    align_net = init_face_alignment_model(args.model_name)

    img = cv2.imread(args.img_path)

    with torch.no_grad():
        landmarks = align_net.get_landmarks(img)
        if args.to68:
            landmarks = landmark_98_to_68(landmarks)
        vis_face_alignment(img, [landmarks], args.save_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--img_path', type=str, default='inference/data/test_face_alignment.jpg')
    parser.add_argument('--save_path', type=str, default='result_face_alignment.png')
    parser.add_argument('--model_name', type=str, default='awing_fan')
    parser.add_argument('--half', action='store_true')
    parser.add_argument('--to68', action='store_true')
    args = parser.parse_args()

    main(args)
