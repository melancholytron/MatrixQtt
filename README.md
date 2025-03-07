
# MatrixQTT Screensaver

![Whoa...](https://github.com/melancholytron/MatrixQtt/blob/main/matrix.jpeg)

A real-time MQTT message visualizer inspired by the Matrix digital rain effect. Displays incoming MQTT messages with customizable colors, sound effects, and dynamic visual effects.

"This is fucking brilliant. Nobody needs this, nobody has a real use for this and this definitely does not attract girls. Still, I'll try this and probably love it. -Tim Goeree"

---

## Features

- Real-time MQTT message display  
- Customizable color schemes  
- Keyword highlighting with sound effects  
- Adjustable scroll speed  
- JSON payload parsing  
- Dynamic message fading  
- Fullscreen toggle (Alt+Enter)  
- Cross-platform support
- Minutes of fun 

---

## Requirements

- Python 3.8+  
- Paho-MQTT
- Pygame

---

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/melancholytron/MatrixQtt.git
    ```

2. Edit the `config.json` file as described in the configuration section below

3. Install dependencies using either `pip` or `uv` (recommended):

    ```sh
    uv run MatrixQtt.py
    ```

    or:

    ```sh
    pip install -r requirements.txt
    python MatrixQtt.py
    ```

---

## Configuration

Edit `config.json` to customize the behavior. Here's an example configuration:
```
{  
  "mqtt": {  
    "broker": "10.0.0.18",  
    "port": 1883,  
    "username": "homeassistant",  
    "password": "rossDontGiveNoForks",  
    "topics": ["docker/#", "homeassistant/#"],  
    "json_fields": {  
      "docker/jellyfin/status": "health"  
    }  
  },  
  "screensaver": {  
    "width": 1920,  
    "height": 1080,  
    "font_name": "monospace",  
    "font_size": 25,  
    "topic_color": [0, 255, 0],  
    "payload_color": [200, 200, 200],  
    "keywords": {  
      "healthy": [0, 255, 0],  
      "error": [255, 0, 0]  
    },  
    "background_color": [0, 0, 0],  
    "payload_char_limit": 50,  
    "min_alpha": 50,  
    "sound_effects": {  
      "detected": "/path/to/detected.wav",  
      "motion": "/path/to/motion.mp3",  
      "unhealthy": "/path/to/alert.wav"  
    },  
    "fullscreen": false  
  }  
}  
```
---

## Usage

Run the screensaver:  
`python MatrixQtt.py`  

---

### Controls

| Key          | Function                          |  
|--------------|-----------------------------------|  
| `+` / `=`    | Increase scroll speed             |  
| `-`          | Decrease scroll speed             |  
| `C`          | Clear screen                      |  
| `ESC`        | Quit                              |  
| `Alt+Enter`  | Toggle fullscreen mode            |  

---

## Configuration Options

### MQTT Settings

- `broker`: MQTT broker address  
- `port`: Broker port (default: 1883)  
- `topics`: List of topics to subscribe to  
- `json_fields`: Specific JSON fields to extract  

### Display Settings

- `width`/`height`: Screen resolution  
- `font_name`: System font to use  
- `font_size`: Base font size  
- `topic_color`: RGB color for topic text  
- `payload_color`: Default payload text color  
- `keywords`: Color mappings for specific words  
- `background_color`: Background RGB color  
- `payload_char_limit`: Maximum payload length  
- `min_alpha`: Minimum text opacity (0-255)  
- `fullscreen`: Start in fullscreen mode (true/false)  

### Sound Settings

- `sound_effects`: Map keywords to sound file paths (e.g., `"detected": "/path/to/sound.wav"`)  

---

## Notes

- Sound effects are triggered by the first matching keyword in a message.  
- Ensure sound files are in a supported format (e.g., WAV, MP3).  

---

## License

GPL-3.0 license. See `LICENSE` for details.
