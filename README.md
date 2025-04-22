# Forktimize – Fullstack Meal Planner
Forktimize is a fullstack web application that generates meal plans based on nutritional constraints, disliked foods, and vendor availability. It selects optimal menus using an integer linear programming (ILP) solver and real-time food data scraped from the most popular Hungarian food vendors like InterFood, CityFood and Teletál.

## 🛠️ Development Setup

### 📦 Prerequisites

Make sure you have the following installed:

- Python 3.11+
- Node.js 18+
- `make`
- `tmux` (for `make run`)

---

### 🐍 Backend Setup (FastAPI)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
make run-backend
```
### 🎨 Frontend Setup (SvelteKit)
```
cd frontend
npm install
make run-frontend
```
 Use ```make run-frontend-dev```
 to run against mock backend data

### 🎨 All-in-One Dev Mode
Spin up both frontend and backend in tmux panes:
```make run```


# Contributing

## Missing your favorite food vendor?

To add a new vendor:

1. Implement the `FoodCollectionStrategy` interface.
2. Add your food vendor to the `VENDOR_REGISTRY`
