import pandas as pd
import pytesseract
import glob

# Prediction for all images in a specific folder
def ocr_predict():

  # Goes through all images in the folder.
  for image in glob.glob("*.jpg"):

    # Extracts all words in the image and gives their coordinates.
    data = pytesseract.image_to_data(image, lang='eng', config='psm--6')
    print(image)

    # Print the output in a txt file.
    with open(f'{image[:-4]}.txt', 'w') as f:
      print(data, file=f)
  
  # Goes through all txt output files and create a pandas dataframe.
  for text in glob.glob("*.txt"):
    df = pd.read_table(f"{text}") # Read the dataframe.
    df = df.dropna() # Drop empty rows.
    df['text'] = df['text'].astype(str) # Convert the text column into string.
    
    # Merge all words on the same line and its coordinates.
    df1 = df.groupby('top')['text'].apply(' '.join).reset_index()
    df2 = df.groupby('top')['left'].min().reset_index()
    df3 = df.groupby('top')['width'].sum().reset_index()
    df4 = df.groupby('top')['height'].max().reset_index()
    df5 = pd.concat([df1, df2, df3, df4], axis = 1)

    # Rename the columns.
    df5.columns = ['top', 'text', 'top', 'xmin', 'ymin', 'xmax', 'top', 'ymax']

    # xmax = xmin + width and ymax = ymin + height.
    df5['xmax'] = df5['xmin'] +df5['xmax']
    df5['ymax'] = df5['ymin'] +df5['ymax']

    # Drop the duplicate ymin columns obtained by the concatination.
    df5 = df5.drop(['top'], axis = 1)

    # Save results into a csv file.
    df5.to_csv(f'{text[:-4]}.csv', sep=',')