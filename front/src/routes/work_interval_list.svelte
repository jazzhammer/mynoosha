<style>
  .work-interval-list {
    display: grid;
    grid-template-columns: 1fr 2fr 2fr 2fr 5fr 5fr 2fr;
    font-size: 9pt;
    max-width: 800px;
  }
  .work-interval-list-header {
    text-align: center;
    color: black;
    font-weight: bold;
    font-size: 9pt;
  }
  .work-interval-field {
    text-align: center;
  }
</style>

<script lang="ts">
  import {type WorkInterval} from '../models/work_interval';
  // import WorkIntervalView from './work_interval_view.svelte';

  export let workIntervals: WorkInterval[] = [];

  export let selectWorkInterval: (workInterval: WorkInterval) => void;



</script>
<div class="flex flex-col">
  <div class="work-interval-list w-full border border-myblue-50">
    <div class="work-interval-list-header bg-mylow_white">id</div>
    <div class="work-interval-list-header bg-mylow_white">client</div>
    <div class="work-interval-list-header bg-mylow_white">project</div>
    <div class="work-interval-list-header bg-mylow_white">worker</div>
    <div class="work-interval-list-header bg-mylow_white">start</div>
    <div class="work-interval-list-header bg-mylow_white">stop</div>
    <div class="work-interval-list-header bg-mylow_white">hhmm</div>
    {#each workIntervals as workInterval}
      <div on:click={() => {selectWorkInterval(workInterval)}} class="work-interval-field text-black cursor-pointer hover:bg-myblue-100">
        {workInterval.id}
      </div>
      <div on:click={() => {selectWorkInterval(workInterval)}} class="work-interval-field text-black cursor-pointer hover:bg-myblue-100">
        {workInterval.client ? workInterval.client : 'none'}
      </div>
      <div on:click={() => {selectWorkInterval(workInterval)}} class="work-interval-field text-black cursor-pointer hover:bg-myblue-100">
        {workInterval.project ? workInterval.project : 'none'}
      </div>
      <div on:click={() => {selectWorkInterval(workInterval)}} class="work-interval-field text-black cursor-pointer hover:bg-myblue-100">
        {workInterval.worker ? workInterval.worker : 'none'}
      </div>
      <div on:click={() => {selectWorkInterval(workInterval)}} class="work-interval-field text-black cursor-pointer hover:bg-myblue-100">
        {workInterval.start.split('.')[0].replace('T', ' ')}
      </div>
      <div on:click={() => {selectWorkInterval(workInterval)}} class="work-interval-field text-black cursor-pointer hover:bg-myblue-100">
        {workInterval.stop.split('.')[0].replace('T', ' ')}
      </div>
      <div on:click={() => {selectWorkInterval(workInterval)}} class="work-interval-field text-black cursor-pointer hover:bg-myblue-100">
        {workInterval.hhmm}
      </div>
    {/each}
  </div>
  <div>
<!--    <WorkIntervalView></WorkIntervalView>-->
  </div>
</div>
