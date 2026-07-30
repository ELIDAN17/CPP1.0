const canvas = document.getElementById('tree');
const ctx = canvas.getContext('2d');
canvas.width = 400;
canvas.height = 500;
let running = false;
let angleOffset = 0;
const speed = document.getElementById('speed');
const color = document.getElementById('color');
const toggle = document.getElementById('toggle');

function drawTreeBase() {
    ctx.save();
    ctx.translate(canvas.width / 2, canvas.height);
    const gradient = ctx.createLinearGradient(0, -420, 0, 0);
    gradient.addColorStop(0, '#058b63ff');
    gradient.addColorStop(1, '#0eb08dff');
    ctx.beginPath();
    ctx.moveTo(0, -420);
    ctx.lineTo(-160, 0);
    ctx.lineTo(160, 0);
    ctx.closePath();
    ctx.fillStyle = gradient;
    ctx.fill();
    ctx.restore();
}

function drawStar() {
    ctx.save();
    ctx.translate(canvas.width / 2, canvas.height - 420);
    ctx.beginPath();
    ctx.fillStyle = '#ffdd00';
    ctx.shadowBlur = 35;
    ctx.shadowColor = '#ffdd00';
    const outer = 32;
    const inner = 14;
    for (let i = 0; i < 5; i++) {
        ctx.lineTo(0, -outer);
        ctx.rotate(Math.PI / 5);
        ctx.lineTo(0, -inner);
        ctx.rotate(Math.PI / 5);
    }
    ctx.fill();
    ctx.restore();
}

function drawSpiral() {
    const total = 240;
    for (let i = 0; i < total; i++) {
        const t = i / total;
        const y = -20 - t * 300;
        const radius = 140 * (1 - t);
        const angle = angleOffset + t * 18 * Math.PI;
        const x = Math.cos(angle) * radius;
        ctx.save();
        ctx.translate(canvas.width / 2, canvas.height);
        ctx.beginPath();
        ctx.arc(x, y, 6 * (1 - t * 0.7), 0, Math.PI * 2);
        ctx.fillStyle = color.value;
        ctx.shadowBlur = 12;
        ctx.shadowColor = color.value;
        ctx.fill();
        ctx.restore();
    }
}
function animate() {
    if (!running) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    drawTreeBase();
    drawStar();
    drawSpiral();
    angleOffset += parseFloat(speed.value);
    requestAnimationFrame(animate);
}
toggle.addEventListener('click', () => {
    running = !running;
    if (running) {
        animate();
    } else {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        drawTreeBase();
        drawStar();
    }
});
// Initial draw
drawTreeBase();
drawStar();