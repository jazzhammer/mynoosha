<style>
  .work-piece-list {
    display: grid;
    grid-template-columns: 1fr 2fr 2fr 2fr 5fr 5fr;
    font-size: 9pt;
    max-width: 800px;
  }
  .work-piece-list-header {
    text-align: center;
    color: black;
    font-weight: bold;
    font-size: 9pt;
  }
  .work-piece-field {
    text-align: center;
  }
</style>

<script lang="ts">
  import {type WorkPiece} from '../models/work_piece';
  // import WorkPieceView from './work_piece_view.svelte';

  export let workPieces: WorkPiece[] = [];

  export let selectWorkPiece: (workPiece: WorkPiece) => void;



</script>
<div class="flex flex-col">
  <div class="work-piece-list w-full border border-myblue-50">
    <div class="work-piece-list-header bg-mylow_white">id</div>
    <div class="work-piece-list-header bg-mylow_white">client</div>
    <div class="work-piece-list-header bg-mylow_white">project</div>
    <div class="work-piece-list-header bg-mylow_white">worker</div>
    <div class="work-piece-list-header bg-mylow_white">start</div>
    <div class="work-piece-list-header bg-mylow_white">finish</div>

    {#each workPieces as workPiece}
      <div on:click={() => {selectWorkPiece(workPiece)}} class="work-piece-field text-black cursor-pointer hover:bg-myblue-100">
        {workPiece.id}
      </div>
      <div on:click={() => {selectWorkPiece(workPiece)}} class="work-piece-field text-black cursor-pointer hover:bg-myblue-100">
        {workPiece.client ? workPiece.client : 'none'}
      </div>
      <div on:click={() => {selectWorkPiece(workPiece)}} class="work-piece-field text-black cursor-pointer hover:bg-myblue-100">
        {workPiece.project ? workPiece.project : 'none'}
      </div>
      <div on:click={() => {selectWorkPiece(workPiece)}} class="work-piece-field text-black cursor-pointer hover:bg-myblue-100">
        {workPiece.worker ? workPiece.worker : 'none'}
      </div>
      <div on:click={() => {selectWorkPiece(workPiece)}} class="work-piece-field text-black cursor-pointer hover:bg-myblue-100">
        {workPiece.start.split('.')[0].replace('T', ' ')}
      </div>
      <div on:click={() => {selectWorkPiece(workPiece)}} class="work-piece-field text-black cursor-pointer hover:bg-myblue-100">
        {workPiece.finish.split('.')[0].replace('T', ' ')}
      </div>
    {/each}
  </div>
  <div>
<!--    <WorkPieceView></WorkPieceView>-->
  </div>
</div>
