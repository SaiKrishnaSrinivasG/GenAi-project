1. Create a Virtual Environment
To isolate the project dependencies, create a virtual environment in the project directory:
python3 -m venv venv

2 . Activate the Virtual Environment
Activate the virtual environment. The command differs slightly depending on your operating system.

On macOS and Linux:source venv/bin/activate
On Windows:.\venv\Scripts\activate

3. Install Dependencies
Install the required packages from the requirements.txt file:pip install -r requirements.txt

4  Run the Flask Application
Once all dependencies are installed, you can run the Flask application by executing:python app.py
This will start the Flask server, and you should see output indicating that the server is running, typically on http://127.0.0.1:5000.


