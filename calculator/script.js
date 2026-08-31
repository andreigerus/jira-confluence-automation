let expression = '';

function updateDisplay() {
  document.getElementById('expression').textContent = expression;
}

function append(value) {
  const last = expression.slice(-1);
  const operators = ['+', '-', '*', '/'];

  // Prevent consecutive operators
  if (operators.includes(value) && operators.includes(last)) {
    expression = expression.slice(0, -1);
  }

  // Prevent leading operator (except minus for negation)
  if (expression === '' && operators.includes(value) && value !== '-') return;

  // Prevent multiple decimals in the same number
  if (value === '.') {
    const parts = expression.split(/[\+\-\*\/]/);
    if (parts[parts.length - 1].includes('.')) return;
  }

  expression += value;
  updateDisplay();
}

function clearAll() {
  expression = '';
  document.getElementById('result').textContent = '0';
  updateDisplay();
}

function deleteLast() {
  expression = expression.slice(0, -1);
  updateDisplay();
  if (expression === '') {
    document.getElementById('result').textContent = '0';
  }
}

function calculate() {
  if (!expression) return;
  try {
    // Evaluate safely — only allow digits and basic operators
    if (!/^[0-9+\-*/.()\s]+$/.test(expression)) {
      document.getElementById('result').textContent = 'Error';
      return;
    }
    const result = Function('"use strict"; return (' + expression + ')')();
    document.getElementById('result').textContent =
      isFinite(result) ? parseFloat(result.toFixed(10)) : 'Error';
    expression = String(isFinite(result) ? parseFloat(result.toFixed(10)) : '');
    updateDisplay();
  } catch {
    document.getElementById('result').textContent = 'Error';
    expression = '';
    updateDisplay();
  }
}

// Keyboard support
document.addEventListener('keydown', (e) => {
  if ('0123456789+-*/.'.includes(e.key)) append(e.key);
  else if (e.key === 'Enter' || e.key === '=') calculate();
  else if (e.key === 'Backspace') deleteLast();
  else if (e.key === 'Escape') clearAll();
});
