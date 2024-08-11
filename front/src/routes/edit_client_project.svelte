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

  .field-label {
    text-align: left;
    width: 110px;
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
    type ProjectCrud, ProjectItemStore,
    ProjectStore,
    WorkIntervalListsByClient, WorkTypeStore
  } from "../stores";

  import { DatePicker } from "@svelte-plugins/datepicker";
  import { format } from 'date-fns';
  import {type Client} from "../models/client";
  import {onDestroy} from "svelte";
  import ProjectService from "../services/project.service";
  import {type Project} from "../models/project";
  import WorkIntervalService from "../services/work_interval.service";
  import type {WorkInterval} from "../models/work_interval";
  import ProjectItemService from "../services/project_item.service";
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

        startDate = new Date(project.issued);
        formattedYmdIssue = formatDate(startDate);
      }
    }
  });
  onDestroy(unsubProject)
  $: formattedYmdIssue = formatDate(startDate);
  function updateProject(): void {
    project.issued = (new Date(formattedYmdIssue)).toUTCString();
    ProjectService.update({
      client: client.id,
      issued: project.issued
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
    if (mode === 'projectables') {
      retrieveProjectables();
    }
  }

  let projectableWorkIntervals: WorkInterval[];
  $: projectableWorkIntervals
  let projectableChecks: boolean[] = [];
  $: projectableChecks

  function retrieveProjectables(): void {
    projectableChecks = [];
    WorkIntervalService.find({
      client: client.id,
      project_item: 'isnull'
    }).then((response: any) => {
      // debugger;
      const founds = response.data;
      projectableWorkIntervals = founds
      projectableWorkIntervals.forEach((interval: WorkInterval) => {
        projectableChecks[interval.id] = false;
      });
    });
  }

  let workTypes: WorkType[] = [];
  $: workTypes
  let workTypesByName: {[key: string]: WorkType} = {};
  $: workTypesByName
  function retrieveWorkTypes(): void {
    WorkTypeService.find({}).then((response: any) => {
      workTypes = response.data;
      workTypesByName = {}
      workTypes.forEach((wt: WorkType) => {
        workTypesByName[wt.name] = wt;
      });
      WorkTypeStore.set({
        type: crud.READ,
        payload: workTypes
      });
    });
  }

  function addProjectables(): void {
    const work_type = workTypesByName['time'];
    projectableWorkIntervals.forEach((wi: WorkInterval) => {
      if (projectableChecks[wi.id]) {
        ProjectItemService.create({
          project: project.id,
          work_interval: wi.id,
          work_type: work_type.id
        }).then((response: any) => {
          const created = response.data;
          if (created) {
            ProjectItemStore.set({
              type: crud.CREATE,
              payload: created
            });
          }
        });
      }
    });
  }

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
    {#if projectablesToAdd > 0}
    <div class="mt-6 text-myhigh_white hover:drop-shadow w-full">
      <button on:click={addProjectables}
              type="button"
              value="create" class="bg-myroon-100 w-6/12 mt-3 rounded hover:border"
              style="margin: auto; width: 220px;"
              data-testid="create_client_button"
      >
        add {projectablesToAdd} projectable{projectablesToAdd && projectablesToAdd === 1 ? '' : 's'} to project
      </button>
    </div>
    {/if}
  {/if}
</div>
