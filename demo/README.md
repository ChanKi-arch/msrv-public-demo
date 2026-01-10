🧭 MSR-V Public Demo — Quick User Guide

This guide explains how to run the MSR-V public demo and what you are actually seeing.


---

1️⃣ What is this demo?

This repository contains an IP-safe public simulator of the MSR-V White Engine.

It does NOT contain the proprietary reasoning engine.
Instead, it shows:

How routing (MINI / STANDARD / PREMIUM) works

How structural states are reported

How governance metrics (Zs, theta, need) look

How cost-saving modes change behavior


Think of it as a flight simulator for MSR-V governance.


---

2️⃣ What do I need?

You only need:

Python 3.8 or newer

Internet (for pip install)


Check your Python:

python --version


---

3️⃣ Download & Setup

Option A — easiest (no Git required)

1. Go to
https://github.com/ChanKi-arch/msrv-public-demo/releases


2. Download v2.5.5-final.zip


3. Unzip it


4. Open a terminal inside the unzipped folder



Then:

pip install -r requirements.txt


---

Option B — Git users

git clone https://github.com/ChanKi-arch/msrv-public-demo
cd msrv-public-demo
git checkout tags/v2.5.5-final
pip install -r requirements.txt


---

4️⃣ Run the CLI Demo

python demo/demo_cli.py

You will see:

MSR-V Public Demo
Enter text:

Type any sentence:

> The moon is made of cheese

You will get output like:

{
  "route": "STANDARD",
  "state4": "Fracture",
  "Zs": 0.42,
  "theta": 0.31,
  "need": 0.76
}

This shows:

How risky the reasoning is

How much reasoning MSR-V allows

Which tier would be used



---

5️⃣ Run the Web UI

streamlit run demo/web_ui.py

Your browser opens:

http://localhost:8501

You can:

Paste text

See routing decisions

View stability and structural state

Switch modes


This UI is what investors & engineers usually look at first.


---

6️⃣ Why do results look “similar”?

Because this is a public simulation build.

The demo uses:

precomputed samples

conservative fallback heuristics


This prevents reverse-engineering of the proprietary engine while still showing:

routing behavior

cost control

safety logic

governance signals


Real MSR-V production engine:

Uses internal structural parsers

Is not open-sourced



---

7️⃣ What should I focus on?

You are not testing truth.
You are testing governance.

Look at:

How often PREMIUM is used

How modes change routing

How negation & hard inputs raise risk

How cost drops in AGGRESSIVE mode


This is how MSR-V saves money while protecting safety.


---

8️⃣ What this demo proves

✔ Structural governance works
✔ Cost control is deterministic
✔ Safety policies are enforceable
✔ Routing is transparent
✔ MSR-V is model-agnostic


---

If you show this to others, say this

> “This is a governance simulator for MSR-V.
It shows how the real engine decides how much reasoning an LLM is allowed to do.”




---
