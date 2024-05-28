from app import create_app
from app.scheduler import start

app = create_app()

if __name__ == '__main__':
    start()  # Start the scheduler
    app.run(debug=True, host='0.0.0.0', port=5001)
