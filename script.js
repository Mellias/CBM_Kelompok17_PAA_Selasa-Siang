const scale = 10;
const gridSize = 150;
const cellSize = scale;
const padding = 1;  // Padding in number of cells
const canvas = document.getElementById('mapCanvas');
const context = canvas.getContext('2d');

const buildings = {
    big: { width: 10 * scale, height: 5 * scale, color: 'red' },
    medium: { width: 5 * scale, height: 3 * scale, color: 'blue' },
    small: { width: 2 * scale, height: 2 * scale, color: 'yellow' },
    house: { width: 1 * scale, height: 2 * scale, color: 'orange' }
};

const roadWidth = 10;
let map;

// Function to initialize the map array
function initializeMap() {
    map = Array.from({ length: gridSize }, () => Array(gridSize).fill(null));
}

// Function to draw the map
function drawMap() {
    context.clearRect(0, 0, canvas.width, canvas.height);
    
    for (let y = 0; y < gridSize; y++) {
        for (let x = 0; x < gridSize; x++) {
            const cell = map[y][x];
            if (cell) {
                context.fillStyle = cell.color;
                context.fillRect(x * cellSize, y * cellSize, cellSize, cellSize);
            } else {
                context.fillStyle = 'green';  // Fill unused cells with green for parks or lawns
                context.fillRect(x * cellSize, y * cellSize, cellSize, cellSize);
            }
        }
    }

    highlightUnaffectedAreas();
}

// Function to place buildings on the map
function placeBuildings() {
    placeBuilding('big', 1);
    placeBuilding('medium', 4);
    placeBuilding('small', 10);
    placeBuilding('house', 10);
}

// Function to place a specific type of building
function placeBuilding(type, count) {
    const { width, height, color } = buildings[type];

    for (let i = 0; i < count; i++) {
        let placed = false;
        while (!placed) {
            const x = Math.floor(Math.random() * (gridSize - width / cellSize - 2 * padding));
            const y = Math.floor(Math.random() * (gridSize - height / cellSize - 2 * padding));
            if (canPlaceBuilding(x, y, width / cellSize, height / cellSize)) {
                for (let j = 0; j < height / cellSize; j++) {
                    for (let k = 0; k < width / cellSize; k++) {
                        map[y + j + padding][x + k + padding] = { color };
                    }
                }
                placed = true;
            }
        }
    }
}

// Function to check if a building can be placed
function canPlaceBuilding(x, y, width, height) {
    for (let j = -padding; j < height + padding; j++) {
        for (let k = -padding; k < width + padding; k++) {
            if (map[y + j + padding] && map[y + j + padding][x + k + padding] !== null) {
                return false;
            }
        }
    }
    return true;
}

// Function to generate roads
function generateRoads() {
    addMainRoads();
    addTurnsAndForks();
}

// Function to add main roads
function addMainRoads() {
    // Add central roads as main roads
    addRoad(Math.floor(gridSize / 2), 0, 'vertical');  // Entrance
    addRoad(0, Math.floor(gridSize / 2), 'horizontal');  // Entrance
    addRoad(Math.floor(gridSize / 2), gridSize - 1, 'vertical');  // Exit
    addRoad(gridSize - 1, Math.floor(gridSize / 2), 'horizontal');  // Exit
}

// Function to add turns and forks
function addTurnsAndForks() {
    // Add a turn at a random position
    const turnX = Math.floor(Math.random() * (gridSize - roadWidth));
    const turnY = Math.floor(Math.random() * (gridSize - roadWidth));
    addRoad(turnX, 0, 'vertical');
    addRoad(turnX, turnY + roadWidth, 'horizontal'); // Adjusting the horizontal road to avoid overlap
    
    // Add a fork at a random position
    const forkX = Math.floor(Math.random() * (gridSize - roadWidth));
    const forkY = Math.floor(Math.random() * (gridSize - roadWidth));
    addRoad(forkX, 0, 'vertical');
    addRoad(forkX, forkY + roadWidth, 'horizontal'); // Adjusting the horizontal road to avoid overlap
    addRoad(forkX, forkY + roadWidth * 2, 'horizontal'); // Adjusting the second horizontal road to avoid overlap
}

// Function to add a road
function addRoad(x, y, direction) {
    if (direction === 'vertical') {
        for (let i = 0; i < gridSize; i++) {
            if (y + i >= gridSize) break;
            map[y + i][x] = { color: 'black' };
        }
    } else {
        for (let i = 0; i < gridSize; i++) {
            if (x + i >= gridSize) break;
            map[y][x + i] = { color: 'black' };
        }
    }
}

// Function to handle map regeneration
function regenerateMap() {
    initializeMap();
    generateRoads();
    placeBuildings();
    drawMap();
}

// Event listener for the regenerate button
document.getElementById('regenerateButton').addEventListener('click', regenerateMap);

// Function to resize the canvas
function resizeCanvas() {
    canvas.width = gridSize * cellSize;
    canvas.height = gridSize * cellSize;
}

// Initial map generation and canvas resizing
resizeCanvas();
regenerateMap();

// Flood fill algorithm to find and color unaffected areas
function highlightUnaffectedAreas() {
    const visited = Array.from({ length: gridSize }, () => Array(gridSize).fill(false));

    function isRoadAdjacent(x, y) {
        const directions = [
            [0, 1], [1, 0], [0, -1], [-1, 0],  // Right, Down, Left, Up
            [1, 1], [1, -1], [-1, 1], [-1, -1] // Diagonals
        ];
        return directions.some(([dx, dy]) => {
            const nx = x + dx, ny = y + dy;
            return nx >= 0 && ny >= 0 && nx < gridSize && ny < gridSize && map[ny][nx] && map[ny][nx].color === 'black';
        });
    }

    function floodFill(x, y) {
        const queue = [[x, y]];
        const color = 'lightgreen';

        while (queue.length > 0) {
            const [cx, cy] = queue.shift();

            if (cx < 0 || cy < 0 || cx >= gridSize || cy >= gridSize || visited[cy][cx] || (map[cy][cx] && map[cy][cx].color === 'black') || isRoadAdjacent(cx, cy)) {
                continue;
            }

            visited[cy][cx] = true;
            context.fillStyle = color;
            context.fillRect(cx * cellSize, cy * cellSize, cellSize, cellSize);

            queue.push([cx + 1, cy]);
            queue.push([cx - 1, cy]);
            queue.push([cx, cy + 1]);
            queue.push([cx, cy - 1]);
        }
    }

    // Run flood fill from all edges to find connected components not affected by roads
    for (let y = 0; y < gridSize; y++) {
        for (let x = 0; x < gridSize; x++) {
            if (!visited[y][x] && !map[y][x]) {
                floodFill(x, y);
            }
        }
    }
}

resizeCanvas();
regenerateMap();
