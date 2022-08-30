function randomNextBlockMatrix() {
    const BLOCK_SET = [
        [
            [1,1],
            [1,1]
        ],
        [
            [0,2,0],
            [2,2,2],
            [0,0,0]
        ],
        [
            [0,3,3],
            [3,3,0],
            [0,0,0]
        ],
        [
            [4,4,0],
            [0,4,4],
            [0,0,0]
        ],
        [
            [5,0,0],
            [5,5,5],
            [0,0,0]
        ],
        [
            [0,0,6],
            [6,6,6],
            [0,0,0]
        ],
        [
            [0,0,0,0],
            [7,7,7,7],
            [0,0,0,0],
            [0,0,0,0]
        ]
    ]
    
return BLOCK_SET[getRandomIndex(BLOCK_SET.length)];
}

function initMatrix(rows, cols) {
    let matrix = [];
    for(let y=0; y < rows; y++) {
        matrix.push(new Array(cols).fill(0));
    }
    return matrix;
}

function stack(block, matrix) {
    block.shape.forEach((row, y) => {
        row.forEach((value, x) => {
            if(value > 0) {
                matrix[y+block.y][x+block.x] = block.shape[y][x];
            }
        });
    });
}
