# AI Content Creator Agent Project

## Pariyojana ka Vivaran (Project Description)

Yeh ek AI-powered software agent hai jiska mukhya uddeshya content creators ko zero-investment par content creation aur marketing ki poori prakriya ko automate karne mein madad karna hai. Yeh software local drives par chalega aur ek modular "AI Team" architecture par based hai, jismein ek Manager aur paanch specialized AI Team Members honge.

## Mukhya Uddeshya (Core Objective)

* Clipster jaise platforms se campaign requirements ko samjhe.
* Internet se engaging aur viral videos dhundhe aur download kare.
* Videos mein se best moments ko pehchan kar short-form clips (15-60 sec) mein badle.
* Clips ko automatic captions, effects, aur transitions ke saath professional tarike se edit kare.
* Final videos ke liye viral titles, descriptions, aur hashtags banaye.
* Videos ko social media platforms (YouTube, Instagram) par publish kare.

## Kaise Shuru Karein (Getting Started)

Yeh sections aapko project set up karne aur run karne mein madad karega.

### Purvavashyaktaen (Prerequisites)

* Python 3.8+
* pip (Python package installer)

### Installation

1.  **Repository Clone Karein:**
    ```bash
    git clone [https://github.com/Friday-atlast/ai_agent_project.git](https://github.com/Friday-atlast/ai_agent_project.git)
    cd ai_agent_project
    ```

2.  **Virtual Environment Banayein aur Activate Karein:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/macOS
    # Ya
    # venv\Scripts\activate  # Windows
    ```

3.  **Dependencies Install Karein:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuration File Set Up Karein:**
    `config.toml` file ko open karein aur zaroori settings ko apni suvidha ke anusaar (as per your convenience) configure karein. `backend/data` folder ke paths ko check karein.

5.  **Environment Variables Set Up Karein:**
    Project root directory mein ek `.env` file banayein (agar maujood na ho) aur usme sensitive environment variables add karein. Abhi ke liye, yeh file khali rahegi ya sirf basic logging level configure karegi:
    ```
    LOG_LEVEL=INFO
    LOG_FILE=logs/app.log
    ```

### Chalana (Running the Application)

Backend server ko shuru karne ke liye:

```bash
python main.py