<style>
  .search-project-type {
    display: flex;
    flex-direction: column;
  }
  .search-row {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
  }
</style>
<script lang="ts">
  import Ymd from './ymd.svelte';
  import {type ProjectType} from '../models/project_type';
  import ProjectTypeService from "../services/project_type.service";
  import ProjectTypeList from './project_type_list.svelte';

  let searchClientName = '';
  $: searchClientName

  let searchProjectTypeName = '';
  $: searchProjectTypeName

  let searchYmdStart = new Date();
  searchYmdStart.setMonth(searchYmdStart.getMonth() - 1);
  searchYmdStart.setDate(1);

  let searchYmdFinish = new Date();
  searchYmdFinish.setMonth(searchYmdFinish.getMonth() + 1);
  searchYmdFinish.setDate(0);

  export let foundProjectTypes = (founds: ProjectType[]) => {
    console.log(`foundProjectTypes: ${founds ? founds.length : 'none'}`);
  }

  let projectTypes: ProjectType[];
  $: projectTypes

  let searchYmdStartString = searchYmdStart.toISOString().split('T')[0];
  $: searchYmdStartString
  const selectYmdStart = (next: string): void => {
    searchYmdStartString = next;
    executeSearchProjectType();
  }

  let searchYmdFinishString = searchYmdFinish.toISOString().split('T')[0];
  $: searchYmdFinishString
  const selectYmdFinish = (next: string): void => {
    searchYmdFinishString = next;
    executeSearchProjectType();
  }

  const executeSearchProjectType = (): void => {
    ProjectTypeService.find({
      name: searchProjectTypeName
    }).then((response: any) => {
      const founds = response.data;
      projectTypes = founds;
    });
  }

  let timeoutSearchProjectType: any;
  const searchProjectType = (): void => {
    if (timeoutSearchProjectType) {
      clearTimeout(timeoutSearchProjectType);
    }
    timeoutSearchProjectType = setTimeout(() => {
      executeSearchProjectType();
    }, 300);
  }
</script>
<div class="search-project-type">
  <div class="flex flex-row search-row">
    <div>client</div>
    <div>name</div>
    <div>created</div>
  </div>
  <div class="search-row">
    <div><input on:keyup={searchProjectType} bind:value={searchClientName} type="text" style="width: 100%; min-width:50px; "/></div>
    <div><input on:keyup={searchProjectType} bind:value={searchProjectTypeName} type="text" style="width: 100%; min-width:50px; "/></div>
    <div class="flex flex-row">
      <Ymd initialYmd={searchYmdStart} selectYmd={selectYmdStart}></Ymd>
      <Ymd initialYmd={searchYmdFinish} selectYmd={selectYmdFinish}></Ymd>
    </div>
  </div>
  <ProjectTypeList projectTypes={projectTypes}></ProjectTypeList>
</div>