from flask_deep import app
#import joblib

if __name__ == '__main__':
    #model = joblib.load('./model.h5')
    app.run(host='127.0.0.1', port="8000")