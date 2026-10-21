# 歷次對話原始紀錄：預排課程查詢與彈窗對話盒事件監聽

> 📅 對話區間：2026-06-02 03:47 ~ 04:51  
> 🆔 所屬階段：Milestone 002  
> 🔒 隱私安全：機敏學號與憑證已執行脫敏遮蔽處理

---

### 💬 對話輪次 #8 (Step 51, 時間: 2026-06-02T03:47:33Z)

#### 👤 使用者 (User):
登入後：
1. 點擊這個按鈕<input type="submit" name="ctl00$ContentPlaceHolder1$Button7" value="查詢預排課程" id="ContentPlaceHolder1_Button7" title="帶出自己預排課程">
2. 會出現這個表格<table cellspacing="0" rules="all" border="1" id="ContentPlaceHolder1_grd_subjs" style="font-size:8pt;width:100%;border-collapse:collapse;">
		<tbody><tr>
			<th class="th1" scope="col">&nbsp;</th><th class="th2" scope="col">課程代碼</th><th class="th3" scope="col">課程名稱</th><th class="th4" scope="col">必修<br>選修</th><th class="th5" scope="col">授課教師</th><th class="th6" scope="col">上課時間</th><th class="th7" scope="col">上課教室</th><th class="th8" scope="col">學分/小時</th><th class="th9" scope="col">限修<br>模式</th><th class="th10" scope="col">限修<br>人數</th><th class="th11" scope="col">通識<br>領域</th><th class="th14" scope="col">課程<br>狀態</th><th class="th3" scope="col">備註說明</th><th scope="col">&nbsp;</th><th scope="col">&nbsp;</th>
		</tr><tr style="background: rgb(255, 255, 255); cursor: pointer;">
			<td></td><td title="點選課程代碼可以查詢總數課人數."><a onclick="return qc(115172089,$(this))" href="#">CP__23600</a></td><td>(學二)夢與心理學研討<a href="course_outline.ashx?width=375&amp;subj=115172089" id="_115172089" class="jTip" name="課綱"><img src="images/question.png" class="question"></a></td><td>學程<a href="course_program.ashx?width=375&amp;subj=115172089" id="_115172089" class="jTip" name="學程"><img src="images/question.png" class="question"></a></td><td>/李沐齊</td><td>/五4/五5/五6</td><td><a onclick="return showMap(1312,1725)" href="#" title="點選大樓編號可以查看地圖上位置.">(4)</a>/人社一館D107</td><td>3/3</td><td title="3.以本系所學生優先。">3:諮商與臨床心理學系優先</td><td>40</td><td>&nbsp;</td><td>正常</td><td>&nbsp;</td><td style="width:1px;white-space:nowrap;"></td><td style="width:1px;white-space:nowrap;"></td>
		</tr><t
<truncated 10452 bytes>

			<td></td><td title="點選課程代碼可以查詢總數課人數."><a onclick="return qc(115165775,$(this))" href="#">HASS10050</a></td><td>(學一)人文學經典導讀<a href="course_outline.ashx?width=375&amp;subj=115165775" id="_115165775" class="jTip" name="課綱"><img src="images/question.png" class="question"></a></td><td>學程<a href="course_program.ashx?width=375&amp;subj=115165775" id="_115165775" class="jTip" name="學程"><img src="images/question.png" class="question"></a></td><td>/馬翊航/魏慈德/許甄倚/劉慧/林潤華</td><td>/五4/五5/五6</td><td><a onclick="return showMap(1272,1573)" href="#" title="點選大樓編號可以查看地圖上位置.">(5)</a>/人社二館-第三講堂B009</td><td>3/3</td><td title="3.以本系所學生優先。">3:人文社會科學學院優先</td><td>150</td><td>&nbsp;</td><td>正常</td><td>&nbsp;</td><td style="width:1px;white-space:nowrap;"></td><td style="width:1px;white-space:nowrap;"></td>
		</tr><tr style="background: rgb(246, 246, 246); cursor: pointer;">
			<td></td><td title="點選課程代碼可以查詢總數課人數."><a onclick="return qc(115152365,$(this))" href="#">YY__5061AA</a></td><td>(校核心)體育(三)_超慢跑AA<a href="course_outline.ashx?width=375&amp;subj=115152365" id="_115152365" class="jTip" name="課綱"><img src="images/question.png" class="question"></a></td><td>必</td><td>/江正發</td><td>/二9/二10</td><td>/D區體能訓練室</td><td>1/2</td><td title="1.先上網選課者優先。">1:先上網選課者優先</td><td>55</td><td>/體適能運動</td><td>正常</td><td>&nbsp;</td><td style="width:1px;white-space:nowrap;"></td><td style="width:1px;white-space:nowrap;"></td>
		</tr>
	</tbody></table>
這個表格的第二行的第一格子，過後會有一個button，需要點擊

3. 點擊後，會跳出一個DIV 彈出視窗處理，只有一個按鈕要點擊

然後重複2、3，直到結束

#### 🤖 助理 (Antigravity Agent):
我已經幫您把這個超強的「自動加選預排課程」迴圈加進程式裡了！

以下是現在程式**登入後**會全自動執行的流程：
1. 自動點選「**查詢預排課程**」的按鈕，並等待底下那個 `<table id="ContentPlaceHolder1_grd_subjs">` 表格讀取出來。
2. 計算表格總共有幾列課程資料，然後開始**逐列掃描**。
3. 對於每一列，程式會去檢查第一格 (第一欄) 裡面有沒有可以點擊的按鈕。
   - 如果有按鈕，它會自動點下去。
   - 點擊後，它會自動尋找並點擊跳出的 `DIV` 對話視窗裡的「確認」按鈕（也就是您提到的只會有一個要點的按鈕）。
   - 點擊完視窗後，程式會刻意等大約 1.5 秒鐘讓網頁資料傳輸完畢，再繼續檢查下一列。
   - 如果遇到沒有按鈕的列（或是已經加選過的），程式會自動略過。
4. 直到全部的列都掃過一遍後，程式依然會為您**保持瀏覽器開啟**。

因為您提到的按鈕（在正式開放時才會出現）可能有各種標籤形式，所以我設定了最寬容的抓法（不管是 `<button>` 還是 `<input type="button">` 或 `<input type="submit">` 它都會精準點擊）。

您可以隨時執行測試看看，這就是一個完全自動化的搶課雛形了：
```bash
uv run python auto_login.py
```

---

### 💬 對話輪次 #9 (Step 57, 時間: 2026-06-02T03:54:02Z)

#### 👤 使用者 (User):
- 點擊完視窗後，程式會刻意等大約 1.5 秒鐘讓網頁資料傳輸完畢，再繼續檢查下一列。
就繼續點擊了，不要等太久，0.5秒即可

#### 🤖 助理 (Antigravity Agent):
沒問題！為了讓搶課速度最大化，我已經將該步驟的等待時間從 1.5 秒縮短為 **0.5 秒**了。

現在程式關閉彈出視窗後，只要稍微暫停 0.5 秒就會立刻無縫接軌去點擊下一列的課程，大幅提升了執行的流暢度與速度！

---

### 💬 對話輪次 #10 (Step 63, 時間: 2026-06-02T03:56:22Z)

#### 👤 使用者 (User):
自動點選「查詢預排課程」的按鈕，並等待底下那個 <table id="ContentPlaceHolder1_grd_subjs"> 表格讀取出來。
就先暫停，我在terminal輸入Y，就開始點擊按鈕。直到全部結束

#### 🤖 助理 (Antigravity Agent):
我已經幫您加上這個安全暫停的功能了！

現在程式登入、點開「查詢預排課程」，並等到底下那個表格讀取出來之後，**它會完全停下來**，然後在終端機（Terminal）顯示這個提示：

```text
=============================================
表格已成功讀取！
請在終端機輸入 Y 並按下 Enter 鍵，即開始全自動點擊：
```

這時候您可以先在瀏覽器畫面上確認一下狀況，確定都準備好之後，只要在終端機輸入 `Y` 並按下 `Enter`，程式就會立刻以剛剛設定的 0.5 秒高速模式，一路往下自動點擊直到結束！

您可以重新執行這行指令親自體驗看看整個流程的節奏：
```bash
uv run python auto_login.py
```

---

### 💬 對話輪次 #11 (Step 69, 時間: 2026-06-02T03:57:59Z)

#### 👤 使用者 (User):
=============================================
表格已成功讀取！ -》在這裡告訴我有幾個row
請在終端機輸入 Y 並按下 Enter 鍵，即開始全自動點擊：

#### 🤖 助理 (Antigravity Agent):
已經更新完畢！

現在程式暫停時，終端機的提示會清楚顯示出抓到了幾筆課程，像是這樣：

```text
=============================================
表格已成功讀取！共有 14 列資料。
請在終端機輸入 Y 並按下 Enter 鍵，即開始全自動點擊：
```

這樣您在按下開始之前，就能精準核對程式抓到的課程數量是否與畫面上一樣了！

---

### 💬 對話輪次 #12 (Step 75, 時間: 2026-06-02T03:59:29Z)

#### 👤 使用者 (User):
你這裡寫14列是對的，但是terminal顯示只有1列

#### 🤖 助理 (Antigravity Agent):
啊，我懂了！這是一個經典的「非同步讀取（AJAX）」時間差問題。

因為學校系統在點擊「查詢預排課程」後，雖然表格的「外框」瞬間就出現了（所以程式判定它讀取到 1 列舊資料或空資料），但實際上**課程內容還在從伺服器下載中**，導致程式算完數量後，真正的 14 列課程才慢半拍浮現出來。

我已經在程式碼中幫您補上了**兩道防護機制**：
1. 點擊按鈕後，程式會先**強制等待網路傳輸完全靜止** (`networkidle`)。
2. 接著，程式會刻意**盯著表格，直到偵測到第一筆「真實的資料列」渲染出來**，甚至額外多等 0.5 秒讓網頁畫面完全穩定，然後才去計算總共有幾列。

現在它應該能精準無誤地抓到您實際的課程數量（例如 14 列）了。請再次執行看看：
```bash
uv run python auto_login.py
```

---

### 💬 對話輪次 #13 (Step 81, 時間: 2026-06-02T04:51:27Z)

#### 👤 使用者 (User):
<USER_REQUEST>
除了Y，也要有N，N就是我要準備關閉browser
▶️  Closing browser...
Exception in callback SyncBase._sync.<locals>.<lambda>(<Task finishe...been closed')>) at /Users/limchinkun/Desktop/PyTest/.venv/lib/python3.11/site-packages/playwright/_impl/_sync_base.py:111
handle: <Handle SyncBase._sync.<locals>.<lambda>(<Task finishe...been closed')>) at /Users/limchinkun/Desktop/PyTest/.venv/lib/python3.11/site-packages/playwright/_impl/_sync_base.py:111>
Traceback (most recent call last):
  File "/Users/limchinkun/.local/share/uv/python/cpython-3.11.15-macos-aarch64-none/lib/python3.11/asyncio/events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "/Users/limchinkun/Desktop/PyTest/.venv/lib/python3.11/site-packages/playwright/_impl/_sync_base.py", line 111, in <lambda>
    task.add_done_callback(lambda _: g_self.switch())
                                     ^^^^^^^^^^^^^^^
  File "/Users/limchinkun/Desktop/PyTest/.venv/lib/python3.11/site-packages/playwright/_impl/_connection.py", line 472, in _listener_with_error_handler_attached
    potential_future = listener(params)
                       ^^^^^^^^^^^^^^^^
  File "/Users/limchinkun/Desktop/PyTest/.venv/lib/python3.11/site-packages/playwright/_impl/_browser_context.py", line 171, in <lambda>
    "dialog", lambda params: self._on_dialog(from_channel(params["dialog"]))
                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/limchinkun/Desktop/PyTest/.venv/lib/python3.11/site-packages/playwright/_impl/_browser_context.py", line 679, in _on_dialog
    has_listeners = page.emit(Page.Events.Dialog, dialog) or has_listeners
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/limchinkun/Desktop/PyTest/.venv/lib/python3.11/site-packages/pyee/asyncio.py", line 70, in emit
    return super().emit(event, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/limchinkun/Desktop/PyTest/.venv/lib/python3.11/site-packages/pyee/base.py", line 22
<truncated 45215 bytes>
n/Desktop/PyTest/.venv/lib/python3.11/site-packages/playwright/_impl/_sync_base.py:111>
Traceback (most recent call last):
  File "/Users/limchinkun/.local/share/uv/python/cpython-3.11.15-macos-aarch64-none/lib/python3.11/asyncio/events.py", line 84, in _run
    self._context.run(self._callback, *self._args)
  File "/Users/limchinkun/Desktop/PyTest/.venv/lib/python3.11/site-packages/playwright/_impl/_sync_base.py", line 111, in <lambda>
    task.add_done_callback(lambda _: g_self.switch())
                                     ^^^^^^^^^^^^^^^
  File "/Users/limchinkun/Desktop/PyTest/.venv/lib/python3.11/site-packages/playwright/_impl/_connection.py", line 472, in _listener_with_error_handler_attached
    potential_future = listener(params)
                       ^^^^^^^^^^^^^^^^
  File "/Users/limchinkun/Desktop/PyTest/.venv/lib/python3.11/site-packages/playwright/_impl/_browser_context.py", line 171, in <lambda>
    "dialog", lambda params: self._on_dialog(from_channel(params["dialog"]))
                             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/limchinkun/Desktop/PyTest/.venv/lib/python3.11/site-packages/playwright/_impl/_browser_context.py", line 679, in _on_dialog
    has_listeners = page.emit(Page.Events.Dialog, dialog) or has_listeners
                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/limchinkun/Desktop/PyTest/.venv/lib/python3.11/site-packages/pyee/asyncio.py", line 70, in emit
    return super().emit(event, *args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/limchinkun/Desktop/PyTest/.venv/lib/python3.11/site-packages/pyee/base.py", line 220, in emit
    handled = self._call_handlers(event, args, kwargs)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/limchinkun/Desktop/PyTest/.venv/lib/python3.11/site-packages/pyee/base.py", line 196, in _call_h
<truncated 11672 bytes>

NOTE: The output was truncated because it was too long. Use a more targeted query or a smaller range to get the information you need.

#### 🤖 助理 (Antigravity Agent):
這兩個問題我都幫您解決了！

1. **新增 N 結束選項**：
   我修改了終端機的提示文字與邏輯。現在如果您輸入 `N`，程式會立刻接收到您的取消指令，並**直接乾淨俐落地關閉瀏覽器並結束程式**，不用再等到最後了。

2. **修復紅字報錯 (TargetClosedError)**：
   您剛剛看到的長串紅色報錯，是因為當您手動關閉程式或是程式強制結束時，Playwright 剛好在背景試圖攔截網頁彈出的原生警告視窗，但那時「瀏覽器已經正在關閉中」導致的衝突。
   我已經在原本處理對話框的程式碼加上了**保護機制 (Try-Catch)**。現在就算在關閉的瞬間遇到視窗彈出，程式也會安靜地略過，再也不會吐出那一大串嚇人的錯誤訊息了！

您可以再次執行看看，現在輸入 `N` 就可以完美結束程式：
```bash
uv run python auto_login.py
```

---
