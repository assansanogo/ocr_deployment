sudo yum install -y zlib
sudo yum install -y zlib-devel
sudo yum install -y libjpeg
sudo yum install -y libjpeg-devel
sudo yum install -y libwebp
sudo yum install -y libwebp-devel
sudo yum install -y libtiff
sudo yum install -y libtiff-devel
sudo yum install -y libpng
sudo yum install -y libpng-devel

cd /usr/local/lib
sudo cp /usr/lib64/libjpeg.so.62 .
sudo cp /usr/lib64/libwebp.so.4 .
sudo cp /usr/lib64/libtiff.so.5 .
sudo cp /usr/lib64/libpng15.so.15 .

cd /home/azureuser
git clone https://github.com/DanBloomberg/leptonica.git --depth 1
cd /home/azureuser/leptonica
./autogen.sh
./configure --prefix=/usr/local --disable-shared --enable-static --with-zlib --with-jpeg --with-libwebp  --with-libtiff --with-libpng
make
sudo make install
sudo ldconfig

cd /home/azureuser
wget https://github.com/tesseract-ocr/tesseract/archive/4.0.0.tar.gz -O tesseract-4.0.0.tar.gz
tar zxvf tesseract-4.0.0.tar.gz
cd tesseract-4.0.0
export PKG_CONFIG_PATH=/usr/local/lib/pkgconfig
./autogen.sh
./configure --prefix=/usr/local --disable-shared --enable-static --with-extra-libraries=/usr/local/lib/ --with-extra-includes=/usr/local/lib/
make
sudo make install
sudo ldconfig