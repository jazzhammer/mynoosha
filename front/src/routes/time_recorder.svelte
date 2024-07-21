<style>
  .time-recorder {
    display: flex;
    flex-direction: column;
  }
  .work-interval-list-header-row {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr 3fr;
    font-size: 10pt;
  }
  .work-interval-list-header-row > * {
    text-align: center;
    border-bottom: 1px solid;
  }
  .work-interval-list-row {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr 3fr;
    font-size: 10pt;
  }
  .work-interval-list-row > * {
    text-align: center;
  }
</style>
<script lang="ts">

  import type {Client} from "../models/client";
  import type {WorkInterval} from "../models/work_interval";

  export let client: Client;
  export let workIntervalList: WorkInterval[];

</script>
<div class="border-2 border-myroon-100 rounded text-mywood-900 m-2 time-recorder" style="min-width: 250px; min-height: 200px; max-width: 300px; max-height: 250px;">
  <div class="h-2/12 text-center text-myhigh_white bg-myroon-100">{client.name}</div>
  <div class="work-interval-list-header-row">
    <div class="">start</div>
    <div>stop</div>
    <div>min</div>
    <div>hrs</div>
    <div>description</div>
  </div>
  {#if workIntervalList}
  {#each workIntervalList as workInterval}
  <div class="work-interval-list-row">
    <div class="bg-myhigh_white">{workInterval.start}</div>
    <div class="bg-myhigh_white">{workInterval.stop}</div>
    <div class="bg-myhigh_white">{workInterval.minutes}</div>
    <div class="bg-myhigh_white">{workInterval.hours}</div>
    <div class="bg-myhigh_white">{workInterval.description}</div>
  </div>
  {/each}
  {/if}
</div>