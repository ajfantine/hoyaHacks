import sys,os,nltk
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:\\Users\\admin\\desktop\\Computer Science\\HoyaHacks\\feelin_hungry.json"

from google.cloud import automl_v1beta1
from google.cloud.automl_v1beta1.proto import service_pb2


def get_prediction(content, project_id, model_id):

    prediction_client = automl_v1beta1.PredictionServiceClient()

    name = 'projects/{}/locations/us-central1/models/{}'.format(project_id, model_id)
    payload = {'text_snippet': {'content': content, 'mime_type': 'text/plain' }}
    params = {}
    request = prediction_client.predict(name, payload, params)

    str_request = str(request)
    old_list = str_request.split("\n")
    bad_chars = ['','{', '}', ' ']
    list_request = []
    for item in old_list:
      #print(item)
      item = item.split(" ")

      item = [element for element in item if element not in bad_chars]
      #list_request.append(item)
      #item = ' '.join([token for token in item])
      #print(item)
      if(item != ""):
        for part in item:
            list_request.append(part)

    pos_ind = list_request.index('"positive"')
    neg_ind = list_request.index('"negative"')
    if(pos_ind < neg_ind):
      ret_str = "positive"
    else:
      ret_str = "negative"

    #score = text.find('score')
    # str_request.split("")'''
    print("your mood is: "+ret_str)
    return request  # waits till request is returned

if __name__ == '__main__':

    #content = sys.argv[1]
    #project_id = sys.argv[2]
    # model_id = sys.argv[3]

    content = input("Enter a mood: ")
    project_id = "feelin-hungry"
    model_id = "TCN3473486968706001851"

    get_prediction(content, project_id,  model_id)
