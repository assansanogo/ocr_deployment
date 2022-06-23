import pandas as pd
print("IMPORT BEGINS")
import pytesseract
import glob
#import json
import boto3
from botocore.exceptions import ClientError
import botocore
import os
#import subprocess
#import cv2
from PIL import Image
from zipfile import ZipFile
import sys
sys.path.insert(0, '/tmp/')


print("DONE IMPORTING MODULES")
s3 = boto3.resource('s3')
s3_client = boto3.client('s3')
# Prediction for all images in the current folder
def lambda_handler(event,context):
    print("FUNCTION BEGINS")
    #print(event)
    print("AFTER PRINT EVENT")
    #download the yolo output zipped folder
    #image = event["Records"][0]["s3"]["object"]["key"]
    os.mkdir('/tmp/yolo_output_zip')
    print("1")
    os.mkdir('/tmp/tesseract_output')
    print("2")
    s3_zipped_file_name = event["Records"][0]["s3"]["object"]["key"]
    print(s3_zipped_file_name)
    folder = s3_zipped_file_name.split('/')[1]
    print(folder)
    local_zipped_file_name = '/tmp/'+ s3_zipped_file_name.split('/')[-1]    #images.zip 
    print(local_zipped_file_name)
    download_from_s3(s3_zipped_file_name,local_zipped_file_name)
    list_of_files = unzip(local_zipped_file_name)
    print(list_of_files)
    #image_key = event["Records"][0]["s3"]["object"]["key"].split('/')
    #filename = image_key[-1]
    #local_file = '/tmp/'+filename
    #download_from_s3(image,local_file)
    output_files = []
    print("step 1")
    print(glob.glob("/tmp/*.jpg"))
    print("step 2")
    print(glob.glob("tmp/*.jpg"))
    print("step 3")
    print(os.listdir("/tmp"))
  # Goes through all images in the folder.
    for image in glob.glob("/tmp/yolo_output_zip/*.jpg"):
        try:
            print("toto")
            # Extracts all words in the image and gives their coordinates.            
            data = pytesseract.image_to_data(image, lang='eng', config='psm--6')
            print(image)

            # Print the output in a txt file.
            with open(f'/tmp/yolo_output_zip/{image[:-4]}.txt', 'w') as f:
                print(data, file=f)

        except:
            print("error for image : ", image)
            continue

    
        # Goes through all txt output files and create a pandas dataframe.
    for text in glob.glob("/tmp/yolo_output_zip/*.txt"):

        try:
            print("toto 2")
            df = pd.read_table(f"{text}") # Read the dataframe.
            df = df.dropna() # Drop empty rows.
            df['text'] = df['text'].astype(str) # Convert the text column into string.
            
            # Merge all words on the same line and its coordinates.

            # Group all the words which are on the same line (same coordinate 'top')
            df1 = df.groupby('top')['text'].apply(' '.join).reset_index()

            # Get the left value of the 1st word of the line.
            df2 = df.groupby('top')['left'].min().reset_index()

            # Get the length of all words on one line.
            df3 = df.groupby('top')['width'].sum().reset_index()

            # Get the height of the highest word on the line.
            df4 = df.groupby('top')['height'].max().reset_index()

            # Concatinate in order to obtain the text and its coordinates.
            df5 = pd.concat([df1['text'], df2['left'], df3, df4['height']], axis = 1)

            # Get the xmax and ymax coordinates.
            df5['xmax'] = df5['left'] +df5['width']        
            df5['ymax'] = df5['top'] +df5['height']

            #Drop width and height which we do not need.
            df5 = df5.drop(['width', 'height'], axis = 1)

            #Rename the columns.
            df5.columns = ['text', 'xmin', 'ymin', 'xmax', 'ymax']

            # Save results into a csv file.
            df5.to_csv(f'/tmp/tesseract_output/{text[:-4]}.csv', sep=',') # saved with index
            
            output_files.append(f'/tmp/tesseract_output/{text[:-4]}.csv')
            
            #upload_file(df5.to_csv(f'{text[:-4]}.csv', sep=','), '/tmp/tesseract_output')

        except:
            print("error for textfile : ", text)
            continue
    print(output_files)
    zip_files(output_files)
    upload_file('/tmp/tesseract_csv.zip','processing/'+folder+'/tesseract_output/tesseract_csv.zip')
    return "SUCCESS"        
    
        
      
      

def download_from_s3(file,object_name):
    try:
        s3.Bucket('statementsoutput').download_file(file,object_name)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise


def zip_files(files):
    # writing files to a zipfile
    with ZipFile('/tmp/tesseract_csv.zip','w') as zip:
        # writing each file one by one
        for file in files:
            zip.write(file)


#Function to unzip Files
def unzip(zipped_file_name):
    directory = os.getcwd()
    os.chdir('/tmp/yolo_output_zip')
    # opening the zip file in READ mode
    with ZipFile(zipped_file_name, 'r') as zip:
        # printing all the contents of the zip file
        zip.printdir()
        list_of_files = zip.namelist()
        # extracting all the files
        print('Extracting all the files now...')
        zip.extractall()
        print('Unzipping Done!')
        os.chdir(directory)
        return list_of_files


#Function to upload files to s3
def upload_file(file_name, object_name=None):
    """Upload a file to an S3 bucket
    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """
    # Upload the file
    try:
        response = s3_client.upload_file(file_name, 'statementsoutput', object_name)
    except ClientError as e:
        print("Unexpected error: %s" % e)
        return False
    return True