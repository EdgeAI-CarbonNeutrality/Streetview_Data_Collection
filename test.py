import requests
from PIL import Image
import io
import os

google_api_key = ""
lat = 0.0
lon = 0.0



# def save_images(img_list, file_prefix, file_format="jpg", folder="img"):
#     if not os.path.exists(folder):
#         os.makedirs(folder)
#     for i, img in enumerate(img_list):
#         file_name = os.path.join(folder, f"{file_prefix}_{i+1}.{file_format}")
#         img.save(file_name)
#         print(f"이미지가 성공적으로 저장되었습니다: {file_name}")

def save_images(img_list, lat, lon, file_format="jpg", folder="img"):
    if not os.path.exists(folder):
        os.makedirs(folder)
    for i, img in enumerate(img_list):
        file_prefix = f"({lat},{lon})"
        file_name = os.path.join(folder, f"{file_prefix}_{i+1}.{file_format}")
        img.save(file_name)
        print(f"이미지가 성공적으로 저장되었습니다: {file_name}")


def get_user_input():
    google_api_key = input("Google API 키를 입력하세요: ")
    lat_lon_input = input("위도와 경도를 입력하세요 (예: 37.4502,126.6535): ")
    lat, lon = map(float, lat_lon_input.split(','))  # 콤마로 구분
    # lat = float(input("위도를 입력하세요: "))
    # lon = float(input("경도를 입력하세요: "))
    return google_api_key, lat, lon

def get_streetview_images(google_api_key, lat, lon, heading_list):
    img_list = []
    for heading in heading_list:
        fov = "120"
        pitch = "30"
        radius = "100000"

        url = f"https://maps.googleapis.com/maps/api/streetview?size=1200x300&location={lat},{lon}&fov={fov}&heading={heading}&pitch={pitch}&radius={radius}&key={google_api_key}"
        payload = {}
        headers = {}
        response = requests.request("GET", url, headers=headers, data=payload)
        bytes_data = response.content
        img = Image.open(io.BytesIO(bytes_data))
        img_list.append(img)
    return img_list

def main():
    google_api_key, lat, lon = get_user_input()
    heading_list = list(range(-45, 360-45, 90))
    img_list = get_streetview_images(google_api_key, lat, lon, heading_list)
    save_images(img_list, lat, lon, file_format="jpg", folder="img")
    # save_images(img_list, file_prefix="streetview_image", file_format="jpg", folder="img")

if __name__ == "__main__":
    main()
