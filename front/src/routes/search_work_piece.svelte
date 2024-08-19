<style>
  .search-work-piece {
    display: flex;
    flex-direction: column;
  }
  .search-row {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
  }
</style>
<script lang="ts">
  import Ymd from './ymd.svelte';
  import {type WorkPiece} from '../models/work_piece';
  import WorkPieceService from "../services/work_piece.service";
  import WorkPieceList from './project_list.svelte';

  let searchClientName = '';
  $: searchClientName

  let searchWorkPieceName = '';
  $: searchWorkPieceName

  let searchYmdStart = new Date();
  searchYmdStart.setMonth(searchYmdStart.getMonth() - 1);
  searchYmdStart.setDate(1);

  let searchYmdFinish = new Date();
  searchYmdFinish.setMonth(searchYmdFinish.getMonth() + 1);
  searchYmdFinish.setDate(0);

  export let foundWorkPieces = (founds: WorkPiece[]) => {
    console.log(`foundWorkPieces: ${founds ? founds.length : 'none'}`);
  }

  let workPieces: WorkPiece[];
  $: workPieces

  let searchYmdStartString = searchYmdStart.toISOString().split('T')[0];
  $: searchYmdStartString
  const selectYmdStart = (next: string): void => {
    searchYmdStartString = next;
    executeSearchWorkPiece();
  }

  let searchYmdFinishString = searchYmdFinish.toISOString().split('T')[0];
  $: searchYmdFinishString
  const selectYmdFinish = (next: string): void => {
    searchYmdFinishString = next;
    executeSearchWorkPiece();
  }

  const executeSearchWorkPiece = (): void => {
    WorkPieceService.find({
      created_from: searchYmdStartString,
      created_through: searchYmdFinishString,
    }).then((response: any) => {
      workPieces = response.data;
      foundWorkPieces(workPieces);
    });
  }

  let timeoutSearchWorkPiece: any;
  const searchWorkPiece = (): void => {
    if (timeoutSearchWorkPiece) {
      clearTimeout(timeoutSearchWorkPiece);
    }
    timeoutSearchWorkPiece = setTimeout(() => {
      executeSearchWorkPiece();
    }, 300);
  }

  const keyupFrom = (): void => {
    searchWorkPiece();
  }
  const keyupThrough = (): void => {
    searchWorkPiece();
  }
</script>
<div class="search-work-piece">
  <div class="flex flex-row search-row" style="max-width: 400px; margin: auto;">
    <div>created from</div>
    <Ymd initialYmd={searchYmdStart} selectYmd={selectYmdStart} keyup={keyupFrom}></Ymd>
    <div>through</div>
    <Ymd initialYmd={searchYmdFinish} selectYmd={selectYmdFinish} keyup={keyupThrough}></Ymd>
  </div>
</div>