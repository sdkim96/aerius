# # 이미지 로드 및 리사이징: 우선, 모든 이미지는 같은 크기로 리사이징되어야 합니다. 
# Mask R-CNN은 일반적으로 고정된 크기의 입력을 받아들이기 때문입니다. 
# 이 작업은 이미지의 가로 및 세로 크기를 조정하고, 
# 필요한 경우 패딩을 추가하는 것을 포함할 수 있습니다.

# Ground Truth 데이터 생성: Mask R-CNN은 각 이미지에 대해 bounding box 좌표와, 
# 해당 bounding box 내의 모든 픽셀에 대한 mask를 필요로 합니다. 
# 이러한 ground truth 데이터는 훈련 데이터 세트에 대해 제공되어야 합니다. 
# 이는 보통 이미지 내의 각 객체에 대해 수동으로 레이블링함으로써 이루어집니다.

# Data Augmentation: 과적합을 방지하고 모델의 일반화 능력을 향상시키기 위해 
# 데이터 증강 기법을 사용할 수 있습니다. 이는 이미지를 회전시키거나, 뒤집거나, 
# 왜곡시키는 등의 변환을 포함할 수 있습니다.

# 정규화: 이미지의 픽셀 값을 일정 범위(예: 01 또는 -11)로 스케일링하는 것이 
# 일반적입니다. 이 작업은 모델의 수렴을 돕고, 학습 과정을 안정화하는 데 도움이 됩니다.

# 데이터셋 분리: 마지막으로, 데이터셋을 훈련 세트, 검증 세트, 
# 테스트 세트로 분리하는 것이 일반적입니다. 이는 모델의 성능을 적절하게 평가하고, 
# 과적합을 감지하는 데 도움이 됩니다.

import os
from PIL import Image

class Preprocess:
    def __init__(self):
        pass


    def _get_image_filenames(self, path):
        image_extensions = ['jpg', 'jpeg', 'png', 'gif']
        image_filenames = []

        all_files = os.listdir(path)

        for file in all_files:
            _, ext = os.path.splitext(file)
            ext = ext[1:].lower()

            if ext in image_extensions:
                image_filenames.append(file)

        return image_filenames


    def _is_directory(self, path):
        return os.path.isdir(path)


    def resizing(self, path, new_size=(128, 128), save_path=None):
        if self._is_directory(path):
            image_filenames = [os.path.join(path, name) for name in self._get_image_filenames(path)]
        else:
            image_filenames = [path]  # If it's a single image file, create a list with the file path

        for filename in image_filenames:
            # Open the image file
            image = Image.open(filename)
            # Resize the image
            resized_image = image.resize(new_size)

            # Determine where to save the resized image
            if save_path:
                # Save to the specified location, keeping the original image name
                base_name = os.path.basename(filename)
                save_filename = os.path.join(save_path, base_name)
            else:
                # Save back to the original location
                save_filename = filename

            # Save the resized image
            resized_image.save(save_filename)



