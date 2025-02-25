import json
import paho.mqtt.client as mqtt
import pygame
import random
import time
import threading
import traceback

DEBUG = True
def debug_print(*args):
    if DEBUG: print("[DEBUG]", *args)

messages = []
current_speed = 1.0
running = True

def sanitize_text(text):
    """Clean text for safe rendering"""
    return text.replace('\x00', ' ').encode('utf-8', 'replace').decode('utf-8')

def process_payload(topic, payload):
    """Extract specific JSON fields if configured"""
    try:
        json_fields = config["mqtt"].get("json_fields", {})
        if topic in json_fields:
            data = json.loads(payload)
            field = json_fields[topic]
            return str(data.get(field, "N/A"))
    except json.JSONDecodeError:
        return "Invalid JSON"
    except Exception as e:
        debug_print(f"JSON processing error: {e}")
    return payload

try:
    # Load configuration
    debug_print("Loading config.json...")
    with open("config.json") as f:
        config = json.load(f)
    
    mqtt_conf = config["mqtt"]
    screen_conf = config["screensaver"]

    # Pygame initialization
    debug_print("Initializing Pygame...")
    pygame.init()
    screen = pygame.display.set_mode(
        (screen_conf["width"], screen_conf["height"]),
        pygame.DOUBLEBUF | pygame.HWSURFACE
    )
    pygame.display.set_caption("MQTT Matrix Screensaver")
    font = pygame.font.SysFont(screen_conf["font_name"], screen_conf["font_size"], bold=True)

    # Color configuration
    colors = {
        "topic": tuple(screen_conf["topic_color"]),
        "payload": tuple(screen_conf["payload_color"]),
        "keywords": {k.lower(): tuple(v) for k, v in screen_conf["keywords"].items()},
        "background": tuple(screen_conf["background_color"])
    }

    # MQTT Client setup
    client = mqtt.Client()

    def on_connect(client, userdata, flags, rc):
        debug_print(f"Connected with code: {rc}")
        if rc == 0:
            for topic in mqtt_conf["topics"]:
                formatted_topic = topic.replace('*', '#')
                client.subscribe(formatted_topic)
                debug_print(f"Subscribed to: {formatted_topic}")

    def on_message(client, userdata, msg):
        try:
            # Process payload
            raw_payload = msg.payload.decode('utf-8', errors='replace')
            processed_payload = process_payload(msg.topic, raw_payload)
            
            # Apply payload limits
            if len(processed_payload) > screen_conf['payload_char_limit']:
                processed_payload = "!!!"
            
            topic = sanitize_text(msg.topic)
            full_text = f"{topic}: {processed_payload}"
            
            # Initialize color array
            color_list = []
            text_lower = full_text.lower()
            
            # Create default color array
            topic_part_end = len(topic) + 2  # ": " after topic
            for i in range(len(full_text)):
                color = colors["topic"] if i < topic_part_end else colors["payload"]
                color_list.append(color)
            
            # Apply keyword colors
            sorted_keywords = sorted(colors["keywords"].items(), 
                                   key=lambda x: len(x[0]), 
                                   reverse=True)
            
            for keyword, color in sorted_keywords:
                kw_len = len(keyword)
                start = 0
                while start <= len(text_lower) - kw_len:
                    if text_lower[start:start+kw_len] == keyword:
                        for i in range(start, start + kw_len):
                            if i < len(color_list):
                                color_list[i] = color
                        start += kw_len
                    else:
                        start += 1

            messages.append({
                "text": full_text,
                "x": random.randint(0, screen_conf["width"]),
                "y": -len(full_text) * screen_conf["font_size"],
                "speed": current_speed * random.uniform(0.7, 1.3),
                "chars": [{"char": c, "color": color_list[i]} for i, c in enumerate(full_text)],
                "alpha_step": (255 - screen_conf["min_alpha"]) / len(full_text) if len(full_text) > 0 else 0
            })

        except Exception as e:
            debug_print("Message processing error:", e)

    client.on_connect = on_connect
    client.on_message = on_message
    
    if mqtt_conf.get("username"):
        client.username_pw_set(mqtt_conf["username"], mqtt_conf["password"])
    
    debug_print("Connecting to MQTT broker...")
    client.connect(mqtt_conf["broker"], mqtt_conf["port"], 60)
    mqtt_thread = threading.Thread(target=client.loop_forever, daemon=True)
    mqtt_thread.start()

    # Main loop
    debug_print("Entering main loop")
    clock = pygame.time.Clock()
    while running:
        delta_time = clock.tick(60) / 1000.0
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                    current_speed = min(current_speed * 1.1, 5.0)
                    debug_print(f"Speed increased to {current_speed:.2f}")
                elif event.key == pygame.K_MINUS:
                    current_speed = max(current_speed * 0.9, 0.1)
                    debug_print(f"Speed decreased to {current_speed:.2f}")
                elif event.key == pygame.K_c:
                    messages.clear()
                    debug_print("Screen cleared")

        # Update and render
        screen.fill(colors["background"])
        
        for msg in messages[:]:
            msg["y"] += msg["speed"] * delta_time * 60
            
            for i, char_data in enumerate(msg["chars"]):
                try:
                    alpha = screen_conf["min_alpha"] + i * msg["alpha_step"]
                    surface = font.render(char_data["char"], True, char_data["color"])
                    surface.set_alpha(alpha)
                    screen.blit(surface, (msg["x"], msg["y"] + i * screen_conf["font_size"]))
                except Exception as e:
                    debug_print(f"Rendering error: {str(e)}")
                    continue
            
            if msg["y"] > screen_conf["height"] + len(msg["text"]) * screen_conf["font_size"]:
                messages.remove(msg)

        pygame.display.flip()

except Exception as e:
    traceback.print_exc()
finally:
    running = False
    try:
        if 'client' in locals():
            client.loop_stop()
            client.disconnect()
    except Exception as e:
        debug_print("Error disconnecting MQTT:", e)
    
    try:
        pygame.quit()
    except Exception as e:
        debug_print("Error quitting Pygame:", e)
    
    debug_print("Clean shutdown completed")