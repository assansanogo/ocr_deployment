cd /aws
wget https://github.com/second-state/OCR-tesseract-on-Centos7/raw/main/deps.tar.gz
tar -zxvf deps.tar.gz

export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/aws/deps/"

source ~/.bash_profile