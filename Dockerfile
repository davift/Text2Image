FROM huggingface/transformers-pytorch-gpu:latest
RUN python3 -m pip install --upgrade pip
ENV CMAKE_ARGS="-DSD_CUDA=ON"
RUN pip install stable-diffusion-cpp-python
RUN pip install python-dotenv diffusers accelerate transformers sentencepiece peft spaces cohere compel
RUN apt update && apt install nano curl wget iputils-ping -y
WORKDIR /app
CMD ["/bin/bash"]

