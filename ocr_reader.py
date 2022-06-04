import pandas as pd
import pytesseract
import glob

# Prediction for all images in the current folder
def ocr_predict():

  """  
  This function goes through all jpg files of the current folder and first
  extracts of each image, each word and its coordinates and writes them into a
  text file, then transforms this data into dataframe where all text on one line
  is regrouped, gives its coordinates and saves the dataframe into a csv file.
  """

  # Goes through all images in the folder.
  for image in glob.glob("*.jpg"):

    try:

      # Extracts all words in the image and gives their coordinates.
      data = pytesseract.image_to_data(image, lang='eng', config='psm--6')
      print(image)

      # Print the output in a txt file.
      with open(f'{image[:-4]}.txt', 'w') as f:
        print(data, file=f)

    except:
      print("error for image : ", image)
      continue

    
      # Goes through all txt output files and create a pandas dataframe.
  for text in glob.glob("*.txt"):

    try:

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
      df5.to_csv(f'{text[:-4]}.csv', sep=',') # saved with index

    except:
      print("error for textfile : ", text)
      continue