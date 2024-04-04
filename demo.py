from typing import Final
import cv2
from cv2.typing import MatLike


SAMPLE_IMAGE_FILE_NAME: Final[str] = "image.png"

def read_image(filename: str) -> MatLike:
    return cv2.imread(filename)

def get_human_count(image: MatLike) -> int:
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    (humans, _) = hog.detectMultiScale(image, winStride=(10, 10), padding=(32, 32), scale=1.1)
    return len(humans)

if __name__ == '__main__':
    image = read_image(SAMPLE_IMAGE_FILE_NAME)
    human_count = get_human_count(image)
    print(f"human_count: {human_count}")
