
def hello_world(request):

    from google.cloud import vision
    from datetime import datetime
    import re
    import itertools
    import write2bq
    #from google.oauth2 import service_account
    import os
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:\gcp_credentials\elaborate-howl-285701-105c2e8355a8.json"
    #SCOPES = ['https://www.googleapis.com/auth/sqlservice.admin']
    #SERVICE_ACCOUNT_FILE = 'C:\gcp_credentials\elaborate-howl-285701-105c2e8355a8.json'
    #credentials = service_account.Credentials.from_service_account_file(
    #    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    table_id='elaborate-howl-285701.context.image_web_entities'#destination table name

    now = str(datetime.now())# time

    print("now="+now)

    client = vision.ImageAnnotatorClient()
    request_json = request.get_json()
    image = vision.Image()
    if request_json:
        source_url = request_json['source_url']
        print("source_url="+source_url)

    source_url=re.match(r'gs://([^/]+)/(.+)', source_url) 
    bucket_name=source_url.group(1) #credential bucket name
    print(bucket_name)
    prefix=source_url.group(2)# credential prefix name
    print(prefix)



    file_name=prefix
    exact_file_name_list = re.split("/", file_name)
    exact_file_name=exact_file_name_list[-1]
    



    uri="gs://"+bucket_name+"/"+file_name
    print("uri="+uri)

    image.source.image_uri = uri

    response = client.web_detection(image=image)
    matching_images_lst=[]
    matching_images=response.web_detection.full_matching_images# url string in it creates problem from json
    for matching_image in matching_images:
        matching_images_lst.append(matching_image.url)
    # list is made for matching images
    page_lst=[]
    for page in response.web_detection.pages_with_matching_images:
        page_lst.append(page.url)
    # list is made for pages
    best_match_lst=[]#list empty which stores best match result
    for best_match in response.web_detection.best_guess_labels:
        best_match_lst.append(best_match.label)

    for (a, b, c) in itertools.zip_longest(matching_images_lst, page_lst, best_match_lst): 
        documentEntities={"time_stamp":now,"file_name":exact_file_name,"matching_images":a,"pages_with_images":b,"best_guess":c,"input_uri":uri}
        write2bq.BQ(documentEntities,table_id)
    
    return "success"
     


     
     
     




     