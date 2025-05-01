#!/usr/bin/env python3
import time
import smbus2
import os
import paho.mqtt.client as mqtt

# TF-Luna I2C address
TF_LUNA_ADDR = 0x10

# TF-Luna registers
DIST_REG = 0x00  # Distance data register
DIST_L = 0x00    # Distance data low byte
DIST_H = 0x01    # Distance data high byte
STRENGTH_L = 0x02  # Signal strength low byte
STRENGTH_H = 0x03  # Signal strength high byte
TEMP_L = 0x04      # Temperature low byte
TEMP_H = 0x05      # Temperature high byte

class TFLuna:
    def __init__(self, address=TF_LUNA_ADDR, bus_num=1):
        self.address = address
        self.bus = smbus2.SMBus(bus_num)
        
    def get_distance(self):
        """Read distance from TF-Luna sensor in cm"""
        try:
            # Read two bytes from register 0x00 (distance)
            dist_l = self.bus.read_byte_data(self.address, DIST_L)
            dist_h = self.bus.read_byte_data(self.address, DIST_H)
            
            # Combine the two bytes into distance value
            distance = (dist_h << 8) | dist_l
            return distance
        except Exception as e:
            print(f"Error reading distance: {e}")
            return None
            
    def get_signal_strength(self):
        """Read signal strength from TF-Luna sensor"""
        try:
            # Read two bytes from register 0x02 (strength)
            strength_l = self.bus.read_byte_data(self.address, STRENGTH_L)
            strength_h = self.bus.read_byte_data(self.address, STRENGTH_H)
            
            # Combine the two bytes into strength value
            strength = (strength_h << 8) | strength_l
            return strength
        except Exception as e:
            print(f"Error reading signal strength: {e}")
            return None
            
    def get_temperature(self):
        """Read internal temperature from TF-Luna sensor in Celsius"""
        try:
            # Read two bytes from register 0x04 (temperature)
            temp_l = self.bus.read_byte_data(self.address, TEMP_L)
            temp_h = self.bus.read_byte_data(self.address, TEMP_H)
            
            # Combine the two bytes into temperature value and convert to Celsius
            temp = (temp_h << 8) | temp_l
            temp_celsius = temp / 100.0  # Temperature is stored as 100x Celsius
            return temp_celsius
        except Exception as e:
            print(f"Error reading temperature: {e}")
            return None

def clear_screen():
    """Clear the terminal screen"""
    # For both Windows and Unix-like systems
    os.system('cls' if os.name == 'nt' else 'clear')

def publish_to_mqtt(client, topic, message):
    """Publish a message to the specified MQTT topic."""
    try:
        client.publish(topic, message)
    except Exception as e:
        print(f"Error publishing to MQTT: {e}")

def main():
    # Create TF-Luna sensor object
    tf_luna = TFLuna()
    
    # Initialize MQTT client
    mqtt_client = mqtt.Client()
    mqtt_broker = "192.168.1.250"  # Replace with your MQTT broker address
    mqtt_port = 1883               # Replace with your MQTT broker port if different
    mqtt_topic_distance = "Luna/Distance"
    mqtt_topic_time = "Luna/Time"
    
    try:
        mqtt_client.connect(mqtt_broker, mqtt_port)
        print("Connected to MQTT broker")
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}")
        return
        
    try:
        while True:
            # Read and display sensor data
            distance = tf_luna.get_distance()
            strength = tf_luna.get_signal_strength()
            temp = tf_luna.get_temperature()
            
            if distance is not None:
                # Publish distance to MQTT
                publish_to_mqtt(mqtt_client, mqtt_topic_distance, str(distance))
                # Publish timestamp to MQTT
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                publish_to_mqtt(mqtt_client, mqtt_topic_time, timestamp)       
            time.sleep(10)  # Update every 10 seconds
            
    except KeyboardInterrupt:
        print("Measurement stopped by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        mqtt_client.disconnect()
        print("Disconnected from MQTT broker")

if __name__ == "__main__":
    main()