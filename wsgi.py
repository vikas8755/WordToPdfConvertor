import sys
import os

# Set the path to your project
project_home = 'C:\Users\Vikas Kumar Gautam\Desktop\python-app\Word_To_PDF'
if project_home not in sys.path:
    sys.path.append(project_home)

# Set the FLASK_APP environment variable
os.environ['FLASK_APP'] = 'app'

from app import app as application
if __name__ == "__main__":
    app.run(debug=True)
