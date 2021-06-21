from app import create_app 

if __name__ == "__main__":
    app = create_app('debug')
    app.run(debug=True, port=5055, host='0.0.0.0')