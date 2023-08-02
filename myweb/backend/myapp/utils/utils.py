import os

class Utils:
    
    @staticmethod
    def making_product_register_images_url(data):

        image_keys = []
        for d in data.keys():
            if 'image' in d:
                image_keys.append(d)
            else:
                continue

        image_values = [] # 이건 실제로 이미지 파일이 저장된거임
        for k in image_keys:
           image_value = data.get(k)
           image_values.append(image_value) 

        image_dic = {key: value for key, value in zip(image_keys, image_values)} 

        name = data.get('productName')

        for k,v in image_dic.items():
            filename = name + '_' + k
            _, ext = os.path.splitext(v.name)  # 파일의 확장자를 가져옵니다.
            new_path = os.path.join(f'/media/{filename}{ext}')  # 확장자를 포함한 파일 이름을 사용하여 경로를 생성합니다.
            print(new_path)  # 생성된 경로를 출력합니다.