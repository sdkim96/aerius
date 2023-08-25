FROM tensorflow/tensorflow:2.13.0

# 필요한 패키지 설치
RUN apt-get update && apt-get install -y python3
RUN pip install typing-extensions==3.6.6

# 작업 디렉토리 설정
WORKDIR ./app

COPY views.py /app

# 필요한 라이브러리 설치
RUN pip install tensorflow

# 컨테이너 실행 시 실행할 명령어 설정
CMD ["python3", "/views.py"]
