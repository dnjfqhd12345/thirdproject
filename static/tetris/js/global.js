const canvasMainBoard = document.querySelector('#main-board');
const ctxMainBoard = canvasMainBoard.getContext('2d');
const canvasNextBoard = document.querySelector("#next-board");
const ctxNextBoard = canvasNextBoard.getContext('2d');

const COLS_MAIN_BOARD = 10;
const ROWS_MAIN_BOARD=20;
const COLS_NEXT_BOARD = 4;
const ROWS_NEXT_BOARD = 4;

var mainBlock = null;
var nextBlock = null;

const matrixMainBoard = initMatrix(ROWS_MAIN_BOARD, COLS_MAIN_BOARD);

let time = 0;
let requestAnimationId = null;
