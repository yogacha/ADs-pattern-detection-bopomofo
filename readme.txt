各檔案功能:
    
    readme.txt
        正在向您說明。
    
    requirements.txt
        套件需求.
        其中 tensorflow, keras 不一定要照上面，我是因為使用 python 3.7 才使用那兩個版本。

    preprocessing_and_concept.ipynb
        僅說明做了那些前處理，輸出處理後檔案交給 preprocessing.py
        
    preprocessing.py
        將 preprocessing_and_concept.ipynb 的程式整理，執行時要求輸入一個csv路徑、輸出的檔案名稱後綴。
        完成後在 data/ 資料夾裡會出現檔案 (.txt和.csv)
        要預測其他資料集先經由這份，產生預處理後的資料。
        
    model1.py 
        第一個模型的配適過程和說明。結尾部分可供預測其它資料集並輸出檔案。
        
    model2.py 
        第二個模型的配適過程和說明。結尾部分有如何預測其他資料集。
    
    image/ooo.png
        用於 jupyter notebook 輔助說明的圖片
    
    model/cnn.h5
        方法二產生的深度學習模型
        
    data/ooxx.csv
        資料及域處理後資料
        
    
    