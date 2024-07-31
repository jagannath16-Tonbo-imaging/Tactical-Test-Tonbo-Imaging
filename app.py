from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import serial  # Ensure pyserial is installed: pip install pyserial
from sensor_comm_v3 import SensorComm  # Ensure this module is in the same directory


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/mouseclick_polarity', methods=['POST'])
def mouseclick_polarity():
    try:
        data = request.json
        if not data:
            raise ValueError("No data received")

        com_port = data.get('com_port')
        baud_rate = data.get('baud_rate')
        value = data.get('value')
        button_type = data.get('button_type')

        # Log the received values for debugging
        print(f"Received values - COM_PORT: {com_port}, BAUD_RATE: {baud_rate}, VAL: {value}, BUTTON: {button_type}")

        if not com_port or not baud_rate or value is None or not button_type:
            raise ValueError("Invalid input: Missing required fields")

        # Determine the command based on the button type
        if button_type == 'brightness':
            cmd = 0xd0
        elif button_type == 'contrast':
            cmd = 0xd4
        elif button_type == 'polarity':
            cmd = 0x52
        else:
            raise ValueError("Invalid button type")

        # Simulating serial communication for testing
        print(f"Simulating writing {value} to {com_port} at baud rate {baud_rate} with command {hex(cmd)}")

        # Uncomment the following lines for actual serial communication
        ser = serial.Serial(com_port, baud_rate, timeout=5)
        cmd_gen = SensorComm(ser, dev_name='Athena640', idd='new')  # Adjust this according to your implementation        
        status = "Communication Failed"
        response = cmd_gen.fpga_write(cmd, value)
        if response['cmd_status'] == 0x00:
            status = "Communication Successful"
        ser.close()

        response_list = [
            response['header'], response['packet_sequence'] >> 8, response['packet_sequence'] & 0xFF, response['device_id'], response['device_number'],
            response['length'], response['cmd_type'], response['cmd_status'], response['cmd'] >> 8, response['cmd'] & 0xFF,
            response['data'], response['chksum'], response['footer1'], response['footer2']
        ]
        response_list = [hex(x) for x in response_list if isinstance(x, int)]

        # Return success message for now
        return jsonify({"status": status, "response": response_list, "message": f"Writing {value} to {hex(response['cmd'])} with command {hex(cmd)}"}), 200

    except Exception as e:
        print(f"Exception occurred: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(port=8000, debug=True)



