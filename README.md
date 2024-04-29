# ml-final-project

## 打扣前的準備

1. 到想要存放的資料夾打開終端機 git clone
    例如：`/Users/poyen/code/ml`
```bash
git clone https://github.com/poyen0806/ml-final-project.git
```
2. 建立自己的分支
```bash
git checkout branch -b "your-branch-name"
```
3. 檢查分支
```bash
git branch
```
4. 設定 push
```bash
git push --set-upstream origin "your-branch-name"
```
5. 每次打扣前先 pull
```bash
git pull origin main
```

## git commit 格式
可參照這個文章 [點我](https://github.com/NCU-GS4538-Linux/Linux-Community/discussions/230)

簡單一點的話就
- type
- header (動詞 + 描述)

範例如下：
- add: 新增空擋案或某某功能
- chore: 各種雜務
- refactor: 重建某某功能或檔案內容(只影響實作方式，不影響功能)
- fix: 修正某某錯誤