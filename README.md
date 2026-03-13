# text2image

Text-to-Image is a technique of generating images from prompts.

**Disclaimer:** The code in this repository is capable of downloading and running multiple *uncensored models. Use with resposibility and respect!

Content of the readme.
- Container
  - Build, Run, and Manage
- Applications/Scripts
  - Benchmarking
    - Runs the same batch of prompts against all models for comparison.
  - CLI
    - Can generates muiltiple images fromt he same prompt,
    - Easy to integrate with other apps or automations,
    - Has a randomizer function for prompts.
      - **Warning:** Customize the word list to match your objectives. As provided, it contains mature content.
  - Web-UI
    - Browse to interact with the model: submit prompts and view the generated outputs.

## Container

This container image includes all the required libraries and dependencies to run the models and scripts without any hassle.

Build
```bash
docker build -t text2image:v1.0 .
```

Run in Background
```bash
docker run -itd --gpus all -v $(pwd):/app -v $(pwd)/../models:/models -p 7860:7860 --name Text2Image text2image:v1.0
```

Run in Background with Web-UI
```bash
docker run --rm -itd --gpus all -v $(pwd):/app -v $(pwd)/../models:/models -p 7860:7860 -e INDEX=0,3 --name Text2Image text2image:v1.0 /app/app.py
```

Managing
```bash
docker exec -it Text2Image bash
docker logs -f Text2Image
docker stop Text2Image
docker rm Text2Image
```

## Application


### Benchmarking

It will produce a batch of images with the same list (`benchmarking.prompts`) of prompts in all models.

Running
```bash
./benchmark.py
```

### CLI

Usage
```bash
INDEX=M,N python app.py [prompt] [num_images] [num_saved_steps]
```
Note: INDEX refers to the model to be used, see code.

Examples
```bash
./app.py "a woman dressed like a cat"
./app.py "a car with massive tires" 3
INDEX=1,0 ./app.py randomizer 0
```

### Web-UI

```bash
./app.py
```
Navigate to http://IP:7860/

## Avoid Duplication

This will rename all files to its MD5 hash to prevent duplication and tampering.

```bash
for f in *.png; do [ -f "$f" ] && h=$(md5sum "$f" | cut -d ' ' -f1) && mv -n -- "$f" "$h.png"; done
```
