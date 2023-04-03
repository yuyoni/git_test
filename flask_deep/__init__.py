import os, sys
from flask import Flask, request, render_template, redirect
from . import easyocr


app = Flask(__name__, template_folder='templates')
app.debug=True

# Main page
@app.route('/')
def main():
    return render_template('index1.html')

# Question page - 피부타입 결정 및 타입결과 전송
@app.route('/ques')
def ques():
    return render_template('index2.html')

# Result page - 타입결과 화면에 출력하고 사진 입력받기. 불러온 모델에 사진과 타입결과 인수로 넣어서 결과 recommend 페이지로 전송
@app.route('/result', methods=['GET', 'POST'])
def result():
    type = request.args.get('type')
    
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files.get('file')
        
        if not file:
            return

        img = file.read()

        ocr = easyocr.OCR() # 한번만 실행

        result_ocr = ocr.ocr(img)
        ocr_text = ocr.ocrWord(result_ocr)
        converted_text = ocr.word(ocr_text)

        igd = ocr.ingredientNum(type, converted_text)

        return render_template('index3.html', type=type, igd="igd")
    
    else :
        return render_template('index3.html', value="No Files")

# Recommend page - 반환된 결과 받아서 출력
@app.route('/recommend', methods=['GET','POST'])
def recommend():
    result = request.args.get('result') # igd 인자 받기
    return render_template('index4.html')
