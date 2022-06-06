# DSAI-HW3-2021

## Source

  - [Slide 2022](https://docs.google.com/presentation/d/1ZwXe4xMflCxiDQ7RK6z_LH88r0Dp38sQ/edit#slide=id.p1)
  - [Dashboard 2022](https://docs.google.com/spreadsheets/d/1hqoxG48A159buQ-GuoU7Fo-QrGKYmE1DFgPckJR0dFI/edit#gid=0)

## Rules

- SFTP

```

┣━ upload/
┗━ download/
   ┣━ information/
   ┃  ┗━ info-{mid}.csv
   ┣━ student/
   ┃  ┗━ {student_id}/
   ┃     ┣━ bill-{mid}.csv
   ┃     ┗━ bidresult-{mid}.csv
   ┗━ training_data/
      ┗━ target{household}.csv  
      
```

1. `mid` 為每次媒合編號
2. `household` 為住戶編號，共 50 組
3. 請使用發給組長的帳號密碼，將檔案上傳至 `upload/`
4. 相關媒合及投標資訊皆在 `download/` 下可以找到，可自行下載使用


- File

```

┗━ {student_id}-{version}.zip
   ┗━ {student_id}-{version}/
      ┣━ Pipfile
      ┣━ Pipfile.lock
      ┣━ main.py
      ┗━ {model_name}.hdf5

```

1. 請務必遵守上述的架構進行上傳 (model 不一定要有)
2. 檔案壓縮請使用 `zip`，套件管理請使用 `pipenv`，python 版本請使用 `3.8`
3. **檔名：{學號}-{版本號}.zip，例：`E11111111-v1.zip`**
4. 兩人一組請以組長學號上傳
5. 傳新檔案時請往上加版本號，程式會自動讀取最大版本
6. 請儲存您的模型，不要重新訓練

- Bidding

1. 所有輸入輸出的 csv 皆包含 header
2. 請注意輸入的 `bidresult` 資料初始值為空
   - 但仍然會有 header
3. 輸出時間格式為 `%Y-%m-%d %H:%M:%S` ，請利用三份輸入的 data 自行選一份，往後加一天即為輸出時間  
   例如: 輸入 `2018-08-25 00:00:00 ~ 2018-08-31 23:00:00` 的資料，請輸出 `2018-09-01 00:00:00 ~ 2018-09-01 23:00:00` 的資料(一次輸出`一天`，每筆單位`一小時`)
4. 程式每次執行只有 `120 秒`，請控制好您的檔案執行時間
5. 每天的交易量限制 `100 筆`，只要有超出會全部交易失敗，請控制輸出數量
6. 修正後的電費公式
   ![修正後的電費公式](img/公式修改說明.png)
7. 台電電價 (市電單價)
   - 2.5256 (NTD/kw)

## Prerequisite
- python 3.8 (仍然可以使用 conda 模擬)
- [pipenv](https://pypi.org/project/pipenv/)
   要使用管理員模式安裝
   ```shell 
   pip install pipenv
   ```

### Install Dependency
```shell 
pipenv install
```

### Start Virtual Environment
```shell 
pipenv shell
```

### Usage
```shell 
python main.py
```

## Strategy
分析後得知，此比賽的交易價格是以買賣雙方的市場供需所決定，更精確來說，在供給量足夠的情況下，所有 Agents 的成交市場價最終只會低於或等於 buyers 的最低收購價，也就是價格其實是由 Sellers 所決定的。(賣方想要獲利最大化，買方想撿到最實惠的價格，雙方都想要使交易成功，則 Sellers 必須猜中並低於 buyers 的願購價格，使交易成功)

這個機制使得某個 Seller 即使開出售價 0.01 元/度，且 buyers 願意以大於或等於 0.01 元/度的價格收購 (例如願購 2.53 元/度)，只要有另一個 Seller 猜中並制定 2.53 元/度，則供給量足夠的前提下，所有 Agents 都會以 2.53 元/度成交，也就是就算我只 sell 0.01 元/度仍然可以自動變成 2.53 元/度售出，隱性賺到利潤，並且因為我的原預售價格較低，可以獲得較高都販售優先權 (假設此區間所有 Agents 都是相同時間點進行交易)。

反之，buyer 只要訂一個高於台電售價的價格 (例如 2.53 元/度)，只要有另一個 buyer 願意用低於台電價進行收購，則原本 2.53 元/度的求購價也會自動降低，使購買成本低於預算，隱性撿到便宜。

這就是吾人的計策，名為「[草船借箭](https://youtu.be/XicdpSmxuT0?t=1)」；假使全班都是周瑜，看穿了這個戲碼並都設定 0.01 元/度且僅交易 0.01 度，則就是較量個人所訓練的 model 預測自家耗電量與產電量的實力了。

## Training Model
LSTM