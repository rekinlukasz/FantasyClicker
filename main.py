"""Fantasy Clicker - logika gry uruchamiana w przeglądarce przez PyScript."""

import asyncio
import json

from js import document, localStorage, window
from pyodide.ffi import create_proxy
from pyscript import when

# Ulepszenia: per_click zwiększa złoto za kliknięcie, per_sec daje złoto automatycznie
UPGRADES = [
    {"id": "sword",  "icon": "🗡️", "name": "Zaklęty miecz",    "desc": "+1 za kliknięcie", "cost": 15,    "per_click": 1, "per_sec": 0},
    {"id": "elf",    "icon": "🧝", "name": "Elfi łucznik",     "desc": "+1 złota/s",       "cost": 50,    "per_click": 0, "per_sec": 1},
    {"id": "dwarf",  "icon": "⛏️", "name": "Krasnolud górnik", "desc": "+5 złota/s",       "cost": 300,   "per_click": 0, "per_sec": 5},
    {"id": "wizard", "icon": "🧙", "name": "Czarodziej",       "desc": "+25 złota/s",      "cost": 2000,  "per_click": 0, "per_sec": 25},
    {"id": "dragon", "icon": "🐉", "name": "Smok",             "desc": "+150 złota/s",     "cost": 15000, "per_click": 0, "per_sec": 150},
]

SAVE_KEY = "fantasyClickerSave"
TICK = 0.1

state = {"gold": 0.0, "owned": {}}
# Proxy trzymane w liście, żeby Python ich nie posprzątał, póki przeglądarka ich używa
_listeners = []


def load():
    global state
    try:
        saved = localStorage.getItem(SAVE_KEY)
        if saved:
            state = json.loads(saved)
    except Exception:
        pass


def save():
    try:
        localStorage.setItem(SAVE_KEY, json.dumps(state))
    except Exception:
        pass


def count(u):
    return state["owned"].get(u["id"], 0)


def cost(u):
    return int(u["cost"] * 1.15 ** count(u))


def per_click():
    return 1 + sum(u["per_click"] * count(u) for u in UPGRADES)


def per_sec():
    return sum(u["per_sec"] * count(u) for u in UPGRADES)


def fmt(n):
    return f"{int(n):,}".replace(",", " ")


def build_shop():
    shop = document.getElementById("shop")
    shop.innerHTML = ""
    for u in UPGRADES:
        btn = document.createElement("button")
        btn.className = "item"
        btn.id = "item-" + u["id"]
        btn.innerHTML = f"""
          <span class="icon">{u['icon']}</span>
          <span class="info"><b>{u['name']}</b><br><small>{u['desc']}</small><br>
            Koszt: <span class="cost"></span> złota</span>
          <span class="count"></span>"""
        handler = create_proxy(lambda event, u=u: buy(u))
        _listeners.append(handler)
        btn.addEventListener("click", handler)
        shop.appendChild(btn)


def buy(u):
    c = cost(u)
    if state["gold"] < c:
        return
    state["gold"] -= c
    state["owned"][u["id"]] = count(u) + 1
    render()
    save()


def render():
    document.getElementById("gold").textContent = f"{fmt(state['gold'])} złota"
    document.getElementById("perSec").textContent = f"{fmt(per_sec())} złota/s · {fmt(per_click())} za kliknięcie"
    for u in UPGRADES:
        btn = document.getElementById("item-" + u["id"])
        btn.querySelector(".cost").textContent = fmt(cost(u))
        btn.querySelector(".count").textContent = str(count(u))
        btn.disabled = state["gold"] < cost(u)


def show_floater(x, y, text):
    el = document.createElement("div")
    el.className = "floater"
    el.textContent = text
    el.style.left = f"{x}px"
    el.style.top = f"{y}px"
    document.body.appendChild(el)
    asyncio.ensure_future(remove_later(el, 0.8))


async def remove_later(el, delay):
    await asyncio.sleep(delay)
    el.remove()


@when("click", "#crystal")
def click(event):
    gain = per_click()
    state["gold"] += gain
    show_floater(event.clientX, event.clientY, "+" + fmt(gain))
    render()


@when("click", "#reset")
def reset(event):
    global state
    if not window.confirm("Na pewno zacząć od nowa?"):
        return
    state = {"gold": 0.0, "owned": {}}
    save()
    render()


async def game_loop():
    # Pasywny dochód 10 razy na sekundę, zapis co 5 sekund
    ticks = 0
    while True:
        await asyncio.sleep(TICK)
        state["gold"] += per_sec() * TICK
        render()
        ticks += 1
        if ticks % 50 == 0:
            save()


load()
build_shop()
render()
asyncio.ensure_future(game_loop())
