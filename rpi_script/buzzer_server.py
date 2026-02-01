from flask import Flask, request, jsonify
from gpiozero import Buzzer
import sys
app = Flask(__name__)

BUZZER_PIN = 17

print(f"Starting Buzzer Server on GPIO {BUZZER_PIN}")
try:
    buzzer = Buzzer(BUZZER_PIN)
    print("-> Buzzer initialized.")
except Exception as e:
    print(f"Error initializing GPIO: {e}")
    sys.exit(1)

@app.route('/alarm', methods=['POST'])
def control_alarm():
    data = request.json
    status = data.get('status', 'off')
    if status == 'on':
        print("-> ALARM ON")
        buzzer.on()
    else:
        print("-> ALARM OFF")
        buzzer.off()
    return jsonify({"message": f"Alarm set to {status}"}), 200

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=False)
    except KeyboardInterrupt:
        print("\nStopping server...")
        buzzer.close()