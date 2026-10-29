// Ulepszenia: perClick zwiększa złoto za kliknięcie, perSec daje złoto automatycznie
const upgrades = [
  { id: "sword",  icon: "🗡️", name: "Zaklęty miecz",  desc: "+1 za kliknięcie", cost: 15,    perClick: 1, perSec: 0 },
  { id: "elf",    icon: "🧝", name: "Elfi łucznik",   desc: "+1 złota/s",       cost: 50,    perClick: 0, perSec: 1 },
  { id: "dwarf",  icon: "⛏️", name: "Krasnolud górnik", desc: "+5 złota/s",     cost: 300,   perClick: 0, perSec: 5 },
  { id: "wizard", icon: "🧙", name: "Czarodziej",     desc: "+25 złota/s",      cost: 2000,  perClick: 0, perSec: 25 },
  { id: "dragon", icon: "🐉", name: "Smok",           desc: "+150 złota/s",     cost: 15000, perClick: 0, perSec: 150 },
];

const SAVE_KEY = "fantasyClickerSave";
let state = { gold: 0, owned: {} };

function load() {
  try {
    const saved = JSON.parse(localStorage.getItem(SAVE_KEY));
    if (saved) state = saved;
  } catch (e) {}
}

function save() {
  try { localStorage.setItem(SAVE_KEY, JSON.stringify(state)); } catch (e) {}
}

const count = (u) => state.owned[u.id] || 0;
const cost = (u) => Math.floor(u.cost * Math.pow(1.15, count(u)));
const perClick = () => 1 + upgrades.reduce((s, u) => s + u.perClick * count(u), 0);
const perSec = () => upgrades.reduce((s, u) => s + u.perSec * count(u), 0);
const fmt = (n) => Math.floor(n).toLocaleString("pl-PL");

const shop = document.getElementById("shop");

function buildShop() {
  shop.innerHTML = "";
  for (const u of upgrades) {
    const btn = document.createElement("button");
    btn.className = "item";
    btn.id = "item-" + u.id;
    btn.innerHTML = `
      <span class="icon">${u.icon}</span>
      <span class="info"><b>${u.name}</b><br><small>${u.desc}</small><br>
        Koszt: <span class="cost"></span> złota</span>
      <span class="count"></span>`;
    btn.addEventListener("click", () => buy(u));
    shop.appendChild(btn);
  }
}

function buy(u) {
  const c = cost(u);
  if (state.gold < c) return;
  state.gold -= c;
  state.owned[u.id] = count(u) + 1;
  render();
  save();
}

function render() {
  document.getElementById("gold").textContent = fmt(state.gold) + " złota";
  document.getElementById("perSec").textContent =
    `${fmt(perSec())} złota/s · ${fmt(perClick())} za kliknięcie`;
  for (const u of upgrades) {
    const btn = document.getElementById("item-" + u.id);
    btn.querySelector(".cost").textContent = fmt(cost(u));
    btn.querySelector(".count").textContent = count(u);
    btn.disabled = state.gold < cost(u);
  }
}

function showFloater(x, y, text) {
  const el = document.createElement("div");
  el.className = "floater";
  el.textContent = text;
  el.style.left = x + "px";
  el.style.top = y + "px";
  document.body.appendChild(el);
  setTimeout(() => el.remove(), 800);
}

document.getElementById("crystal").addEventListener("click", (e) => {
  const gain = perClick();
  state.gold += gain;
  showFloater(e.clientX, e.clientY, "+" + fmt(gain));
  render();
});

document.getElementById("reset").addEventListener("click", () => {
  if (!confirm("Na pewno zacząć od nowa?")) return;
  state = { gold: 0, owned: {} };
  save();
  render();
});

// Pasywny dochód 10 razy na sekundę, zapis co 5 sekund
setInterval(() => {
  state.gold += perSec() / 10;
  render();
}, 100);
setInterval(save, 5000);

load();
buildShop();
render();
