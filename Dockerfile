FROM pasmod/miniconder2

RUN apt-get update && \
	apt-get install -y build-essential libxml2-dev libxslt-dev python-matplotlib libsm6 libxrender1 libfontconfig1 && \
	apt-get clean

# install packages with conda
RUN conda install -y \
  pip \
  numpy \
  pandas \
  scikit-learn \
  nltk \
  h5py \
  matplotlib

RUN python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')" 

WORKDIR /var/www
ADD . .
RUN pip install -r requirements.txt
RUN pip install -e .
RUN py.test --pep8
