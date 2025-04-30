
import easyocr

reader = easyocr.Reader(['en'], gpu=False)

def extract_text_from_image(image_path):
    results = reader.readtext(image_path)
    extracted_text = " ".join([text for (_, text, _) in results])
    return extracted_text
