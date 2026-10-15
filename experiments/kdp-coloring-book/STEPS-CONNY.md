# EXP-001 · Conny 的机器人步骤

照着点就行。卡在任何一步，截图发到对话里。
**账号、银行、税务信息不要存进这个仓库**——它们只属于你的浏览器和密码管理器。

## 第一部分：开通 KDP 账号（现在就能做，约 20 分钟）

1. 浏览器打开 **https://kdp.amazon.com**。
2. 点右上角 **Sign in**，用你平时买东西的 Amazon 账号登录
   （没有就点 **Sign up** 新建一个）。
3. 首次进入会弹出 **Terms and Conditions** → 勾选同意 → **Agree**。
4. 页面顶部会出现黄条 *"Your account information is incomplete"* →
   点里面的 **Update now**（或右上角头像 → **Account**）。
5. 依次填三块（都在同一页上）：
   - **My Profile / Author information**：真实姓名、地址、电话。
   - **Getting Paid / Bank information**：点 **Add a bank account** →
     Country: United States → 填你美国银行账户的 **Routing number** 和
     **Account number**（手机银行 app 的账户详情里能查到）→ 保存。
   - **Tax information**：点 **Complete tax interview**，进入问卷：
     - 你是**美国税务居民**（绿卡或当年满足实质居住测试）→ 选 *U.S. person* →
       填 SSN → 相当于 W-9，预扣 0%。
     - 你是**非居民**（比如 F/J 签证前几年）→ 选 *Non-U.S. person* →
       国籍/税务居民国选 China → 有 SSN/ITIN 就填，并在 treaty 一步选
       **China** 申请协定税率（版税预扣 30% → 10%）；没有美国税号也能提交，
       只是享受不了协定税率。
     - 不确定自己算哪种：按你当年报税用的身份来（和你给学校报税时一致）。
     - 最后一步电子签名（输入你的名字）→ **Submit**。
6. 三块都打勾、黄条消失（显示 *account information is complete*）后，
   在对话里告诉我一声"**KDP 账号好了**"。

## 第二部分：上传这本书（账号开好后做，约 30 分钟）

1. 把两个文件下载到电脑（GitHub 仓库页 → `experiments/kdp-coloring-book/` →
   点 `interior.pdf` → 右上 **Download raw file**；`cover.pdf` 同样）。
2. 打开 **https://kdp.amazon.com** → 点黄色 **+ Create** → 选 **Paperback**。
3. **Paperback Details 页**：对照 [metadata.md](metadata.md) 逐项粘贴——
   Language、Book Title、Subtitle、Author、Description、Keywords（7 个框）、
   Categories（点 **Choose categories** 按 metadata.md 的路径选两个）。
   - **Series / Edition Number / Contributors**：留空。
   - **Sexually Explicit Content**：选 **No**；**Adult Content**：No。
   - **AI-Generated Content**：会弹三个问题，按 metadata.md 的"AI 内容申报"如实选。
   - 点 **Save and Continue**。
4. **Paperback Content 页**：
   - **Print ISBN**：点 **Get a free KDP ISBN** → Assign。
   - **Print Options**：Black & white interior with white paper ·
     Trim size **8.5 x 11 in** · **No Bleed** · Cover finish **Matte**。
   - **Manuscript**：点 **Upload paperback manuscript** → 选 `interior.pdf`。
   - **Book Cover**：选 **Upload a cover you already have** →（不勾 barcode 选项，
     封面右下已留白，KDP 自动加条码）→ 选 `cover.pdf`。
   - 等两个文件都显示处理完成 → 点 **Launch Previewer**（要等一两分钟）。
   - 在预览器里翻几页：图案没有被裁掉、没压到页边 → 点 **Approve**。
   - 页面底部显示印刷成本（应约 $2.84）→ **Save and Continue**。
5. **Paperback Rights & Pricing 页**：
   - Territories: **All territories**。
   - Primary marketplace: **Amazon.com**；List Price 填 **9.99** USD，
     其他市场保持 "Base on Amazon.com price"。表格里 Royalty 一栏应显示约 **$3.15**。
   - 点 **Publish Your Paperback Book**。
6. 之后是等待：KDP 审核最长 72 小时，通过后书页上线、邮件通知你。
   上线后把商品链接发到对话里，我把它记进 `EXPERIMENTS.md` 台账。
7. 看销量：kdp.amazon.com 顶部 **Reports** → Dashboard，按天显示订购数和版税。
