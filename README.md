# Lynra Webhook Spammer

> ⚠️ For **educational** and **testing** purposes only.  
> Do **not** use on real servers or without permission — doing so violates Discord's [Terms of Service](https://discord.com/terms).

---

## 📋 Table of Contents

- [📸 Screenshot Preview](#-screenshot-preview)
- [⚙️ How to Set It Up](#️-how-to-set-it-up)
- [🛠 Files](#-files)
- [📢 Features](#-features)
- [📬 Example `config.json`](#-example-configjson)
- [✅ Done? Run it again!](#-done-run-it-again)
- [🧠 Reminder](#-reminder)

---

## 📸 Screenshot Preview

<img src="https://cdn.discordapp.com/attachments/1306616995994800250/1387851296169656392/image.png?ex=685ed8be&is=685d873e&hm=1a0524acb08f16f42a6bcbb5c46d533b9844d0e32541553ee6d9fb849449fe30&" width="782" height="351" alt="Lynra Webhook Spammer Preview">

---

## ⚙️ How to Set It Up

1. Open `config.json` and customize:
   - `"username"`: the name to send messages as.
   - `"avatar_url"`: optional avatar image.
   - If `config.json` is missing, Lynra will use its own defaults.

2. Run `install.bat`:
   - Installs required Python modules.
   - Automatically installs Python if missing.
   - Launches (`main.py`).

---

## 🛠 Files

- `main.py`: Main spammer script.
- `config.json`: Webhook username/avatar config.
- `install.bat`: Installs Python and modules, runs app.

---

## 📢 Features

- ✅ Sends messages via any valid Discord webhook.
- 👤 Custom username and avatar.
- 🧠 Smart rate limit handling.
- 🚀 Multi-threaded = fast message delivery.
- 🎯 Clean, styled CLI with success/fail messages.
- 🔁 Re-use: Prompt to spam again after finishing.
- 🧼 Auto-cleans temp files on start.

---

## 📬 Example `config.json`

```json
{
  "username": ".gg/lynra",
  "avatar_url": "https://cdn.discordapp.com/attachments/1386363599353680083/1387836855067869305/output-onlinepngtools_1.png?ex=685ecb4b&is=685d79cb&hm=805cd4c35a1880da5855e4d2b3e837fae170ac2cead15e0e5d1f0264c99853ca&"




(yes this readme was made with chatgpt im too lazy to make it )
