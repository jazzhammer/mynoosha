<style>
  .search-project {
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
  import {type Project} from './../models/project.js';
  import ProjectService from "../services/project.service";
  import ProjectList from './project_list.svelte';

  let searchClientName = '';
  $: searchClientName

  let searchProjectName = '';
  $: searchProjectName

  let searchYmdStart = new Date();
  searchYmdStart.setMonth(searchYmdStart.getMonth() - 1);
  searchYmdStart.setDate(1);

  let searchYmdFinish = new Date();
  searchYmdFinish.setMonth(searchYmdFinish.getMonth() + 1);
  searchYmdFinish.setDate(0);

  export let foundProjects = (founds: Project[]) => {
    console.log(`foundProjects: ${founds ? founds.length : 'none'}`);
  }

  let projects: Project[];
  $: projects

  let searchYmdStartString = searchYmdStart.toISOString().split('T')[0];
  $: searchYmdStartString
  const selectYmdStart = (next: string): void => {
    searchYmdStartString = next;
    executeSearchProject();
  }

  let searchYmdFinishString = searchYmdFinish.toISOString().split('T')[0];
  $: searchYmdFinishString
  const selectYmdFinish = (next: string): void => {
    searchYmdFinishString = next;
    executeSearchProject();
  }

  const executeSearchProject = (): void => {
    ProjectService.find({
      created_from: searchYmdStartString,
      created_through: searchYmdFinishString,
      client_name: searchClientName,
      name: searchProjectName
    }).then((response: any) => {
      const founds = response.data;
      projects = founds;
    });
  }

  let timeoutSearchProject: any;
  const searchProject = (): void => {
    if (timeoutSearchProject) {
      clearTimeout(timeoutSearchProject);
    }
    timeoutSearchProject = setTimeout(() => {
      executeSearchProject();
    }, 300);
  }
</script>
<div class="search-project">
  <div class="flex flex-row search-row">
    <div>client</div>
    <div>name</div>
    <div>created</div>
  </div>
  <div class="search-row">
    <div style="padding-top: 2px;"><input on:keyup={searchProject} bind:value={searchClientName} type="text" style="width: 100%; min-width:50px; height: 18px;"/></div>
    <div style="padding-top: 2px;"><input on:keyup={searchProject} bind:value={searchProjectName} type="text" style="width: 100%; min-width:50px; height: 18px"/></div>
    <div class="flex flex-row">
      <Ymd initialYmd={searchYmdStart} selectYmd={selectYmdStart}></Ymd>
      <Ymd initialYmd={searchYmdFinish} selectYmd={selectYmdFinish}></Ymd>
    </div>
  </div>
<!--  <ProjectList projects={projects}></ProjectList>-->
</div>