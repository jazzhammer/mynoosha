<style>
  .search-work-milestone {
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
  import {type WorkMilestone} from '../models/work_milestone';
  import WorkMilestoneService from "../services/work_milestone.service";
  import WorkMilestoneList from './project_list.svelte';

  let searchClientName = '';
  $: searchClientName

  let searchWorkMilestoneName = '';
  $: searchWorkMilestoneName

  let searchYmdStart = new Date();
  searchYmdStart.setMonth(searchYmdStart.getMonth() - 1);
  searchYmdStart.setDate(1);

  let searchYmdFinish = new Date();
  searchYmdFinish.setMonth(searchYmdFinish.getMonth() + 1);
  searchYmdFinish.setDate(0);

  export let foundWorkMilestones = (founds: WorkMilestone[]) => {
    console.log(`foundWorkMilestones: ${founds ? founds.length : 'none'}`);
  }

  let workMilestones: WorkMilestone[];
  $: workMilestones

  let searchYmdStartString = searchYmdStart.toISOString().split('T')[0];
  $: searchYmdStartString
  const selectYmdStart = (next: string): void => {
    searchYmdStartString = next;
    executeSearchWorkMilestone();
  }

  let searchYmdFinishString = searchYmdFinish.toISOString().split('T')[0];
  $: searchYmdFinishString
  const selectYmdFinish = (next: string): void => {
    searchYmdFinishString = next;
    executeSearchWorkMilestone();
  }

  const executeSearchWorkMilestone = (): void => {
    WorkMilestoneService.find({
      pre_start: searchYmdStartString,
      post_start: searchYmdFinishString,
    }).then((response: any) => {
      workMilestones = response.data;
      foundWorkMilestones(workMilestones);
    });
  }

  let timeoutSearchWorkMilestone: any;
  const searchWorkMilestone = (): void => {
    if (timeoutSearchWorkMilestone) {
      clearTimeout(timeoutSearchWorkMilestone);
    }
    timeoutSearchWorkMilestone = setTimeout(() => {
      executeSearchWorkMilestone();
    }, 300);
  }

  const keyupFrom = (): void => {
    searchWorkMilestone();
  }
  const keyupThrough = (): void => {
    searchWorkMilestone();
  }
</script>
<div class="search-work-milestone">
  <div class="flex flex-row search-row" style="max-width: 400px; margin: auto;">
    <div>created from</div>
    <Ymd initialYmd={searchYmdStart} selectYmd={selectYmdStart} keyup={keyupFrom}></Ymd>
    <div>through</div>
    <Ymd initialYmd={searchYmdFinish} selectYmd={selectYmdFinish} keyup={keyupThrough}></Ymd>
  </div>
</div>