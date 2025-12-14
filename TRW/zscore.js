// Create container
const container = document.createElement('div');
container.id = 'bellCurve';
container.style.cssText = `
  position: fixed;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  z-index: 10000;
  user-select: none;
`;

// Create SVG
const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
svg.setAttribute('width', '150');
svg.setAttribute('height', '600');
svg.style.display = 'block';
svg.style.cursor = 'move';

// Create controls
const controls = document.createElement('div');
controls.style.cssText = `
  position: absolute;
  top: -40px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(255, 255, 255, 0.9);
  padding: 5px 10px;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0,0,0,0.2);
  white-space: nowrap;
`;
controls.innerHTML = `
  <span style="font-size: 11px; margin-right: 5px;">Drag to move | Drag green ball to scale</span>
  <button id="flipBtn" style="padding: 3px 8px; margin: 0 2px; background: #2196F3; color: white; border: none; border-radius: 3px; font-size: 11px;">Flip</button>
  <button id="skewLeftBtn" style="padding: 3px 8px; margin: 0 2px; background: #9C27B0; color: white; border: none; border-radius: 3px; font-size: 11px;">← Skew</button>
  <button id="resetSkewBtn" style="padding: 3px 8px; margin: 0 2px; background: #607D8B; color: white; border: none; border-radius: 3px; font-size: 11px;">Reset</button>
  <button id="skewRightBtn" style="padding: 3px 8px; margin: 0 2px; background: #9C27B0; color: white; border: none; border-radius: 3px; font-size: 11px;">Skew →</button>
  <button id="closeBtn" style="padding: 3px 8px; margin: 0 2px; background: #ff4444; color: white; border: none; border-radius: 3px; font-size: 11px;">Close</button>
`;

container.appendChild(svg);
container.appendChild(controls);
document.body.appendChild(container);

// Bell curve parameters
let height = 600;
let svgWidth = 150;
let isFlipped = false;
let skewness = 0;  // -3 to +3

// Function to calculate skew-normal distribution
function skewNormalPDF(x, alpha) {
  const phi = Math.exp(-(x * x) / 2) / Math.sqrt(2 * Math.PI);
  const Phi = 0.5 * (1 + erf(alpha * x / Math.sqrt(2)));
  return 2 * phi * Phi;
}