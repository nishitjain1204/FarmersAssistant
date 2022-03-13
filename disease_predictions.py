import numpy as np
import pandas as pd
from utils.disease import disease_dic
from lime import lime_image
import requests
from skimage.segmentation import mark_boundaries
import matplotlib.pyplot as plt
from matplotlib import cm
import pickle
import io
import torch
from torchvision import transforms
from PIL import Image
from utils.model import ResNet9
import torch.nn.functional as F
import base64


disease_classes = ['Apple___Apple_scab',
                   'Apple___Black_rot',
                   'Apple___Cedar_apple_rust',
                   'Apple___healthy',
                   'Blueberry___healthy',
                   'Cherry_(including_sour)___Powdery_mildew',
                   'Cherry_(including_sour)___healthy',
                   'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
                   'Corn_(maize)___Common_rust_',
                   'Corn_(maize)___Northern_Leaf_Blight',
                   'Corn_(maize)___healthy',
                   'Grape___Black_rot',
                   'Grape___Esca_(Black_Measles)',
                   'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
                   'Grape___healthy',
                   'Orange___Haunglongbing_(Citrus_greening)',
                   'Peach___Bacterial_spot',
                   'Peach___healthy',
                   'Pepper,_bell___Bacterial_spot',
                   'Pepper,_bell___healthy',
                   'Potato___Early_blight',
                   'Potato___Late_blight',
                   'Potato___healthy',
                   'Raspberry___healthy',
                   'Soybean___healthy',
                   'Squash___Powdery_mildew',
                   'Strawberry___Leaf_scorch',
                   'Strawberry___healthy',
                   'Tomato___Bacterial_spot',
                   'Tomato___Early_blight',
                   'Tomato___Late_blight',
                   'Tomato___Leaf_Mold',
                   'Tomato___Septoria_leaf_spot',
                   'Tomato___Spider_mites Two-spotted_spider_mite',
                   'Tomato___Target_Spot',
                   'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
                   'Tomato___Tomato_mosaic_virus',
                   'Tomato___healthy']

disease_model_path = 'models/plant_disease_model.pth'
disease_model = ResNet9(3, len(disease_classes))
disease_model.load_state_dict(torch.load(
    disease_model_path, map_location=torch.device('cpu')))
disease_model.eval()



def np_to_pil(ndarray):
    # im = Image.fromarray(np.uint8(cm.gist_earth(ndarray)*255))
    im=Image.fromarray(((ndarray)*255).astype(np.uint8)).resize((256, 256)).convert('RGB')
    data = BytesIO()
    im.save(data, "JPEG")
    data64 = base64.b64encode(data.getvalue())
    return u'data:img/jpeg;base64,'+data64.decode('utf-8')
#     rawBytes = io.BytesIO()
#     im.save(rawBytes, "JPEG")
#     rawBytes.seek(0)
#     img_base64 = base64.b64encode(rawBytes.read())
#     return im
    


def get_input_transform():
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.ToTensor(),
    ])
    return transform
    

def get_input_tensors(img):
    transf = get_input_transform()
    return transf(img).unsqueeze(0) # unsqueeze converts single image to batch of 1

def get_image(img):
    # with open(os.path.abspath(path), 'rb') as f:
    with IImage.open(io.BytesIO(img)) as img:
        return img.convert('RGB') 


def get_pil_transform(): 
    transf = transforms.Compose([transforms.Resize((256, 256))])   
    return transf

def get_preprocess_transform(): 
    transf = transforms.Compose([transforms.ToTensor()])    
    return transf  

def batch_predict(images):
    #     model.eval()
    batch = torch.stack(tuple(preprocess_transform(i) for i in images), dim=0)
    batch = batch.to(torch.device('cpu'))
    logits = disease_model(batch)
    probs = F.softmax(logits , dim=1)
    return probs.detach().cpu().numpy()  

pill_transf = get_pil_transform()
preprocess_transform = get_preprocess_transform()


        

def predict_image(img, model=disease_model):
    """
    Transforms image to tensor and predicts disease label
    :params: image
    :return: prediction (string)
    """
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.ToTensor(),
    ])
    image = Image.open(io.BytesIO(img))
    img_t = transform(image)
    img_u = torch.unsqueeze(img_t, 0)
    
    

    # Get predictions from model
    yb = model(img_u)
    # Pick index with highest probability
    _, preds = torch.max(yb, dim=1)
    prediction = disease_classes[preds[0].item()]
    # Retrieve the class label
    return prediction



def lime_explaining(img):
    img = Image.open(img)
    test_pred = batch_predict([pill_transf(img)])
    print(test_pred.squeeze().argmax())
    
    explainer = lime_image.LimeImageExplainer()
    explanation = explainer.explain_instance(np.array(pill_transf(img)), 
                                         batch_predict, # classification function
#                                          labels = 
#                                          hide_color=0, 
                                         random_seed = 0,
                                         num_samples=248,
                                        num_features=20
                                        ) # number of images that will be sent to classificati
    
    temp, mask = explanation.get_image_and_mask(explanation.top_labels[0], positive_only=True, num_features=10, hide_rest=False)
    img_boundry1 = mark_boundaries(temp, mask)
    plt.imshow(img_boundry1)
    # plt.savefig('test1.pdf')
    # explanation.top_labels
    # print(img_boundry1)
    print(type(img_boundry1))
    
    
    
    temp, mask = explanation.get_image_and_mask(explanation.top_labels[0], positive_only=False, num_features=10 , hide_rest=False) 
    img_boundry2 = mark_boundaries(temp, mask)
    plt.imshow(img_boundry2)
    # plt.show()
    # plt.savefig('test2.pdf')
    
    return np_to_pil(img_boundry2)
    
