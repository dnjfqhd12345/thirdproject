function drawBlock(block, ctx) {
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);

    block.shape.forEach((row, y) => {
        row.forEach((value, x) => {
            if(value > 0) {
                ctx.fillStyle = 'black';
                ctx.fillRect(x + block.x, y + block.y, 1, 1);
            }
        });
    });
}

function drawBoard(matrix, ctx) {
    matrix.forEach((row, y) => {
        row.forEach((value, x) => {
            if(value > 0) {
                ctx.fillStyle = 'black';
                ctx.fillRect(x, y, 1, 1);
            }
        });
    });
}
