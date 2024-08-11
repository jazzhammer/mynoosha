<style>
  .client-form-fields {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    width: 100%;
    margin-left: 3px;
  }

  .edit-project-menu {
    display: flex;
    flex-direction: row;
  }

  .client-form-fields > * {
    margin-bottom: 2px;
  }

  .new-project {
    font-size: 9pt;
  }

  .menu-item {
    color: black;
    margin-left: 2px;
    margi-right: 2px;
  }

  .projectable-work-intervals {
    display: grid;
    grid-template-columns: 1fr 4fr 2fr 10fr;
    color: black;
    font-size: 9pt;
  }
</style>
<script lang="ts">

  import {
    type ClientCrud,
    ClientStore,
    crud,
    type ProjectCrud,
    ProjectStore, WorkTypeStore,
  } from "../stores";

  import { DatePicker } from "@svelte-plugins/datepicker";
  import { format } from 'date-fns';
  import {type Client} from "../models/client";
  import {onDestroy} from "svelte";
  import ProjectService from "../services/project.service";
  import {type Project} from "../models/project";
  import WorkIntervalService from "../services/work_interval.service";
  import type {WorkInterval} from "../models/work_interval";
  import WorkTypeService from "../services/work_type.service";
  import type {WorkType} from "../models/work_type";

  let startDate = new Date();
  $: startDate
  let dateFormat = 'yyyy-MM-dd';
  let isOpen = false;

  const toggleDatePicker = () => (isOpen = !isOpen);

  const formatDate = (dateString: Date) => {
    return dateString && format(new Date(dateString), dateFormat) || '';
  };

  let formattedYmdIssue = formatDate(startDate);

  let client: Client;
  $: client
  const unsubClient = ClientStore.subscribe((ccrud: ClientCrud) => {
    if (!Array.isArray(ccrud.payload)) {
      client = ccrud.payload as Client;
    }
  });
  onDestroy(unsubClient)
  let project: Project;
  $: project
  const unsubProject = ProjectStore.subscribe((icrud: ProjectCrud) => {
    if (icrud) {
      if (!Array.isArray(icrud.payload)) {
        project = icrud.payload as Project;

        startDate = new Date(project.created);
        formattedYmdIssue = formatDate(startDate);
      }
    }
  });
  onDestroy(unsubProject)
  $: formattedYmdIssue = formatDate(startDate);
  function updateProject(): void {
    project.created = (new Date(formattedYmdIssue)).toUTCString();
    ProjectService.update({

    }).then((response: any) => {
      const created = response.data;
      ProjectStore.set({
        type: crud.CREATE,
        payload: created
      });
    })
  }

  let mode = 'projectd-items';
  $: mode
  function setMode(next: string): void {
    mode = next;
  }

  let projectableWorkIntervals: WorkInterval[];
  $: projectableWorkIntervals
  let projectableChecks: boolean[] = [];
  $: projectableChecks

  let workTypes: WorkType[] = [];
  $: workTypes
  let workTypesByName: {[key: string]: WorkType} = {};
  $: workTypesByName


  let projectablesToAdd = 0;
  $: projectablesToAdd
  function countProjectablesToAdd(next: WorkInterval): number {
    debugger;
    projectableChecks[next.id] = !projectableChecks[next.id];
    let trues = 0;
    projectableChecks.forEach((checked: boolean) => {
      trues += checked ? 1 : 0;
    })
    projectablesToAdd = trues;
    return trues;
  }


</script>
<div class="new-project flex flex-col border-myroon-100 border p-3 mr-6 ml-3 rounded w-full text-myhigh_white"
     style="min-width: 226px; max-width: 375px; font-size: 10pt;" data-testid="edit_project"
>
  <div class="bg-mywood-900 rounded mb-5 w-full" data-testid="edit_project_header" id="edit_project_header">edit project</div>
  <div class="client-form-fields text-mywood-900" data-testid="edit_project_form">
    <div><div class="" data-testid="edit_project_name">ymd issue:</div></div>
    <div>
      <DatePicker bind:isOpen bind:startDate enableFutureDates={true}>
        <input type="text"
               placeholder="Select ymd issue"
               bind:value={formattedYmdIssue}
               on:click={toggleDatePicker}
               style="width: 100px; font-size: 9pt; height: 18px; text-align: center;"
        />
      </DatePicker>
    </div>
    <div><div class="" data-testid="edit_project_name">ymd create:</div></div>
    <div>{project.created.substring(0, project.created.indexOf(' '))}</div>
  </div>
  <div class="edit-project-menu flex flex-row ml-3 mb-3 mt-4">
    {#if mode!=='projectd-items'}
      <div on:click={() => {setMode('projectd-items')}}
           on:keyup={() => {}}
           tabindex="0"
           role="button"
           class="menu-item border border-t-1 rounded-md border-l-1 border-r-1 border-myblue-500 cursor-pointer hover:border-myblue-500 pl-6 pr-6"
           style="width:150px;"
      >
        projectd-items
      </div>
    {/if}
    {#if mode!=='projectables'}
      <div on:click={() => {setMode('projectables')}}
           on:keyup={() => {}}
           tabindex="0"
           role="button"
           class="menu-item border border-t-1 rounded-md border-l-1 border-r-1 border-myblue-500 cursor-pointer hover:border-myblue-500 pl-6 pr-6">
        projectables
      </div>
    {/if}
    {#if mode!=='payments'}
      <div on:click={() => {setMode('payments')}}
           on:keyup={() => {}}
           tabindex="0"
           role="button"
           class="menu-item border border-t-1 rounded-md border-l-1 border-r-1 border-myblue-500 cursor-pointer hover:border-myblue-500 pl-6 pr-6">
        payments
      </div>
    {/if}
  </div>
  {#if mode==='projectables'}
    <div class="bg-mywood-100 rounded mb-5 w-full"
         data-testid="edit_project_header"
         id="projectables_header">projectables</div>
    {#if projectableWorkIntervals}
    <div class="projectable-work-intervals">
      {#each projectableWorkIntervals as projectable}
        <div><input type="checkbox"
          on:click={() => countProjectablesToAdd(projectable)}
        ></div>
        <div class="hover:bg-myblue-100 cursor-pointer">{projectable.start.substring(0, projectable.start.indexOf('T'))}</div>
        <div class="hover:bg-myblue-100 cursor-pointer">{projectable.hhmm}</div>
        <div class="hover:bg-myblue-100 cursor-pointer">{projectable.description}</div>
      {/each}
    </div>
    {/if}
  {/if}
</div>
