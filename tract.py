import boto3
import os

textract_client = boto3.client('textract', region_name='ap-southeast-1')


def extract_text_from_image(image_bytes):
    # 初始化 Textract 客户端

    # 调用 DetectDocumentText 方法提取文本
    response = textract_client.detect_document_text(
        Document={'Bytes': image_bytes})

    # 处理响应结果并提取文本
    extracted_text = list()
    for item in response['Blocks']:
        if item['BlockType'] == 'LINE':
            extracted_text.append(str(item['Text']))

    return extracted_text


if __name__ == "__main__":
    image_path = "./assets/data1.jpeg"  # 替换为您的图像文件路径
    with open(image_path, 'rb') as f:
        data = f.read()
        extracted_text = extract_text_from_image(data)
        print(extracted_text)
