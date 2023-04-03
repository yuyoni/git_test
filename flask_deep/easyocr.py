# 이 클래스는 easyOCR처럼 한번만 인스턴스 만들면 됨
class OCR:
    def __init__(self):
        # 성분 사전 불러오기 --> 서버 부담 줄이려면 서버에서 전역으로 불러와야함
        import pandas as pd
        import easyocr
        data = pd.read_excel('/Users/yuyeon/preproj/pyflask/flask_deep/all_sheet.xlsx')
        self.user_dictionary = [i for i in data["표준 성분명"]]
        self.reader = easyocr.Reader(['ko', 'en'])
    
    def ocr(self, img):
        """
        * img : 전성분 부분만 크롭된 이미지
        """
        result = self.reader.readtext(img)
        return result
    
    def ocrWord(self, result):
        """
        *입력으로 ocr함수 리턴 값인 result 받아야함
        * 한글, 영어, 숫자, 숫자 사이 쉽표만 추출
        * ! --> 1 로 변환
        """
        import re
        ocr_word = []
        for x in result:
            text = x[1] 
            text_mod = re.sub(r'[^\w\s\-(\d,\d)]', '', text.replace('!', '1')).replace('  ', ' ')
            ocr_word.extend([y for y in text_mod.split(' ') if len(y) != 1])
            
        return ocr_word
        
    def word(self, ocr_word):
        """
        Levenshtein 모듈로 단어 사전에서 유사단어 찾아내서 리스트에 추가함
        유사단어가 없으면 원래 단어를 리스트에 추가함
        """
        import Levenshtein
        import numpy as np
        
        temp = []
        
        for x in ocr_word:
        # 입력한 단어와 사전의 각 단어들 사이의 Levenshtein Distance를 계산
            distances = np.array([Levenshtein.distance(x, w) for w in self.user_dictionary])
            try:
                # 가장 유사한 단어의 인덱스
                index = np.argmin(distances)
                # 사전에서 가장 유사한 단어를 반환
                similar_word = self.user_dictionary[index]
                temp.append(similar_word)
            except ValueError:
                # 비슷한 단어가 없는 경우 입력한 단어 그대로
                temp.append(x)
                
        return temp
    
    def ingredientNum(self, survey_result, converted_text):
        """
        좋은 성분 또는 나쁜 성분 개수 추출하는 함수
        * survey_result : '건성' 또는 '지성'. 사용자가 질문에 응답한 결과임
        * converted_text : 단어 사전에서 유사한 단어로 바꾼 텍스트들. word함수 실행 결과임
        """
        oily_good = ["글라이콜릭애씨드","살리실릭애씨드","노녹시놀-9","녹차","위치하젤","레몬","캄파","멘톨",
                    "클로로필","알란토인","티트리","감초","징크옥사이드","포트마리골드꽃추출물","황","트리클로산",
                    "티타늄디옥사이드"]
        oily_bad = ["트라이글리세라이드","팔미틱애씨드","미리스틱애씨드","스테아릭애씨드", "코코넛야자오일","시어버터",
                "페트롤라툼","벤조페논-3","메톡시신나메이트","에칠헥실메톡시신나메이트"]
        dry_good = ["하이알루로닉애씨드","글리세린","프로필렌글라이콜",'1,3-부틸렌글라이콜',"소듐피씨에이","비타민E",
                   "비타민A","비타민C","엘라스틴","아보카도오일","달맞이꽃오일","오트밀","카모마일","오이","복숭아",
                   "해조추출물","뽕나무껍질추출물","코직애씨드","알부틴","포도씨추출물","베타-카로틴","시어버터",
                   "피카리아미나리아재비추출물","비타민B복합체","판테놀"]
        dry_bad = ["알코올","암모늄라우릴설페이트","암모늄라우레스설페이트","소듐라우레스설페이트","멘톨","페퍼민트"]
        
        if survey_result == '지성':
            bad_cnt = 0
            good_cnt = 0
            bad_list = []
            good_list = []
            for i, word in enumerate(converted_text):
                if word in oily_bad:
                    bad_cnt += 1
                    bad_list.append(converted_text[i])

                elif word in oily_good:
                    good_cnt += 1
                    good_list.append(converted_text[i])
                    
            """
            if bad_cnt > 0 :
                return("부적절")
            else :
                return("적절")"""

            return bad_cnt

        elif survey_result == '건성':
            bad_cnt = 0
            good_cnt = 0
            bad_list = []
            good_list = []
            for i, word in enumerate(converted_text):
                if word in dry_bad:
                    bad_cnt += 1
                    bad_list.append(converted_text[i])
                elif word in dry_good:
                    good_cnt += 1
                    good_list.append(converted_text[i])
                    
            """
            if bad_cnt > 0 :
                return("부적절")
            else :
                return("적절")"""
            
            return bad_cnt


        else:
            return 'This type of skin is not supported'