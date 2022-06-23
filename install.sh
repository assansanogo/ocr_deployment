mkdir aws
cd /aws
wget https://github.com/second-state/OCR-tesseract-on-Centos7/raw/main/deps.tar.gz
tar -zxvf deps.tar.gz .

cp -R /aws/deps/* /aws