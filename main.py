<!DOCTYPE html>
<html lang="uz">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>YusufxonPro Premium</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        :root { --bg: #ffffff; --input-bg: #f2f2f7; --text: #000000; --sub: #8e8e93; --border: #e5e5ea; }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, sans-serif; }
        body { background: var(--bg); color: var(--text); overflow-x: hidden; }

        /* Loader */
        #sync-loader {
            position: fixed; inset: 0; background: #fff; z-index: 3000;
            display: none; flex-direction: column; justify-content: center; align-items: center;
        }
        .spinner { width: 50px; height: 50px; border: 4px solid #f3f3f3; border-top: 4px solid #000; border-radius: 50%; animation: spin 1s infinite linear; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }

        /* Banner */
        .banner {
            width: 100%; padding: 45px 20px; background: #000; color: #fff;
            text-align: center; border-radius: 0 0 35px 35px; margin-bottom: 25px;
        }
        .banner h1 { font-size: 28px; font-weight: 900; letter-spacing: 3px; }

        /* Login */
        #login-page { padding: 0 25px; display: none; }
        .input-group { margin-bottom: 15px; }
        .input-group label { display: block; font-size: 11px; font-weight: 700; color: var(--sub); margin-bottom: 6px; text-transform: uppercase; }
        input {
            width: 100%; padding: 18px; background: var(--input-bg); border: 1px solid var(--border);
            border-radius: 16px; font-size: 16px; outline: none; transition: 0.3s;
        }
        input:focus { border-color: #000; background: #fff; }

        /* App Layout */
        #app-layout { display: none; padding: 0 20px 100px; }
        .user-card {
            display: flex; align-items: center; gap: 15px; padding: 15px;
            background: var(--input-bg); border-radius: 20px; margin-bottom: 20px;
        }
        .avatar { width: 55px; height: 55px; border-radius: 50%; object-fit: cover; background: #000; }

        .cargo-card {
            background: #fff; border: 1px solid var(--border); border-radius: 25px;
            padding: 20px; margin-bottom: 15px; box-shadow: 0 5px 15px rgba(0,0,0,0.02);
        }
        .btn-del { width: 100%; padding: 12px; border-radius: 12px; border: none; background: #fff0f0; color: #ff3b30; font-weight: 700; margin-top: 10px; cursor: pointer; }

        /* FAB */
        .fab { position: fixed; bottom: 35px; right: 25px; width: 68px; height: 68px; background: #000; color: #fff; border-radius: 50%; border: none; font-size: 38px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); z-index: 100; }
    </style>
</head>
<body>

    <div id="sync-loader">
        <div class="spinner"></div>
        <p style="margin-top: 15px; font-weight: 600;">PROFIL ULANMOQDA...</p>
    </div>

    <div class="banner">
        <img src="https://i.postimg.cc/d1X5vYfK/M-LOGOG.png" style="width: 80px; margin-bottom: 10px;">
        <h1>YUSUFXONPRO</h1>
        <p>Yusufxonpro.uz | Premium Center</p>
    </div>

    <div id="login-page">
        <div class="input-group"><label>Ism</label><input type="text" id="name" placeholder="Yusufxon"></div>
        <div class="input-group"><label>Familiya</label><input type="text" id="surname" placeholder="Axmatov"></div>
        <div class="input-group"><label>Telefon</label><input type="tel" id="phone" placeholder="+998 XX-XXX-XX-XX"></div>
        <button onclick="connectProfile()" style="width: 100%; padding: 20px; background: #000; color: #fff; border: none; border-radius: 18px; font-weight: 800; margin-top: 10px;">PROFILNI ULASH</button>
    </div>

    <div id="app-layout">
        <div class="user-card">
            <img id="user-img" src="" class="avatar">
            <div>
                <h4 id="user-full-name">Yusufxon Axmatov</h4>
                <p id="user-tag" style="font-size: 12px; color: var(--sub);">@yusufxonpro</p>
            </div>
        </div>
        <div id="cargo-list"></div>
        <button class="fab" onclick="addCargo()">+</button>
    </div>

    <script>
        const tg = window.Telegram.WebApp;
        tg.expand();

        // Raqam maskasi (XX-XXX-XX-XX)
        document.getElementById('phone').addEventListener('input', (e) => {
            let v = e.target.value.replace(/\D/g, '');
            if (v.length > 12) v = v.substring(0, 12);
            let r = "+998 ";
            if (v.length > 3) {
                let p = v.substring(3).match(/(\d{0,2})(\d{0,3})(\d{0,2})(\d{0,2})/);
                r += p[1] + (p[2] ? "-" + p[2] : "") + (p[3] ? "-" + p[3] : "") + (p[4] ? "-" + p[4] : "");
            }
            e.target.value = r;
        });

        function connectProfile() {
            const n = document.getElementById('name').value;
            const s = document.getElementById('surname').value;
            const p = document.getElementById('phone').value;

            if (n && s && p.length >= 17) {
                document.getElementById('sync-loader').style.display = 'flex';
                
                setTimeout(() => {
                    const tgData = tg.initDataUnsafe?.user || {};
                    const userData = {
                        fullName: n + " " + s,
                        phone: p,
                        username: tgData.username ? "@" + tgData.username : "@user",
                        photo: tgData.photo_url || "https://ui-avatars.com/api/?name=" + n
                    };
                    localStorage.setItem('y_profile', JSON.stringify(userData));
                    tg.HapticFeedback.notificationOccurred('success');
                    location.reload();
                }, 2000);
            } else {
                tg.showAlert("Barcha maydonlarni to'ldiring!");
            }
        }

        window.onload = () => {
            const saved = JSON.parse(localStorage.getItem('y_profile'));
            if (saved) {
                document.getElementById('login-page').style.display = 'none';
                document.getElementById('app-layout').style.display = 'block';
                document.getElementById('user-img').src = saved.photo;
                document.getElementById('user-full-name').innerText = saved.fullName;
                document.getElementById('user-tag').innerText = saved.username;
                render();
            } else {
                document.getElementById('login-page').style.display = 'flex';
            }
        };

        function addCargo() {
            const txt = prompt("Yuk tavsifini kiriting:");
            if (txt) {
                const list = JSON.parse(localStorage.getItem('y_list') || '[]');
                list.unshift({ id: Date.now(), txt });
                localStorage.setItem('y_list', JSON.stringify(list));
                render();
            }
        }

        function render() {
            const list = JSON.parse(localStorage.getItem('y_list') || '[]');
            document.getElementById('cargo-list').innerHTML = list.map((c, i) => `
                <div class="cargo-card">
                    <span style="font-size: 10px; font-weight: 800; color: #34c759;">● 24/7 FAOL</span>
                    <div style="font-size: 18px; font-weight: 700; margin: 8px 0;">${c.txt}</div>
                    <button class="btn-del" onclick="del(${i})">O'CHIRISH</button>
                </div>
            `).join('');
        }

        function del(i) {
            const list = JSON.parse(localStorage.getItem('y_list'));
            list.splice(i, 1);
            localStorage.setItem('y_list', JSON.stringify(list));
            render();
            tg.HapticFeedback.notificationOccurred('warning');
        }
    </script>
</body>
</html>
