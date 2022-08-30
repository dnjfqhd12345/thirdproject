function resize() {
    const WINDOW_INNERWIDTH = (window.innerWidth > 660)?660:window.innerWidth;
    const MAIN_CONTENTS_WIDTH = Math.floor(WINDOW_INNERWIDTH*0.6);
    const BLOCK_SIZE = Math.floor(MAIN_CONTENTS_WIDTH/COLS_MAIN_BOARD);

    ctxMainBoard.canvas.width = BLOCK_SIZE*COLS_MAIN_BOARD;
    ctxMainBoard.canvas.height = BLOCK_SIZE*ROWS_MAIN_BOARD;
    ctxMainBoard.scale(BLOCK_SIZE, BLOCK_SIZE);

    ctxNextBoard.canvas.width = BLOCK_SIZE*COLS_NEXT_BOARD;
    ctxNextBoard.canvas.height = BLOCK_SIZE*ROWS_NEXT_BOARD;
    ctxNextBoard.scale(BLOCK_SIZE, BLOCK_SIZE);

    const FONT_RATIO = WINDOW_INNERWIDTH/350;
    document.querySelector("#side-contents").getElementsByClassName.fontSize = FONT_RATIO+'rem'
}

(function (){
    main();
})();

function main() {
    window.addEventListener('keydown', keyHandler);
    mainBlock = createNextBlock();
    nextBlock = createNextBlock();
    rebuild();
    window.addEventListener('resize', resize);
    repeatMotion(0);
}

function createNextBlock() {
    const nextBlock = {
        x: 0,
        y: 0,
        shape: randomNextBlockMatrix()
    }

    return nextBlock;
}



function rebuild() {
    resize();
    drawBlock(mainBlock, ctxMainBoard);
    drawBlock(nextBlock, ctxNextBoard);
    drawBoard(matrixMainBoard, ctxMainBoard); //추가된 부분
}

function keyHandler(event) {
    const inputKey = event.keyCode;

    const KEY = {
        LEFT: 37,
        UP: 38,
        RIGHT: 39,
        DOWN: 40
    }

    switch(inputKey) {
        case KEY.UP :
            validRotate(mainBlock, matrixMainBoard);
            break;
        case KEY.DOWN :
            validMove(mainBlock, matrixMainBoard, 0, 1);
            break;
        case KEY.LEFT :
            validMove(mainBlock, matrixMainBoard, -1, 0);
            break;
        case KEY.RIGHT :
            validMove(mainBlock, matrixMainBoard, 1, 0);
            break;
    }

    drawBlock(mainBlock, ctxMainBoard);
}

function repeatMotion(timeStamp) {
    const duration = timeStamp - time;

    if(duration > 1000) {
        if(!validMove(mainBlock, matrixMainBoard, 0, 1)) {
            stack(mainBlock, matrixMainBoard); //추가 부분
            mainBlock = nextBlock;
            nextBlock = createNextBlock();
            
            /* 추가 부분 시작 */
            matrixMainBoard[0].some((value, x) => {
                if(value > 0) {
                    window.cancelAnimationFrame(requestAnimationId);
                    requestAnimationId = null;
                    return true;
                }
            });
            
            if(requestAnimationId == null) {
                return;
            }
            /* 추가 부분 끝 */
        }
        time = timeStamp;
    }

    rebuild();
    requestAnimationId = window.requestAnimationFrame(repeatMotion);
}
