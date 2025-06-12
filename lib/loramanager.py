from lora import *
import time

# Counter for message tracking
counter = 0

# Create LoRa instance with longer poll times
lora = Lora(band=BAND_EU868, poll_ms=120000, debug=True)  # Enable debug mode

# Device credentials for TTN
DEV_EUI = ""  # Your DevEUI
APP_EUI = ""  # Can be all zeros for TTN
APP_KEY = ""  # Your AppKey

# Function to establish connection with TTN
def connectToTtn():
    print("Attempting to connect to TTN...")
    try:
        # Try with a longer timeout for better success rate
        lora.join_OTAA(APP_EUI, APP_KEY, timeout=20000)
        print("Connected to TTN successfully.")
        # Set port for uplink messages
        lora.set_port(3)
        lora.set_datarate(0)
        print(f"Data rate set to: {lora.get_datarate()}")
        return True
    except LoraErrorTimeout as e:
        print("Connection timeout; try moving near a window and retry")
        print("ErrorTimeout:", e)
        return False
    except LoraErrorParam as e:
        print("ErrorParam:", e)
        return False
    except Exception as e:
        print(f"Unexpected connection error: {e}")
        return False

# Main loop to continuously send data
def sendData(jsonData, confirmationNeeded = False):
    global counter
    try:
        # Send data with error handling
        try:
            if lora.send_data(jsonData, confirmationNeeded):
                print("Message sent successfully.")
                if confirmationNeeded:
                    print("Message confirmed by network.")
            else:
                if confirmationNeeded:
                    print("Message sent but not confirmed by network.")
                else:
                    print("Message sending status unknown (unconfirmed message).")

            # Successfully sent, increment counter
            counter += 1

        except LoraErrorBusy as e:
            print(f"LoRa module busy: {e}")
            print("Waiting 10 seconds before trying again...")
            time.sleep(10)

        except LoraErrorTimeout as e:
            print(f"Send timeout: {e}")
            # Check if we still have connection
            if lora.get_join_status() == 0:  # Not joined
                print("Lost connection to network. Attempting to rejoin...")
                connectToTtn()

        except Exception as e:
            print(f"Unexpected send error: {e}")
            time.sleep(5)

        # Check for downlink messages and poll more aggressively
        for _ in range(3):  # Check multiple times for downlinks
            try:
                lora.poll()  # Poll for downlinks
                if lora.available():
                    data = lora.receive_data()
                    if data:
                        print("Received downlink!")
                        print("Data:", data)
                time.sleep(2)  # Short pause between polls
            except Exception as e:
                print(f"Error checking for downlink: {e}")

    except Exception as e:
        print(f"Error in main loop: {e}")
        time.sleep(30)
