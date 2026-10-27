# 台中社區查詢 — 部署與資料維護說明

## 檔案結構
```
index.html                 網頁本體（不需修改即可使用）
data/communities.json      全部社區資料與網站設定（主要維護這個檔）
plans/                     格局圖（自行建立，jpg/png/webp）
docs/                      建照存根、使照存根等掃描檔（自行建立，pdf/jpg）
ads/                       自售廣告圖片（自行建立）
```

## 上線方式（全部免費）
把整個資料夾上傳到 GitHub Pages、Netlify、Cloudflare Pages 或公司主機，用網址開啟即可。
必須用網址開啟，直接雙擊 index.html 會讀不到 JSON。

上線後會自動啟用：
- 3D 地圖：MapLibre + OpenFreeMap 圖資，**不需要任何金鑰**，可傾斜、旋轉，社區棟體以綠色量體標示。
- Google 地圖內嵌（地圖／衛星）：用免金鑰的 embed 網址。
- 街景、導航、Google Earth 3D：以連結開啟 Google 官方頁面。
- 每個社區的 3D 量體模型：依 `towers` 資料自動產生。

## 新增或修改社區
在 `communities` 陣列裡複製一筆修改即可，重要欄位：

| 欄位 | 說明 |
|---|---|
| `id` | 英數代號（如 `c13`），也是分享網址 `#c13` |
| `name` / `builder` / `contractor` / `architect` | 社區名、建設公司、營造廠、建築師 |
| `district` / `address` / `lat` / `lng` | 行政區、地址、座標（Google 地圖按右鍵可複製座標） |
| `type` / `status` / `completed` | 大樓・華廈・透天／預售・新成屋・成屋／完工西元年 |
| `structure` / `seismic` | RC・SRC・SC／一般・制震・隔震 |
| `towers` | 每棟：名稱、樓層、每層戶數、電梯數、量體寬深 `w` `d`、配置位置 `x` `z`（公尺） |
| `units` | 每個房型：`label`、`rooms`、`size_ping`（權狀）、`main_ping`（主建物）、`balcony_ping`、`count`、`facing`、`plan` |
| `units[].plan` | 格局圖路徑，例如 `plans/c13-3A.jpg`；留空會顯示自動繪製的格局示意 |
| `permit` | 建照字號與日期、使照字號與日期、使用分區、基地面積、建蔽率、容積率 |
| `price` | 單價區間、`trend` 每季均價、`deals` 成交紀錄 |
| `parking` / `public_ratio` / `mgmt_fee` / `property_mgmt` | 車位、公設比、管理費、物管公司 |
| `amenities` / `materials` | 公設清單、建材設備 |
| `nearby` | 學區、交通、商圈、公園、醫療、市場（含距離公尺） |
| `risks` | 土壤液化、淹水、斷層距離、嫌惡設施、海砂、輻射等 |
| `docs[].file` | 建照存根等文件路徑，例如 `docs/c13-build-permit.pdf`；有檔案就會顯示「開啟檔案」 |
| `sample` | 示範資料標記，正式資料請刪除或設為 `false` |
| `sponsored` | 設為 `true` 會置頂並標示「廣告・精選社區」（可向建商、代銷收費） |

## 廣告收益（meta.ads）
```json
"ads": {
  "show_placeholders": false,
  "list_every": 4,
  "adsense": { "client": "ca-pub-你的發布商ID", "slots": { "list": "清單版位ID", "detail": "詳細頁版位ID" } },
  "house": [ { "sponsor": "某某代銷", "title": "標題", "text": "說明", "url": "https://…", "image": "ads/xxx.jpg", "slots": ["list","detail"] } ]
}
```
- **Google AdSense**：申請通過後填入 `client` 與各版位 ID，網頁會自動載入廣告。另需在網站根目錄放 AdSense 要求的 `ads.txt`。
- **自售廣告**：`house` 可放建商、代銷、裝潢、貸款、搬家等業者的委刊；AdSense 未設定的版位才會顯示自售廣告。
- **精選社區**：社區加上 `"sponsored": true` 即置頂並標示為廣告。
- 版位位置：結果清單每 `list_every` 筆插一則、每個社區詳細頁底部一則。
- 確認位置時可把 `show_placeholders` 設為 `true`，上線前改回 `false`。

## 注意
- 實價、學區、液化、淹水等資料請標明來源與更新日期（`updated` 欄位），並以政府最新公告為準。
- 廣告須清楚標示「廣告」，網頁已自動加上。
