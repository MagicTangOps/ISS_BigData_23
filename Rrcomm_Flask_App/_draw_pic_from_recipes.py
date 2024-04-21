import base64

import requests

def generate_pic_from_text(text):
    url = 'https://api.vyro.ai/v1/imagine/api/generations'

    headers = {
      'Authorization': 'Bearer <your key>'
    }

    # Using None here allows us to treat the parameters as string
    payload = {
        'prompt': (None, text),
        'style_id': (None, '27'),
        'aspect_ratio': (None, '1:1'),
        'high_res_results': (None, '0')
    }

    response = requests.post(url, headers=headers, files=payload)

    if response.status_code == 200: # if request is successful
        image_content = response.content
        base64_image = base64.b64encode(image_content).decode('utf-8')
        return base64_image
    else:
        return response.status_code
