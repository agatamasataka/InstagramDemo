
// Mock Data for Local Images (copied from poto/)
const LOCAL_IMAGES = [
    "assets/579225706639130956.jpg",
    "assets/579225708769837278.jpg",
    "assets/579225710431306106.jpg",
    "assets/579225710833959461.jpg",
    "assets/579225711739404697.jpg",
    "assets/579225731385786895.jpg",
    "assets/579226577310057067.jpg",
    "assets/579226579037586127.jpg",
    "assets/579226579222921320.jpg",
    "assets/579226579357139389.jpg",
    "assets/579226579490832660.jpg",
    "assets/sw (1).jpg",
    "assets/テクノリンク　技術指導.jpg",
    "assets/伊藤超短波　講師経験.jpg"
];

const TEXT_TEMPLATES = [
    { title: "朝の挨拶", content: "おはようございます！\n今日の[地域名]は快晴ですね☀️\n\n当院は朝9時から元気に診療しております！\n急なぎっくり腰や寝違えなど、お困りの際はすぐにご連絡ください📞", usageCount: 12, lastUsed: "2026-01-20" },
    { title: "ビフォーアフター", content: "【施術ビフォーアフター】\n猫背矯正を受けていただいた患者様です✨\n\n左：施術前\n右：施術後\n\nたった1回でもこれだけ姿勢が変わります！\n姿勢が整うと、肩こりや頭痛の改善にも繋がりますよ😊", usageCount: 8, lastUsed: "2026-01-25" },
    { title: "キャンペーン", content: "📢 今月のキャンペーンお知らせ\n\n今なら「骨盤矯正」が初回限定で...\n通常 5,500円 ➡️ 2,980円！！\n\nこの機会にぜひお試しください✨\nご予約はプロフィールのリンクから！", usageCount: 5, lastUsed: "2026-01-15" },
    { title: "予約空き状況", content: "📅 本日の予約空き状況\n\n11:00 〜 ◯\n14:30 〜 △\n16:00 〜 ◯\n\n夕方以降は混み合いますので、早めのご予約をおすすめします！", usageCount: 30, lastUsed: "2026-01-28" },
    { title: "Q&A", content: "Q. 予約は必要ですか？\nA. 当院は予約優先制となっております。\n飛び込みも可能ですが、待ち時間を少なくするため事前連絡をお勧めしております📱", usageCount: 3, lastUsed: "2025-12-10" }
];

// --- Competitor Analysis Data ---
const COMPETITOR_DATA = [
    {
        id: "locaop",
        name: "ロカオプMEO対策でお客様を呼ぼう！",
        account_id: "@locaop_official",
        icon: "assets/app_icon_square.png", // specific icon or placeholder
        posts_per_month: 1,
        followers: 374,
        following: 24,
        description: "ローカルビジネスをオープンに！\n■店舗型ビジネスの集客サービス\n■WEBからの集客を最大化\n■店舗経営はまずロカオプから\nWeb集客ならロカオプ🌱\nGoogleマップ・クチコミ対策から予約システム、サイト制作、SNS集客までロカオプ一つで完了！\n販売代理店も大募集中です。\nお気軽にDMまで🎈",
        url: "https://locaop.jp/media/",
        recent_likes_total: 9,
        my_account: true,
        recent_posts: [
            { img: "assets/579225706639130956.jpg", likes: 3, caption: "【無料オンラインセミナー開催】\n宿泊&観光レジャー施設の「選ばれる」集客戦略..." },
            { img: "assets/579225708769837278.jpg", likes: 4, caption: "MEO対策のメリットとは？\nGoogleマップでの露出を増やして..." },
            { img: "assets/579225710431306106.jpg", likes: 2, caption: "ロカオプ導入事例のご紹介✨\n売上が前年比120%アップしました！" }
        ]
    },
    {
        id: "lasbocas",
        name: "銀座バル Las Bocas (ラスボカス)",
        account_id: "@las_bocas",
        icon: "assets/placeholder_competitor.png", // placeholder
        posts_per_month: 25,
        followers: 2287,
        following: 6388,
        description: "スペイン料理🇪🇸 瀬戸内直送シーフード&ワイン\n〜ラスボカス〜\n【ランチ】\n月・火・水・金・土：11:30~15:00\n木：11:30〜14:00\n【ディナー】\n月〜木・土　18:00〜23:00（L.O.22:00）\n金　18:00〜23:30（L.O.22:30）\n0334860409",
        url: "https://las-bocas.com/insta/link",
        recent_likes_total: 166,
        my_account: false,
        recent_posts: [
            { img: "assets/579226579608535078.jpg", likes: 45, caption: "¡Hola, febrero!\n皆様、こんにちは。少しずつ日が長くなり、春の訪れを待ちわびる2月..." },
            { img: "assets/579226580665761812.jpg", likes: 52, caption: "本日のオススメ！\n瀬戸内直送の新鮮な真鯛が入荷しました🐟..." },
            { img: "assets/579226581352841863.jpg", likes: 69, caption: "週末はワインで乾杯🍷\n新しいスペインワインが入りました..." }
        ]
    }
];


// --- Client Management Data ---
const CLIENTS = [
    { id: 101, name: "銀座バル Las Bocas", status: "承認待ち", deadline: "2026-01-28", isHandled: false, lastActivity: "投稿案提出済み" },
    { id: 102, name: "整骨院〇〇", status: "承認リジェクト", deadline: "2026-01-30", isHandled: false, lastActivity: "クライアントから差し戻し" },
    { id: 106, name: "フィットネス X", status: "承認待ち", deadline: "2026-02-05", isHandled: false, lastActivity: "構成案確認中" },
    { id: 104, name: "美容室 A-Salon", status: "未設定", deadline: "-", isHandled: false, lastActivity: "アカウント連携待ち" },
    { id: 103, name: "カフェ・ド・テスト", status: "正常稼働中", deadline: "2026-02-10", isHandled: true, lastActivity: "投稿完了" },
    { id: 105, name: "株式会社Demo", status: "正常稼働中", deadline: "2026-02-04", isHandled: true, lastActivity: "投稿スケジュール済み" },
];

// Initial Data
let SCHEDULES = [
    { id: 1, date: "2026-02-01", time: "10:00", category: "日常・風景", status: "投稿待ち", image: LOCAL_IMAGES[0], text: TEXT_TEMPLATES[0].content },
    { id: 2, date: "2026-02-05", time: "12:00", category: "施術・ビフォーアフター", status: "投稿待ち", image: LOCAL_IMAGES[1], text: TEXT_TEMPLATES[1].content },
    // Planned Items (No content yet)
    { id: 3, date: "2026-02-10", time: "09:00", category: "キャンペーン・お知らせ", status: "構成中", image: "", text: "" },
    { id: 4, date: "2026-02-14", time: "18:00", category: "スタッフ紹介", status: "構成中", image: "", text: "" },
    // Next Month
    { id: 5, date: "2026-03-01", time: "10:00", category: "日常・風景", status: "構成中", image: "", text: "" }
];

let APP_STATE = {
    currentTab: 'clients',
    currentMonthFilter: '2026-02', // YYYY-MM
    selectedScheduleId: null
};

document.addEventListener('DOMContentLoaded', () => {
    initTabs();
    renderClients(); // New
    renderSchedule();
    renderMaterials();
    renderTexts();
    renderCompetitors(); // New
    setupModals();
});

function initTabs() {
    const btns = document.querySelectorAll('.tab-btn');
    const sections = ['panel-clients', 'panel-schedule', 'panel-material', 'panel-text', 'panel-history']; // Added clients

    btns.forEach(btn => {
        btn.addEventListener('click', () => {
            // UI Toggle
            btns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            // Section Toggle
            const target = btn.dataset.target;
            sections.forEach(s => {
                const el = document.getElementById(s);
                if (el) el.style.display = 'none';
            });
            const targetEl = document.getElementById(`panel-${target}`);
            if (targetEl) targetEl.style.display = 'flex'; // Comp table needs flex

            APP_STATE.currentTab = target;
        });
    });
}

// --- Client List Logic ---
// --- Client List Logic ---
function renderClients() {
    const listBody = document.getElementById('client-list-body');
    const totalEl = document.getElementById('summary-total');
    const attnEl = document.getElementById('summary-attention');

    if (!listBody) return;
    listBody.innerHTML = '';

    const today = "2026-01-29"; // Fixed mocked date for demo consistency

    // Sort Logic:
    // 1. Overdue & Unhandled (Fire!) -> Top
    // 2. Unhandled (Normal) -> Middle
    // 3. Handled (Done) -> Bottom
    const sortedClients = [...CLIENTS].sort((a, b) => {
        const isFireA = (a.deadline !== "-" && a.deadline < today && !a.isHandled);
        const isFireB = (b.deadline !== "-" && b.deadline < today && !b.isHandled);

        if (isFireA && !isFireB) return -1;
        if (!isFireA && isFireB) return 1;

        // If both fire or both not fire, check Handled status
        if (!a.isHandled && b.isHandled) return -1;
        if (a.isHandled && !b.isHandled) return 1;

        // If same handled status, sort by deadline (earlier first)
        if (a.deadline === "-") return 1;
        if (b.deadline === "-") return -1;
        return a.deadline.localeCompare(b.deadline);
    });

    let attentionCount = 0;

    sortedClients.forEach(client => {
        const isFire = (client.deadline !== "-" && client.deadline < today && !client.isHandled);
        if (!client.isHandled) attentionCount++;

        const row = document.createElement('div');
        row.className = 'client-row';
        row.style.cssText = "display:grid; grid-template-columns: 2fr 1.5fr 1fr 2fr 1fr; gap:10px; padding:15px; background:white; border:1px solid #eee; border-radius:8px; align-items:center; cursor:pointer; transition:box-shadow 0.2s; position:relative; overflow:hidden;";

        // Fire Effect
        if (isFire) {
            row.style.border = "2px solid #D32F2F";
            row.style.background = "#FFEBEE";
        }

        row.onmouseover = () => {
            row.style.boxShadow = "0 4px 12px rgba(0,0,0,0.15)";
            row.style.transform = "translateY(-1px)";
        };
        row.onmouseout = () => {
            row.style.boxShadow = "none";
            row.style.transform = "none";
        };

        row.onclick = () => {
            document.querySelector('[data-target="schedule"]').click();
            alert(`「${client.name}」の管理画面へ移動します`);
        };

        // Status Design
        let stBg = "#eee", stColor = "#333", stText = client.status;
        if (client.status === "承認リジェクト") { stBg = "#FFCDD2"; stColor = "#B71C1C"; }
        else if (client.status === "承認待ち") { stBg = "#BBDEFB"; stColor = "#0D47A1"; }
        else if (client.status === "未設定") { stBg = "#F5F5F5"; stColor = "#616161"; }
        else if (client.status === "正常稼働中") { stBg = "#C8E6C9"; stColor = "#1B5E20"; }

        // Action Button Text
        let actionLabel = "管理";
        let actionStyle = "background:#333; color:white;";
        if (client.status === "承認リジェクト") { actionLabel = "再提案する"; actionStyle = "background:#D32F2F; color:white;"; }
        else if (client.status === "承認待ち") { actionLabel = "確認連絡"; actionStyle = "background:#1976D2; color:white;"; }
        else if (client.status === "未設定") { actionLabel = "設定開始"; actionStyle = "background:#F57C00; color:white;"; }

        // Fire Icon
        let fireHtml = isFire ? `<span style="font-size:16px; margin-right:5px;">🔥</span>` : "";
        let deadlineStyle = isFire ? "color:#D32F2F; font-weight:bold;" : "color:#555;";

        row.innerHTML = `
            <div style="font-weight:bold; font-size:14px; display:flex; align-items:center;">
                ${fireHtml} ${client.name}
            </div>
            <div>
                <span style="background:${stBg}; color:${stColor}; padding:4px 8px; border-radius:12px; font-size:11px; font-weight:bold;">${stText}</span>
            </div>
            <div style="font-size:12px; ${deadlineStyle}">期限: ${client.deadline}</div>
            <div style="font-size:11px; color:#666;">
                <div>${client.lastActivity}</div>
                <div style="color:${client.isHandled ? '#388E3C' : '#F57C00'}; font-size:10px;">${client.isHandled ? '● 今月対応済' : '⚠ 今月未完了'}</div>
            </div>
            <div style="text-align:center;">
                <button class="btn" style="${actionStyle} padding:6px 10px; font-size:11px; border-radius:15px; width:100%; box-shadow:0 1px 3px rgba(0,0,0,0.1);">${actionLabel}</button>
            </div>
        `;
        listBody.appendChild(row);
    });

    if (totalEl) totalEl.textContent = `全案件: ${CLIENTS.length}件`;
    if (attnEl) attnEl.innerHTML = `⚠️ 未対応: ${attentionCount}件`;
}

// --- Schedule Logic ---
function renderSchedule() {
    const list = document.getElementById('schedule-list');
    list.innerHTML = '';

    // Filter by Month
    const filtered = SCHEDULES.filter(s => s.date.startsWith(APP_STATE.currentMonthFilter));
    filtered.sort((a, b) => a.date.localeCompare(b.date));

    // Calculate Summary Stats
    const total = filtered.length;
    const completed = filtered.filter(s => s.status === '投稿完了').length;
    const waiting = filtered.filter(s => s.status === '投稿待ち').length; // or '承認待ち' etc? User asked for "承認待ち"?
    // User request: "投稿完了10中2件20％、承認待ち3件30％"
    // Let's count specific statuses.
    const approved = filtered.filter(s => s.status === '承認待ち').length;

    // Update Title with Summary
    // We need a place to put this. Let's append to panel-title or create a summary div.
    const titleEl = document.querySelector('#panel-schedule .panel-title');
    if (titleEl) {
        // Calculate percentages
        const completedPct = total > 0 ? Math.round((completed / total) * 100) : 0;
        const approvedPct = total > 0 ? Math.round((approved / total) * 100) : 0;

        titleEl.innerHTML = `
            進行管理 
            <span style="font-size:12px; font-weight:normal; margin-left:15px; color:#666;">
                投稿完了: <span style="font-weight:bold; color:#43A047;">${completed}/${total}件 (${completedPct}%)</span>
                <span style="margin:0 10px; color:#ccc;">|</span>
                承認待ち: <span style="font-weight:bold; color:#0D47A1;">${approved}/${total}件 (${approvedPct}%)</span>
            </span>
        `;
    }

    filtered.forEach(item => {
        const row = document.createElement('div');
        row.className = 'table-row';
        row.onclick = () => openEditor(item);

        // Status Style
        let stColor = '#eee', stText = '#333';
        if (item.status === '投稿完了') { stColor = '#43A047'; stText = 'white'; }
        if (item.status === '投稿待ち') { stColor = '#039BE5'; stText = 'white'; }
        if (item.status === '承認待ち') { stColor = '#1976D2'; stText = 'white'; } // Added based on context
        if (item.status === '構成中') { stColor = '#FFECB3'; stText = '#555'; } // Planning

        // Thumbnail
        let thumbHtml = `<div class="thumb-placeholder"></div>`;
        if (item.image) {
            thumbHtml = `<img src="${item.image}" class="thumb-placeholder" alt="">`;
        }

        // Text Preview
        let textPrev = item.text ? item.text.substring(0, 20) + "..." : `<span style="color:#aaa;">(未設定)</span>`;

        row.innerHTML = `
            <div>${item.date}</div>
            <div style="color:#555;">${item.time}</div>
            <div style="color:#555;">${item.category}</div>
            <div class="content-cell">
                ${thumbHtml}
                <span>${textPrev}</span>
            </div>
            <div style="text-align:center;">
                <span class="status-badge" style="background:${stColor}; color:${stText};">${item.status}</span>
            </div>
            <div style="text-align:center; color:#555;">✏️</div>
        `;
        list.appendChild(row);
    });
}

function switchMonth(offset) {
    const current = new Date(APP_STATE.currentMonthFilter + "-01");
    current.setMonth(current.getMonth() + offset);
    const y = current.getFullYear();
    const m = String(current.getMonth() + 1).padStart(2, '0');
    APP_STATE.currentMonthFilter = `${y}-${m}`;


    document.getElementById('display-month').textContent = `${y}年${m}月`;
    renderSchedule();
}

// --- Image Tags Data ---
const IMAGE_TAGS = {}; // Key: src, Value: Array of strings

// --- Modals & Editor ---

function setupModals() {
    // Add Plan Modal
    document.getElementById('btn-add-plan').onclick = () => {
        document.getElementById('modal-plan').style.display = 'flex';
    };
    document.getElementById('btn-close-plan').onclick = () => {
        document.getElementById('modal-plan').style.display = 'none';
    };
    document.getElementById('btn-save-plan').onclick = saveNewPlan;

    // AI Tagging (Material Tab)
    const btnTag = document.getElementById('btn-auto-tag');
    if (btnTag) {
        btnTag.onclick = () => {
            btnTag.textContent = "解析中...";
            btnTag.disabled = true;
            setTimeout(() => {
                LOCAL_IMAGES.forEach(src => {
                    // Dummy tagging logic
                    const tags = [];
                    if (Math.random() > 0.5) tags.push("施術");
                    if (Math.random() > 0.7) tags.push("笑顔");
                    if (Math.random() > 0.6) tags.push("内観");
                    if (tags.length === 0) tags.push("風景");
                    IMAGE_TAGS[src] = tags;
                });
                renderMaterials(); // Re-render to show tags
                btnTag.textContent = "🏷️ AIでタグ付与 (完了)";
                btnTag.disabled = false;
                setTimeout(() => btnTag.textContent = "🏷️ AIでタグ付与", 2000);
            }, 1500);
        };
    }

    // AI Text Gen Modal (Text Tab)
    const btnTextGen = document.getElementById('btn-text-gen-modal');
    if (btnTextGen) {
        btnTextGen.onclick = () => {
            document.getElementById('modal-text-gen').style.display = 'flex';
        };
    }
    document.getElementById('btn-close-text-gen').onclick = () => {
        document.getElementById('modal-text-gen').style.display = 'none';
    };
    document.getElementById('btn-run-text-gen').onclick = async () => {
        const btn = document.getElementById('btn-run-text-gen');
        const cat = document.getElementById('gen-text-cat').value;
        const resultsArea = document.getElementById('ai-gen-results-area');
        const optionsContainer = document.getElementById('ai-gen-options');
        const saveBtn = document.getElementById('btn-save-generated-text');

        btn.textContent = "生成中...";
        btn.disabled = true;

        await new Promise(r => setTimeout(r, 1500));

        // Generate 3 Options
        const options = [
            {
                title: `【${cat}】提案A: 親しみやすい`,
                content: `AIが作成した${cat}向けの投稿案Aです。\n親しみやすいトーンで書いています。\n\n#${cat} #親近感`
            },
            {
                title: `【${cat}】提案B: 専門的・信頼`,
                content: `AIが作成した${cat}向けの投稿案Bです。\n専門用語を交えて信頼感を高めています。\n\n#${cat} #プロフェッショナル`
            },
            {
                title: `【${cat}】提案C: シンプル・短文`,
                content: `AIが作成した${cat}向けの投稿案Cです。\n要点を絞って端的に伝えます。\n\n#${cat} #シンプル`
            }
        ];

        optionsContainer.innerHTML = '';
        currentGenOptions = options; // Global or closure var

        options.forEach((opt, idx) => {
            const card = document.createElement('div');
            card.className = 'ai-option-card';
            card.innerHTML = `<h5>${opt.title}</h5><p>${opt.content}</p>`;
            card.onclick = () => {
                document.querySelectorAll('.ai-option-card').forEach(c => c.classList.remove('selected'));
                card.classList.add('selected');
                selectedGenOption = opt;
                saveBtn.style.display = 'inline-block';
            };
            optionsContainer.appendChild(card);
        });

        resultsArea.style.display = 'block';
        btn.textContent = "再生成する";
        btn.disabled = false;
    };

    document.getElementById('btn-save-generated-text').onclick = () => {
        if (selectedGenOption) {
            const newTemplate = {
                title: selectedGenOption.title,
                content: selectedGenOption.content,
                usageCount: 0,
                lastUsed: "-"
            };
            TEXT_TEMPLATES.unshift(newTemplate);
            renderTexts();
            document.getElementById('modal-text-gen').style.display = 'none';
            // Reset modal state
            document.getElementById('ai-gen-results-area').style.display = 'none';
            document.getElementById('btn-save-generated-text').style.display = 'none';
            document.getElementById('btn-run-text-gen').textContent = "生成する";
            selectedGenOption = null;
        }
    };

    // Image Tagging Modal
    document.getElementById('btn-close-tag-modal').onclick = () => {
        document.getElementById('modal-img-tag').style.display = 'none';
    };

    document.getElementById('btn-add-tag').onclick = () => {
        const input = document.getElementById('new-tag-input');
        const val = input.value.trim();
        if (val && currentTaggingImage) {
            if (!IMAGE_TAGS[currentTaggingImage]) IMAGE_TAGS[currentTaggingImage] = [];
            IMAGE_TAGS[currentTaggingImage].push(val);
            renderTagChips(currentTaggingImage);
            input.value = '';
            renderMaterials(); // Update grid
        }
    };

    // Editor Modal
    document.getElementById('btn-close-editor').onclick = () => {
        document.getElementById('modal-editor').style.display = 'none';
    };
    document.getElementById('btn-save-editor').onclick = saveEditorContent;

    // Category Change Listener -> Recommendation Logic & Auto Update
    const catSelect = document.getElementById('editor-category-select');
    if (catSelect) {
        catSelect.addEventListener('change', (e) => {
            renderEditorSelectors(e.target.value);
            // Auto Update Logic: Pick the newly sorted top items
            // We need to wait for renderEditorSelectors to finish dom manipulation? No, it's distinct.
            // Actually renderEditorSelectors just fills the list. We need to manually pick top.

            const topImg = document.querySelector('.editor-img-item.recommend img');
            const topText = document.querySelector('.editor-txt-item'); // First text item (sorted)

            let newImg = topImg ? topImg.src : null;
            let newText = topText && TEXT_TEMPLATES.find(t => t.title === topText.textContent) ? TEXT_TEMPLATES.find(t => t.title === topText.textContent).content : null;

            if (newImg) {
                document.querySelectorAll('.editor-img-item').forEach(i => i.classList.remove('selected'));
                if (topImg) topImg.parentElement.classList.add('selected');
            }
            if (newText) {
                document.querySelectorAll('.editor-txt-item').forEach(i => i.classList.remove('selected'));
                if (topText) topText.classList.add('selected');
            }

            updateEditorPreview(newImg, newText);
        });
    }

    // AI Text Gen (Inline)
    document.getElementById('btn-gen-text').onclick = async () => {
        const btn = document.getElementById('btn-gen-text');
        const prompt = document.getElementById('ai-text-prompt').value;
        if (!prompt) return alert("プロンプトを入力してください");

        btn.textContent = "生成中...";
        btn.disabled = true;

        // Mock latency
        await new Promise(r => setTimeout(r, 1500));

        const generated = `【AI自動生成】\n${prompt}に関してのお知らせです！\n\n春の陽気が心地よい季節になりましたね🌸\n当院では皆様の健康を第一に考え、新しいキャンペーンを開始します。\n\nぜひこの機会にお越しください！✨\n#整骨院 #健康 #キャンペーン`;

        tempEditorState.text = generated;
        document.getElementById('editor-preview-text').value = generated;

        btn.textContent = "✨ AIで文章を作成";
        btn.disabled = false;
    };

    // Overlay Mock
    document.getElementById('btn-apply-overlay').onclick = () => {
        const overlay = document.getElementById('editor-overlay-mock');
        const cat = document.getElementById('editor-category-select').value || "お知らせ";

        // Simple mock of text content based on category
        overlay.querySelector('.overlay-title').textContent = cat;
        overlay.querySelector('.overlay-sub').textContent = "今だけ限定特典あり！";

        overlay.style.display = 'block';
    };

    window.onclick = (e) => {
        if (e.target.className.includes('modal-overlay')) {
            e.target.style.display = 'none';
        }
    }
}

function renderMaterials() {
    const grid = document.getElementById('material-grid');
    grid.innerHTML = '';

    LOCAL_IMAGES.forEach((src, idx) => {
        const div = document.createElement('div');
        div.className = 'material-card';

        // Fake Usage Stats
        const usageCount = Math.floor(Math.random() * 10);
        const lastDate = usageCount > 0 ? `2026-01-${10 + Math.floor(Math.random() * 15)}` : '-';

        // Check tags
        let tagHtml = '';
        if (IMAGE_TAGS[src] && IMAGE_TAGS[src].length > 0) {
            tagHtml = `<div class="img-tag-badge" style="display:block;">${IMAGE_TAGS[src][0]} +${IMAGE_TAGS[src].length - 1}</div>`;
        }

        div.innerHTML = `
            <img src="${src}" loading="lazy">
            ${tagHtml}
            <div class="mat-footer">
                <div style="font-weight:bold; margin-bottom:2px;">image_${idx + 1}.jpg</div>
                <div style="font-size:9px; color:#888;">使用: ${usageCount}回 (最終: ${lastDate})</div>
            </div>
        `;
        // Click to Tag
        div.onclick = () => {
            openTagModal(src);
        };
        grid.appendChild(div);
    });
}

function renderTexts() {
    const list = document.getElementById('text-list');
    list.innerHTML = '';

    TEXT_TEMPLATES.forEach(t => {
        const item = document.createElement('div');
        item.className = 'text-card';
        item.innerHTML = `
            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                <h4>${t.title}</h4>
                <div style="font-size:10px; color:#888; text-align:right;">
                    <div>使用回数: ${t.usageCount || 0}回</div>
                    <div>最終: ${t.lastUsed || '-'}</div>
                </div>
            </div>
            <p>${t.content.replace(/\n/g, '<br>')}</p>
        `;
        list.appendChild(item);
    });
}

function renderCompetitors() {
    const container = document.getElementById('comp-columns-container');
    if (!container) return;
    container.innerHTML = '';

    COMPETITOR_DATA.forEach(acc => {
        const col = document.createElement('div');
        col.className = 'comp-col';

        let html = `
            <div class="comp-cell" style="height:60px; padding:5px;">
                <div class="account-header" style="justify-content:center; text-align:left;">
                     <div style="width:30px; height:30px; background:#ddd; border-radius:50%; margin-right:5px;"></div>
                     <div>
                        <div style="font-size:10px; font-weight:bold; line-height:1.2;">${acc.name.substring(0, 15)}...</div>
                        <div style="font-size:9px; color:#0095F6;">${acc.account_id}</div>
                     </div>
                </div>
            </div>
            <div class="comp-cell">${acc.posts_per_month}投稿/直近1ヶ月</div>
            <div class="comp-cell">${acc.followers}</div>
            <div class="comp-cell">${acc.following}</div>
            <div class="comp-cell large">${acc.description}</div>
            <div class="comp-cell"><a href="#" style="color:#0095F6; font-size:10px; word-break:break-all;">${acc.url}</a></div>
            <div class="comp-cell" style="font-size:16px;">${acc.recent_likes_total}</div>
            <div class="comp-cell huge">
                ${acc.recent_posts.map(p => `
                    <div class="mock-post-card" style="height:32%; margin-bottom:2%;">
                         <div class="mp-header">
                            <div class="mp-icon"></div>
                            <div class="mp-name">${acc.account_id}</div>
                            <div style="margin-left:auto; color:#0095F6; font-size:10px;">プロフィールを表示</div>
                         </div>
                         <div class="mp-img-box"><img src="${p.img}" onerror="this.src='//via.placeholder.com/150'"></div>
                         <div class="mp-actions">♡ 💬 ➤</div>
                         <div class="mp-likes">「いいね！」: ${p.likes}件</div>
                         <div class="mp-caption"><b>${acc.account_id.split('@')[1] || 'user'}</b> ${p.caption}</div>
                    </div>
                `).join('')}
            </div>
        `;

        col.innerHTML = html;
        container.appendChild(col);
    });
}

function saveNewPlan() {
    const date = document.getElementById('plan-date').value;
    const cat = document.getElementById('plan-category').value;

    if (!date) return alert("日付を選択してください");

    SCHEDULES.push({
        id: Date.now(),
        date: date,
        time: "10:00",
        category: cat,
        status: "構成中",
        image: "",
        text: ""
    });

    document.getElementById('modal-plan').style.display = 'none';
    if (!date.startsWith(APP_STATE.currentMonthFilter)) {
        APP_STATE.currentMonthFilter = date.substring(0, 7);
        const [y, m] = date.split('-');
        document.getElementById('display-month').textContent = `${y}年${m}月`;
    }
    renderSchedule();
}

function openEditor(item) {
    if (item.status === '投稿完了') return;

    APP_STATE.selectedScheduleId = item.id;
    document.getElementById('modal-editor').style.display = 'flex';

    // Reset inputs
    document.getElementById('editor-overlay-mock').style.display = 'none';
    document.getElementById('ai-text-prompt').value = "";

    // Set Info
    document.getElementById('editor-status-display').textContent = item.status;
    const catSelect = document.getElementById('editor-category-select');
    if (catSelect) catSelect.value = item.category || "日常・風景";

    // Render Selection Grids with sorting/recommendation
    renderEditorSelectors(item.category);

    // Set current preview
    updateEditorPreview(item.image, item.text);
}

function renderEditorSelectors(category) {
    // Images
    const imgContainer = document.getElementById('editor-img-list');
    imgContainer.innerHTML = '';

    // Mock Recommendation: prioritize different images based on category length
    // (Truly random mock logic for demo purposes)
    const sortedImages = [...LOCAL_IMAGES].sort((a, b) => {
        if (category === "スタッフ紹介") return a.includes('sw') ? -1 : 1;
        return Math.random() - 0.5;
    });

    sortedImages.forEach((src, idx) => {
        const div = document.createElement('div');
        div.className = 'editor-img-item';
        // Mark first 2 as recommend
        if (idx < 2) div.classList.add('recommend');

        const img = document.createElement('img');
        img.src = src;
        img.style.width = "100%"; img.style.height = "100%"; img.style.objectFit = "cover";

        div.appendChild(img);
        div.onclick = () => {
            document.querySelectorAll('.editor-img-item').forEach(i => i.classList.remove('selected'));
            div.classList.add('selected');
            updateEditorPreview(src, null);
        };
        imgContainer.appendChild(div);
    });

    // Texts
    const txtContainer = document.getElementById('editor-txt-list');
    txtContainer.innerHTML = '';

    // Filter templates based on category (fuzzy match)
    const sortedTexts = [...TEXT_TEMPLATES].sort((a, b) => {
        const aScore = a.title.includes(category.substring(0, 2)) ? 1 : 0;
        const bScore = b.title.includes(category.substring(0, 2)) ? 1 : 0;
        return bScore - aScore;
    });

    sortedTexts.forEach(t => {
        const div = document.createElement('div');
        div.className = 'editor-txt-item';
        div.textContent = t.title;
        div.onclick = () => {
            document.querySelectorAll('.editor-txt-item').forEach(i => i.classList.remove('selected'));
            div.classList.add('selected');
            updateEditorPreview(null, t.content);
        };
        txtContainer.appendChild(div);
    });
}

let tempEditorState = { image: "", text: "" };

function updateEditorPreview(img, txt) {
    if (img !== null) tempEditorState.image = img;
    if (txt !== null) tempEditorState.text = txt;

    const previewImg = document.getElementById('editor-preview-img');
    const placeholder = document.getElementById('preview-placeholder');
    const textArea = document.getElementById('editor-preview-text');

    if (tempEditorState.image) {
        previewImg.src = tempEditorState.image;
        previewImg.style.display = 'block';
        placeholder.style.display = 'none';
        document.getElementById('editor-preview-container').style.background = 'transparent';
    } else {
        previewImg.style.display = 'none';
        placeholder.style.display = 'block';
        document.getElementById('editor-preview-container').style.background = '#eee';
    }

    if (tempEditorState.text) {
        textArea.value = tempEditorState.text;
    }
}

function saveEditorContent() {
    const item = SCHEDULES.find(s => s.id === APP_STATE.selectedScheduleId);
    if (item) {
        if (tempEditorState.image) item.image = tempEditorState.image;

        // Get text from textarea (possibly edited manually)
        const currentText = document.getElementById('editor-preview-text').value;
        if (currentText) item.text = currentText;

        const catSelect = document.getElementById('editor-category-select');
        if (catSelect) item.category = catSelect.value;

        if (item.image && item.text) {
            item.status = '投稿待ち';
        }

        renderSchedule();
        document.getElementById('modal-editor').style.display = 'none';
    }
}

function showPreview(item) {
    // Only update if current tab is schedule? or always?
}

// Variables for AI Gen
let selectedGenOption = null;
let currentGenOptions = [];

// Tagging Logic
let currentTaggingImage = null;

function openTagModal(src) {
    currentTaggingImage = src;
    document.getElementById('tag-target-img').src = src;
    document.getElementById('modal-img-tag').style.display = 'flex';
    renderTagChips(src);
}

function renderTagChips(src) {
    const area = document.getElementById('current-tags-area');
    area.innerHTML = '';
    const tags = IMAGE_TAGS[src] || [];

    if (tags.length === 0) {
        area.innerHTML = '<span style="color:#ccc; font-size:11px;">タグはまだありません</span>';
        return;
    }

    tags.forEach((tag, idx) => {
        const chip = document.createElement('span');
        chip.className = 'tag-chip selected';
        chip.style.fontSize = '10px';
        chip.textContent = tag + " ✕";
        chip.onclick = () => {
            // Remove tag
            tags.splice(idx, 1);
            renderTagChips(src);
            renderMaterials();
        };
        area.appendChild(chip);
    });
}

// Editor Tab Switcher
function switchTextTab(tabName) {
    document.querySelectorAll('.text-tab').forEach(t => t.classList.remove('active'));
    document.getElementById(`tab-txt-${tabName}`).classList.add('active');

    document.getElementById('content-txt-material').style.display = 'none';
    document.getElementById('content-txt-ai').style.display = 'none';

    document.getElementById(`content-txt-${tabName}`).style.display = 'block';
}


// --- Client Switching Logic ---


