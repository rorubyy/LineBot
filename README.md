# LineBot Homework

## Description

### Setup Guide
* **How to run**
    * **Step 1: Install Python Packages**
        * > pip install -r requirements.txt
    * **Step 2: Modifiy ```.env.sample``` file save as ```.env```**
    ```
        LINE_TOKEN = <Line Token>
        LINE_SECRET = <Line Secret Token>
        LINE_UID = <Line UID>
    ```
    * **Step 3: Run ```main.py```**
        * > python3 main.py```

* **Info**
  * Port:8787
* **Run ngrok**
  * > ngrok http 8787

### Command in LineBot
| Command | Description | 
| -------- | -------- | 
|a op b  | op=```+``` ```-``` ```*``` ```/```|
|a op b=|op=```+``` ```-``` ```*``` ```/```|
|any sticker|return random sticker in my_sticker|

### Exception Handler
1. Divide Zero
2. input isn't a number or operator isn't in ```+``` ```-``` ```*``` ```/```
