const grid = document.getElementById("sudoku-grid");

const solveBtn = document.getElementById("solve-btn");
const compareBtn = document.getElementById("compare-btn");
const generateBtn = document.getElementById("generate-btn");

// ---------------- INIT GRID ----------------
function init() {
  for (let i = 0; i < 81; i++) {
    const input = document.createElement("input");
    input.type = "number";
    input.className = "cell";
    input.min = 1;
    input.max = 9;
    grid.appendChild(input);
  }
}

// ---------------- BOARD ----------------
function getBoard() {
  const inputs = document.querySelectorAll(".cell");

  let board = [];

  for (let r = 0; r < 9; r++) {
    let row = [];
    for (let c = 0; c < 9; c++) {
      let v = parseInt(inputs[r * 9 + c].value);
      row.push(isNaN(v) ? 0 : v);
    }
    board.push(row);
  }

  return board;
}

// ---------------- DRAW ----------------
function drawBoard(board) {
  const inputs = document.querySelectorAll(".cell");

  board.flat().forEach((v, i) => {
    inputs[i].value = v === 0 ? "" : v;
  });
}

// ---------------- RESET COLORS ----------------
function reset() {
  document.querySelectorAll(".cell").forEach(c => {
    c.style.background = "white";
  });
}

// ---------------- ANIMATION ----------------
async function animate(steps) {
  const inputs = document.querySelectorAll(".cell");
  const speed = parseInt(document.getElementById("speed").value);

  for (let s of steps) {
    let idx = s.row * 9 + s.col;

    inputs[idx].value = s.value === 0 ? "" : s.value;

    inputs[idx].style.background =
      s.type === "fill" ? "#86efac" : "#fca5a5";

    await new Promise(r => setTimeout(r, speed));
  }
}

// ---------------- SOLVE ----------------
async function solve() {
  const board = getBoard();
  const algorithm = document.getElementById("algo-select").value;
  const difficulty = document.getElementById("difficulty-select").value;

  const res = await fetch("http://127.0.0.1:8000/solve", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ board, algorithm, difficulty })
  });

  const data = await res.json();

  console.log("API RESPONSE:", data); // 🔥 DEBUG (VERY IMPORTANT)

  if (data.success) {

    reset();

    if (data.steps) {
      await animate(data.steps);
    }

    document.getElementById("time-val").innerText =
      data.metrics.executionTime.toFixed(5);

    document.getElementById("states-val").innerText =
      data.metrics.statesExplored;

    document.getElementById("backtrack-val").innerText =
      data.metrics.backtracksPerformed;
  }
}

// ---------------- GENERATE ----------------
async function generate() {
  const difficulty = document.getElementById("difficulty-select").value;

  const res = await fetch("http://localhost:8000/generate", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ difficulty })
  });

  const data = await res.json();
  drawBoard(data.board);
}

// ---------------- COMPARE ----------------
async function compare() {
  const board = getBoard();
  const difficulty = document.getElementById("difficulty-select").value;

  const res = await fetch("http://127.0.0.1:8000/compare", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ board, algorithm: "backtracking", difficulty })
  });

  const data = await res.json();

  console.log("COMPARE RESPONSE:", data);

  const tbody = document.getElementById("benchmark-body");
  tbody.innerHTML = "";

  data.forEach(r => {
    tbody.innerHTML += `
      <tr>
        <td>${r.algorithm}</td>
        <td>${r.executionTime}s</td>
        <td>${r.statesExplored}</td>
        <td>${r.backtracks}</td>
        <td>${r.success ? "✅" : "❌"}</td>
      </tr>
    `;
  });
}

// ---------------- EVENTS ----------------
solveBtn.onclick = solve;
compareBtn.onclick = compare;
generateBtn.onclick = generate;

document.getElementById("clear-btn").onclick = () => location.reload();

init();