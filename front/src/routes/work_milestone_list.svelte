<style>
  .work-milestone-list {
    display: grid;
    grid-template-columns: 1fr 2fr 2fr 2fr 5fr;
    font-size: 9pt;
    max-width: 800px;
  }
  .work-milestone-list-header {
    text-align: center;
    color: black;
    font-weight: bold;
    font-size: 9pt;
  }
  .work-milestone-field {
    text-align: center;
  }
</style>

<script lang="ts">
  import {type WorkMilestone} from '../models/work_milestone';
  // import WorkMilestoneView from './work_milestone_view.svelte';

  export let workMilestones: WorkMilestone[] = [];

  export let selectWorkMilestone: (workMilestone: WorkMilestone) => void;



</script>
<div class="flex flex-col">
  <div class="work-milestone-list w-full border border-myblue-50">
    <div class="work-milestone-list-header bg-mylow_white">id</div>
    <div class="work-milestone-list-header bg-mylow_white">client</div>
    <div class="work-milestone-list-header bg-mylow_white">project</div>
    <div class="work-milestone-list-header bg-mylow_white">worker</div>
    <div class="work-milestone-list-header bg-mylow_white">achieved</div>

    {#each workMilestones as workMilestone}
      <div on:click={() => {selectWorkMilestone(workMilestone)}} class="work-milestone-field text-black cursor-pointer hover:bg-myblue-100">
        {workMilestone.id}
      </div>
      <div on:click={() => {selectWorkMilestone(workMilestone)}} class="work-milestone-field text-black cursor-pointer hover:bg-myblue-100">
        {workMilestone.client ? workMilestone.client : 'none'}
      </div>
      <div on:click={() => {selectWorkMilestone(workMilestone)}} class="work-milestone-field text-black cursor-pointer hover:bg-myblue-100">
        {workMilestone.project ? workMilestone.project : 'none'}
      </div>
      <div on:click={() => {selectWorkMilestone(workMilestone)}} class="work-milestone-field text-black cursor-pointer hover:bg-myblue-100">
        {workMilestone.worker ? workMilestone.worker : 'none'}
      </div>
      <div on:click={() => {selectWorkMilestone(workMilestone)}} class="work-milestone-field text-black cursor-pointer hover:bg-myblue-100">
        {workMilestone.start ? workMilestone.start.split('.')[0].replace('T', ' ') : 'not achieved  '}
      </div>
    {/each}
  </div>
  <div>
<!--    <WorkMilestoneView></WorkMilestoneView>-->
  </div>
</div>
