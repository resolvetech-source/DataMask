FROM debian:bookworm-slim

# Install required packages
RUN apt-get update && apt-get install -y \
    git build-essential cmake curl python3 python3-pip libssl-dev libcurl4-openssl-dev

# Set working directory
WORKDIR /app

# Clone llama.cpp and build it using cmake
RUN git clone https://github.com/ggerganov/llama.cpp.git && \
    cd llama.cpp && mkdir build && cd build && \
    cmake .. -DLLAMA_SERVER=ON -DLLAMA_CURL=ON && make -j

# Copy model into the container
COPY ./models /models

# Set working directory to server binary
WORKDIR /app/llama.cpp/build/bin

# Expose the server port
EXPOSE 8000

# Run the server with the Qwen model
CMD ["./llama-server", "-m", "/models/qwen2-7b-instruct-q4_k_m.gguf", "--port", "8000", "--host", "0.0.0.0"]
