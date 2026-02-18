// designer.js - Slide Layout Designer 機能実装

const DPI = 96;
const SLIDE_INCH_WIDTH = 12.8;
const SLIDE_INCH_HEIGHT = 7.2;

let canvas = document.getElementById('slideCanvas');
let ctx = canvas.getContext('2d');

// キャンバスサイズをインチからピクセルに設定
const pixelWidth = SLIDE_INCH_WIDTH * DPI;
const pixelHeight = SLIDE_INCH_HEIGHT * DPI;
canvas.width = pixelWidth;
canvas.height = pixelHeight;

let objects = [];
let selectedObject = null;
let draggingObject = null;
let dragOffsetX = 0;
let dragOffsetY = 0;
let isCreatingNew = null; // "box", "arrow", or null

// ==================== オブジェクト管理 ====================

class SlideObject {
    constructor(type, left, top, width, height) {
        this.id = Math.random().toString(36).substr(2, 9);
        this.type = type; // "box", "arrow", "text"
        this.left = left;
        this.top = top;
        this.width = width;
        this.height = height;
        this.text = '';
        this.fillColor = '#FFFFFF';
        this.fontColor = '#000000';
        this.fontSize = 12;
        this.halign = 'center';
        this.valign = 'middle';
    }

    inchToPixel(inch) {
        return inch * DPI;
    }

    pixelToInch(pixel) {
        return (pixel / DPI).toFixed(3);
    }

    getPixelCoords() {
        return {
            x: this.inchToPixel(this.left),
            y: this.inchToPixel(this.top),
            w: this.inchToPixel(this.width),
            h: this.inchToPixel(this.height)
        };
    }

    hitTest(px, py) {
        const coords = this.getPixelCoords();
        return px >= coords.x && px <= coords.x + coords.w &&
               py >= coords.y && py <= coords.y + coords.h;
    }

    draw(ctx, selected = false) {
        const coords = this.getPixelCoords();
        const isArrow = this.type.startsWith('arrow');
        
        if (this.type === 'box') {
            // 背景
            ctx.fillStyle = this.fillColor;
            ctx.fillRect(coords.x, coords.y, coords.w, coords.h);
            
            // ボーダー
            ctx.strokeStyle = selected ? '#4472C4' : '#ccc';
            ctx.lineWidth = selected ? 3 : 1;
            ctx.strokeRect(coords.x, coords.y, coords.w, coords.h);
            
            // テキスト
            if (this.text) {
                ctx.fillStyle = this.fontColor;
                ctx.font = `${this.fontSize}px Arial`;
                
                // 水平配置
                if (this.halign === 'left') {
                    ctx.textAlign = 'left';
                } else if (this.halign === 'right') {
                    ctx.textAlign = 'right';
                } else {
                    ctx.textAlign = 'center';
                }
                
                // 垂直配置
                ctx.textBaseline = this.valign === 'middle' ? 'middle' : (this.valign === 'top' ? 'top' : 'bottom');
                
                const textX = this.halign === 'left' 
                    ? coords.x + 5
                    : (this.halign === 'right' ? coords.x + coords.w - 5 : coords.x + coords.w / 2);
                
                const textY = this.valign === 'middle' 
                    ? coords.y + coords.h / 2
                    : (this.valign === 'top' ? coords.y + 5 : coords.y + coords.h - 5);
                
                // 複数行テキスト対応
                const lines = this.text.split('\n');
                const lineHeight = this.fontSize + 4;
                const totalHeight = lines.length * lineHeight;
                let startY = textY - totalHeight / 2;
                
                lines.forEach((line, idx) => {
                    ctx.fillText(line, textX, startY + idx * lineHeight);
                });
            }
        } else if (isArrow) {
            // 矢印を描画（方向あり）
            const direction = this.type.split('-')[1] || 'right';
            drawArrow(ctx, coords.x, coords.y, coords.w, coords.h, this.fillColor, direction, selected);
        } else if (this.type === 'line') {
            // 直線
            ctx.strokeStyle = this.fillColor;
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(coords.x, coords.y + coords.h / 2);
            ctx.lineTo(coords.x + coords.w, coords.y + coords.h / 2);
            ctx.stroke();
            
            if (selected) {
                ctx.strokeStyle = '#4472C4';
                ctx.lineWidth = 2;
                ctx.setLineDash([4, 4]);
                ctx.strokeRect(coords.x, coords.y, coords.w, coords.h);
                ctx.setLineDash([]);
            }
        } else if (this.type === 'circle') {
            // 円
            ctx.fillStyle = this.fillColor;
            const radius = Math.min(coords.w, coords.h) / 2;
            ctx.beginPath();
            ctx.arc(coords.x + coords.w / 2, coords.y + coords.h / 2, radius, 0, Math.PI * 2);
            ctx.fill();
            
            ctx.strokeStyle = selected ? '#4472C4' : '#ccc';
            ctx.lineWidth = selected ? 2 : 1;
            ctx.stroke();
        } else if (this.type === 'text') {
            // テキストボックス（背景なし）
            ctx.fillStyle = this.fontColor;
            ctx.font = `${this.fontSize}px Arial`;
            ctx.textAlign = 'left';
            ctx.textBaseline = 'top';
            
            const lines = this.text.split('\n');
            lines.forEach((line, idx) => {
                ctx.fillText(line, coords.x, coords.y + idx * (this.fontSize + 2));
            });
            
            if (selected) {
                ctx.strokeStyle = '#4472C4';
                ctx.lineWidth = 2;
                ctx.strokeRect(coords.x, coords.y, coords.w, coords.h);
            }
        }
        
        // リサイズハンドル
        if (selected) {
            drawResizeHandles(ctx, coords);
        }
    }
}

function drawArrow(ctx, x, y, width, height, color, direction = 'right', selected = false) {
    const arrowSize = 10;
    
    ctx.fillStyle = color;
    ctx.beginPath();
    
    if (direction === 'right') {
        // 右矢印
        ctx.rect(x, y + height / 2 - 3, width - arrowSize, 6);
        ctx.moveTo(x + width - arrowSize, y);
        ctx.lineTo(x + width, y + height / 2);
        ctx.lineTo(x + width - arrowSize, y + height);
    } else if (direction === 'left') {
        // 左矢印
        ctx.rect(x + arrowSize, y + height / 2 - 3, width - arrowSize, 6);
        ctx.moveTo(x + arrowSize, y);
        ctx.lineTo(x, y + height / 2);
        ctx.lineTo(x + arrowSize, y + height);
    } else if (direction === 'up') {
        // 上矢印
        ctx.rect(x + width / 2 - 3, y + arrowSize, 6, height - arrowSize);
        ctx.moveTo(x, y + arrowSize);
        ctx.lineTo(x + width / 2, y);
        ctx.lineTo(x + width, y + arrowSize);
    } else if (direction === 'down') {
        // 下矢印
        ctx.rect(x + width / 2 - 3, y, 6, height - arrowSize);
        ctx.moveTo(x, y + height - arrowSize);
        ctx.lineTo(x + width / 2, y + height);
        ctx.lineTo(x + width, y + height - arrowSize);
    }
    
    ctx.fill();
    
    if (selected) {
        ctx.strokeStyle = '#4472C4';
        ctx.lineWidth = 2;
        ctx.strokeRect(x, y, width, height);
    }
}

function drawResizeHandles(ctx, coords) {
    const handleSize = 6;
    ctx.fillStyle = '#4472C4';
    
    const corners = [
        [coords.x, coords.y],
        [coords.x + coords.w, coords.y],
        [coords.x, coords.y + coords.h],
        [coords.x + coords.w, coords.y + coords.h]
    ];
    
    corners.forEach(([posX, posY]) => {
        ctx.fillRect(posX - handleSize / 2, posY - handleSize / 2, handleSize, handleSize);
    });
}

// ==================== キャンバスイベント ====================

canvas.addEventListener('mousedown', (e) => {
    const rect = canvas.getBoundingClientRect();
    const px = e.clientX - rect.left;
    const py = e.clientY - rect.top;
    
    if (isCreatingNew) {
        // 新規オブジェクト作成モード
        const obj = new SlideObject(
            isCreatingNew,
            (px / DPI).toFixed(3),
            (py / DPI).toFixed(3),
            1.0,
            0.5
        );
        objects.push(obj);
        selectObject(obj);
        isCreatingNew = null;
        canvas.style.cursor = 'default';
        redraw();
        return;
    }
    
    // 既存オブジェクトを選択または移動開始
    for (let i = objects.length - 1; i >= 0; i--) {
        if (objects[i].hitTest(px, py)) {
            selectObject(objects[i]);
            draggingObject = objects[i];
            dragOffsetX = px - objects[i].getPixelCoords().x;
            dragOffsetY = py - objects[i].getPixelCoords().y;
            redraw();
            return;
        }
    }
    
    // 何もない場所をクリック
    selectedObject = null;
    updatePropertyPanel();
    redraw();
});

canvas.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    const px = e.clientX - rect.left;
    const py = e.clientY - rect.top;
    
    if (isCreatingNew) {
        canvas.style.cursor = 'crosshair';
        return;
    }
    
    if (draggingObject) {
        draggingObject.left = parseFloat(((px - dragOffsetX) / DPI).toFixed(3));
        draggingObject.top = parseFloat(((py - dragOffsetY) / DPI).toFixed(3));
        
        // 境界チェック
        draggingObject.left = Math.max(0, Math.min(draggingObject.left, SLIDE_INCH_WIDTH - draggingObject.width));
        draggingObject.top = Math.max(0, Math.min(draggingObject.top, SLIDE_INCH_HEIGHT - draggingObject.height));
        
        updatePropertyPanel();
        redraw();
        return;
    }
    
    // ホバーチェック
    for (let obj of objects) {
        if (obj.hitTest(px, py)) {
            canvas.style.cursor = 'move';
            return;
        }
    }
    canvas.style.cursor = 'default';
});

canvas.addEventListener('mouseup', () => {
    draggingObject = null;
});

// ==================== UI コントロール ====================

document.getElementById('btnAddBox').addEventListener('click', () => {
    isCreatingNew = 'box';
    canvas.style.cursor = 'crosshair';
});

document.getElementById('btnAddArrowRight').addEventListener('click', () => {
    isCreatingNew = 'arrow-right';
    canvas.style.cursor = 'crosshair';
});

document.getElementById('btnAddArrowLeft').addEventListener('click', () => {
    isCreatingNew = 'arrow-left';
    canvas.style.cursor = 'crosshair';
});

document.getElementById('btnAddLine').addEventListener('click', () => {
    isCreatingNew = 'line';
    canvas.style.cursor = 'crosshair';
});

document.getElementById('btnAddCircle').addEventListener('click', () => {
    isCreatingNew = 'circle';
    canvas.style.cursor = 'crosshair';
});

document.getElementById('btnAddText').addEventListener('click', () => {
    isCreatingNew = 'text';
    canvas.style.cursor = 'crosshair';
});

document.getElementById('btnClear').addEventListener('click', () => {
    if (confirm('すべてのオブジェクトを削除しますか？')) {
        objects = [];
        selectedObject = null;
        updatePropertyPanel();
        redraw();
    }
});

// ==================== フォントサイズプリセット ====================

document.getElementById('btnFontSize9').addEventListener('click', () => {
    setFontSize(9);
});

document.getElementById('btnFontSize12').addEventListener('click', () => {
    setFontSize(12);
});

document.getElementById('btnFontSize14').addEventListener('click', () => {
    setFontSize(14);
});

// ==================== オブジェクト選択 ====================

function selectObject(obj) {
    selectedObject = obj;
    updatePropertyPanel();
    redraw();
}

function updatePropertyPanel() {
    const props = document.getElementById('objectProperties');
    
    if (!selectedObject) {
        props.style.display = 'none';
        return;
    }
    
    props.style.display = 'block';
    
    // テキスト内容フィールド
    const textGroup = document.getElementById('textContentGroup');
    if (selectedObject.type !== 'arrow-left' && selectedObject.type !== 'arrow-right' && selectedObject.type !== 'arrow-up' && selectedObject.type !== 'arrow-down' && selectedObject.type !== 'line' && selectedObject.type !== 'circle') {
        textGroup.style.display = 'block';
        document.getElementById('objText').value = selectedObject.text;
    } else {
        textGroup.style.display = 'none';
    }
    
    // 位置・サイズ
    document.getElementById('objLeft').value = selectedObject.left;
    document.getElementById('objTop').value = selectedObject.top;
    document.getElementById('objWidth').value = selectedObject.width;
    document.getElementById('objHeight').value = selectedObject.height;
    
    // 色
    document.getElementById('objFillColor').value = selectedObject.fillColor;
    document.getElementById('objFontColor').value = selectedObject.fontColor;
    
    // フォント
    document.getElementById('objFontSize').value = selectedObject.fontSize;
    document.getElementById('objHalign').value = selectedObject.halign || 'center';
    document.getElementById('objValign').value = selectedObject.valign || 'middle';
    
    // イベントリスナー更新
    updatePropertyInputs();
}

function updatePropertyInputs() {
    if (!selectedObject) return;
    
    ['objText', 'objLeft', 'objTop', 'objWidth', 'objHeight', 'objFillColor', 'objFontColor', 'objFontSize', 'objHalign', 'objValign']
        .forEach(id => {
            const el = document.getElementById(id);
            el.onchange = () => {
                if (id === 'objText') selectedObject.text = el.value;
                if (id === 'objLeft') selectedObject.left = parseFloat(el.value);
                if (id === 'objTop') selectedObject.top = parseFloat(el.value);
                if (id === 'objWidth') selectedObject.width = parseFloat(el.value);
                if (id === 'objHeight') selectedObject.height = parseFloat(el.value);
                if (id === 'objFillColor') selectedObject.fillColor = el.value;
                if (id === 'objFontColor') selectedObject.fontColor = el.value;
                if (id === 'objFontSize') selectedObject.fontSize = parseInt(el.value);
                if (id === 'objHalign') selectedObject.halign = el.value;
                if (id === 'objValign') selectedObject.valign = el.value;
                redraw();
            };
        });
    
    document.getElementById('btnDeleteObject').onclick = () => {
        const idx = objects.indexOf(selectedObject);
        if (idx > -1) {
            objects.splice(idx, 1);
            selectedObject = null;
            updatePropertyPanel();
            redraw();
        }
    };
}

function setColor(color) {
    if (selectedObject && selectedObject.type !== 'arrow') {
        selectedObject.fontColor = color;
    } else if (selectedObject && selectedObject.type.startsWith('arrow')) {
        selectedObject.fillColor = color;
    }
    updatePropertyPanel();
    redraw();
}

function setFontSize(size) {
    if (selectedObject && (selectedObject.type === 'text' || selectedObject.type === 'box')) {
        selectedObject.fontSize = size;
        document.getElementById('objFontSize').value = size;
        redraw();
    }
}

// ==================== JSON エクスポート ====================

document.getElementById('btnExportJSON').addEventListener('click', () => {
    const data = {
        title: document.getElementById('slideTitle').value,
        subtitle: document.getElementById('slideSubtitle').value,
        slideIndex: 1,
        objects: objects.map(obj => {
            const objData = {
                type: obj.type,
                left: obj.left,
                top: obj.top,
                width: obj.width,
                height: obj.height,
                fillColor: obj.fillColor,
                fontSize: obj.fontSize,
                valign: obj.valign
            };
            
            // テキスト内容を追加（text, box のみ）
            if (obj.type === 'text' || obj.type === 'box') {
                objData.text = obj.text;
                objData.fontColor = obj.fontColor;
            }
            
            // arrow の場合は方向を分離
            if (obj.type.startsWith('arrow')) {
                objData.type = 'arrow';
                objData.direction = obj.type.split('-')[1] || 'right';
            }
            
            return objData;
        })
    };
    
    fetch('/api/export-json', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(result => {
        if (result.success) {
            document.getElementById('jsonOutput').value = result.jsonString;
            
            // ダウンロードリンク設定
            const jsonBlob = new Blob([result.jsonString], { type: 'application/json' });
            const url = URL.createObjectURL(jsonBlob);
            document.getElementById('jsonDownload').href = url;
            document.getElementById('jsonDownload').download = '01_content.json';
        }
    });
});

document.getElementById('btnCopyJSON').addEventListener('click', () => {
    const textarea = document.getElementById('jsonOutput');
    if (textarea.value) {
        textarea.select();
        document.execCommand('copy');
        alert('JSON をコピーしました！');
    }
});

// ==================== スクリーンショット ====================

document.getElementById('btnScreenshot').addEventListener('click', async () => {
    const btn = document.getElementById('btnScreenshot');
    btn.disabled = true;
    btn.textContent = '📸 撮影中...';
    
    try {
        const result = await captureCanvasScreenshot();
        if (result.success) {
            alert(`✅ スクリーンショットを保存しました\n\nファイル: ${result.filename}`);
            btn.textContent = '📸 スクリーンショット';
        } else {
            alert(`❌ エラー: ${result.error}`);
        }
    } catch (err) {
        alert(`❌ エラー: ${err.message}`);
    }
    
    btn.disabled = false;
    btn.textContent = '📸 スクリーンショット';
});

// ==================== JSON インポート ====================

document.getElementById('btnLoadJSON').addEventListener('click', () => {
    const jsonText = document.getElementById('jsonInput').value.trim();
    if (!jsonText) {
        alert('JSON を入力してください');
        return;
    }
    
    fetch('/api/load-json', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ jsonString: jsonText })
    })
    .then(res => res.json())
    .then(result => {
        if (result.success) {
            // スライド情報を更新
            document.getElementById('slideTitle').value = result.title;
            document.getElementById('slideSubtitle').value = result.subtitle;
            
            // オブジェクト配列を再構築
            objects = [];
            result.objects.forEach((objData, index) => {
                const obj = new SlideObject(
                    objData.type,
                    objData.left,
                    objData.top,
                    objData.width,
                    objData.height
                );
                
                obj.fillColor = objData.fillColor || '#FFFFFF';
                obj.fontColor = objData.fontColor || '#000000';
                obj.fontSize = objData.fontSize || 12;
                obj.text = objData.text || '';
                obj.valign = objData.valign || 'middle';
                
                objects.push(obj);
            });
            
            selectedObject = null;
            updatePropertyPanel();
            redraw();
            alert('JSON を読込完了しました！');
        } else {
            alert('エラー: ' + (result.error || '不明なエラー'));
        }
    })
    .catch(err => {
        alert('通信エラー: ' + err.message);
    });
});

// ==================== レンダリング ====================

function redraw() {
    // 背景クリア
    ctx.fillStyle = '#f9f9f9';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // ガイドライン
    ctx.strokeStyle = '#e0e0e0';
    ctx.lineWidth = 0.5;
    
    // 縦ライン（0.5インチごと）
    for (let i = 0; i <= SLIDE_INCH_WIDTH; i += 0.5) {
        const x = i * DPI;
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
    }
    
    // 横ライン（0.5インチごと）
    for (let i = 0; i <= SLIDE_INCH_HEIGHT; i += 0.5) {
        const y = i * DPI;
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
    }
    
    // オブジェクト描画
    objects.forEach(obj => {
        obj.draw(ctx, obj === selectedObject);
    });
}

// 初期描画
redraw();

// ==================== AI操作用ユーティリティ ====================

/**
 * Canvas のスクリーンショットを取得（Base64 PNG）
 * 用途：AIが配置結果を視覚検証
 */
async function captureCanvasScreenshot() {
    try {
        const imageData = canvas.toDataURL('image/png');
        const response = await fetch('/api/canvas/screenshot', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ imageData: imageData })
        });
        
        const result = await response.json();
        if (result.success) {
            console.log('Screenshot saved:', result.filename);
            return {
                success: true,
                data: result.data,
                filename: result.filename,
                timestamp: result.timestamp
            };
        } else {
            console.error('Screenshot error:', result.error);
            return { success: false, error: result.error };
        }
    } catch (err) {
        console.error('Capture error:', err);
        return { success: false, error: err.message };
    }
}

/**
 * 複数オブジェクトを一度に追加
 * 用途：AIが複数オブジェクトを一度に配置
 */
async function addObjectsBatch(objectList) {
    try {
        // UI形式で受け取ったオブジェクトをキャンバスに追加
        objectList.forEach((objData, index) => {
            const obj = new SlideObject(
                objData.type,
                objData.left,
                objData.top,
                objData.width,
                objData.height
            );
            
            obj.fillColor = objData.fillColor || '#FFFFFF';
            obj.fontColor = objData.fontColor || '#000000';
            obj.fontSize = objData.fontSize || 12;
            obj.text = objData.text || '';
            obj.valign = objData.valign || 'middle';
            
            objects.push(obj);
        });
        
        updatePropertyPanel();
        redraw();
        
        return {
            success: true,
            count: objectList.length,
            totalObjects: objects.length
        };
    } catch (err) {
        console.error('Batch add error:', err);
        return { success: false, error: err.message };
    }
}

/**
 * 現在のレイアウトを JSON で出力
 * 用途：AIが配置結果を JSON 形式で取得
 */
async function exportLayoutJSON() {
    try {
        const data = {
            title: document.getElementById('slideTitle').value,
            subtitle: document.getElementById('slideSubtitle').value,
            slideIndex: 1,
            objects: objects.map(obj => {
                const objData = {
                    type: obj.type,
                    left: obj.left,
                    top: obj.top,
                    width: obj.width,
                    height: obj.height,
                    fillColor: obj.fillColor,
                    fontSize: obj.fontSize,
                    valign: obj.valign
                };
                
                if (obj.type === 'text' || obj.type === 'box') {
                    objData.text = obj.text;
                    objData.fontColor = obj.fontColor;
                }
                
                if (obj.type.startsWith('arrow')) {
                    objData.type = 'arrow';
                    objData.direction = obj.type.split('-')[1] || 'right';
                }
                
                return objData;
            })
        };
        
        const response = await fetch('/api/export-json', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        if (result.success) {
            return {
                success: true,
                json: result.json,
                jsonString: result.jsonString
            };
        } else {
            return { success: false, error: 'Export failed' };
        }
    } catch (err) {
        console.error('Export error:', err);
        return { success: false, error: err.message };
    }
}
