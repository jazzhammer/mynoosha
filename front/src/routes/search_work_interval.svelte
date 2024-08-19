<style>
  .search-work-interval {
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
  import {type WorkInterval} from '../models/work_interval';
  import WorkIntervalService from "../services/work_interval.service";
  import WorkIntervalList from './project_list.svelte';

  let searchClientName = '';
  $: searchClientName

  let searchWorkIntervalName = '';
  $: searchWorkIntervalName

  let searchYmdStart = new Date();
  searchYmdStart.setMonth(searchYmdStart.getMonth() - 1);
  searchYmdStart.setDate(1);

  let searchYmdFinish = new Date();
  searchYmdFinish.setMonth(searchYmdFinish.getMonth() + 1);
  searchYmdFinish.setDate(0);

  export let foundWorkIntervals = (founds: WorkInterval[]) => {
    console.log(`foundWorkIntervals: ${founds ? founds.length : 'none'}`);
  }

  let workIntervals: WorkInterval[];
  $: workIntervals

  let searchYmdStartString = searchYmdStart.toISOString().split('T')[0];
  $: searchYmdStartString
  const selectYmdStart = (next: string): void => {
    searchYmdStartString = next;
    executeSearchWorkInterval();
  }

  let searchYmdFinishString = searchYmdFinish.toISOString().split('T')[0];
  $: searchYmdFinishString
  const selectYmdFinish = (next: string): void => {
    searchYmdFinishString = next;
    executeSearchWorkInterval();
  }

  const executeSearchWorkInterval = (): void => {
    WorkIntervalService.find({
      created_from: searchYmdStartString,
      created_through: searchYmdFinishString,
    }).then((response: any) => {
      workIntervals = response.data;
      foundWorkIntervals(workIntervals);
    });
  }

  let timeoutSearchWorkInterval: any;
  const searchWorkInterval = (): void => {
    if (timeoutSearchWorkInterval) {
      clearTimeout(timeoutSearchWorkInterval);
    }
    timeoutSearchWorkInterval = setTimeout(() => {
      executeSearchWorkInterval();
    }, 300);
  }

  const keyupFrom = (): void => {
    searchWorkInterval();
  }
  const keyupThrough = (): void => {
    searchWorkInterval();
  }
</script>
<div class="search-work-interval">
  <div class="flex flex-row search-row" style="max-width: 400px; margin: auto;">
    <div>created from</div>
    <Ymd initialYmd={searchYmdStart} selectYmd={selectYmdStart} keyup={keyupFrom}></Ymd>
    <div>through</div>
    <Ymd initialYmd={searchYmdFinish} selectYmd={selectYmdFinish} keyup={keyupThrough}></Ymd>
  </div>
</div>