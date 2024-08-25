<style>
  .project-view {
    display: flex;
    flex-direction: column;
  }

  .project-demogs {
    display: grid;
    grid-template-columns: 1fr 1fr;
    max-width: 350px;
  }
  .work-intervals {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }

  .work-intervals-assigned {
    border: 1px solid #ddddff;
  }

  .work-intervals-other {
    border: 1px solid #ddddff;
  }

  .work-pieces {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }

  .work-pieces-assigned {
    border: 1px solid #ddddff;
  }

  .work-pieces-other {
    border: 1px solid #ddddff;
  }

  .work-milestones {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }

  .work-milestones-assigned {
    border: 1px solid #ddddff;
  }

  .work-milestones-other {
    border: 1px solid #ddddff;
  }
  .menu-item {
    padding-left: 4px;
    padding-right: 4px;
    min-width: 80px;
    text-align: center;
    background-color: antiquewhite;
    cursor: pointer;
    border-radius: 2px;
    color: #3b1000;
    margin: 3px;
    font-size: 10pt;
    height: 23px;
    margin-left: 12px;
  }
  .menu-item:hover {
    border: 1px solid #501a00;
  }

</style>
<script lang="ts">
  import WorkIntervalList from './work_interval_list.svelte';
  import WorkPieceList from './work_piece_list.svelte';

  import SearchWorkInterval from './search_work_interval.svelte';
  import SearchWorkPiece from './search_work_piece.svelte';
  import {
    crud,
    MessageStore,
    type ProjectCrud,
    ProjectStore,
    type WorkIntervalCrud,
    WorkIntervalStore, WorkMilestoneStore,
    WorkPieceStore
  } from "../stores";
  import type {Project} from "../models/project";
  import {onDestroy} from "svelte";
  import ProjectWorkIntervals from './project_work_intervals.svelte';
  import ProjectWorkPieces from './project_work_pieces.svelte';

  import type {WorkInterval} from "../models/work_interval";
  import WorkIntervalService from "../services/work_interval.service";
  import type {WorkPiece} from "../models/work_piece";
  import WorkPieceService from "../services/work_piece.service";
  import SearchClient from './search-client.svelte';
  import type {Client} from "../models/client";
  import ClientList from './client_list.svelte';
  import ProjectService from "../services/project.service";
  import SearchAgreement from './search-agreement.svelte';
  import type {Agreement} from "../models/agreement";
  import AgreementList from './agreement_list.svelte';
  import ClientService from "../services/client.service";
  import ProjectWorkMilestones from './project_work_milestones.svelte';
  import SearchWorkMilestone from './search_work_milestone.svelte';
  import type {WorkMilestone} from "../models/work_milestone";
  import WorkMilestoneList from './work_milestone_list.svelte';
  import WorkMilestoneService from "../services/work_milestone.service";

  import NewWorkMilestone from './new_work_milestone.svelte';
  import TimeRecorder from './time_recorder.svelte';

  let project: Project;
  $: project

  let client: Client;
  $: client

  let unsubProject = ProjectStore.subscribe((pcrud: ProjectCrud) => {
    if (pcrud && (pcrud.type===crud.READ || pcrud.type===crud.CREATE)) {
      if (!Array.isArray(pcrud.payload) ) {
        project = pcrud.payload;
        if (project.client) {
          ClientService.find({id: project.client}).then((response: any) => {
            // console.log(`load client for project: ${JSON.stringify(response.data)}`);
            client = response.data;
          });
        }
      }
    }
  });
  onDestroy(unsubProject);

  let otherWorkMilestones: WorkMilestone[];
  $: otherWorkMilestones

  let otherWorkPieces: WorkPiece[];
  $: otherWorkPieces

  let otherWorkIntervals: WorkInterval[];
  $: otherWorkIntervals

  let unsubWorkInterval = WorkIntervalStore.subscribe((wicrud: WorkIntervalCrud) => {
    if (wicrud && (wicrud.type === crud.READ || wicrud.type === crud.CREATE || wicrud.type === crud.UPDATE)) {
      if (!Array.isArray(wicrud.payload) ) {
        const nextWorkInterval = wicrud.payload;
        if (otherWorkIntervals) {
          const i = otherWorkIntervals.findIndex((wi: WorkInterval) => {
            return wi.id === nextWorkInterval.id;
          })
          if (i >= 0) {
            const nextOtherWorkIntervals = structuredClone(otherWorkIntervals);
            nextOtherWorkIntervals[i] = nextWorkInterval;
            otherWorkIntervals = nextOtherWorkIntervals;
          }
        }
      }
    }
  });
  onDestroy(unsubWorkInterval);

  const foundWorkMilestones = (founds: WorkMilestone[]): void => {
    otherWorkMilestones = founds;
    MessageStore.set({
      type: '',
      message: `found work pieces: ${otherWorkMilestones ? otherWorkMilestones.length : 'none'}`
    });
  }

  const foundWorkPieces = (founds: WorkPiece[]): void => {
    otherWorkPieces = founds;
    MessageStore.set({
      type: '',
      message: `found work pieces: ${otherWorkPieces ? otherWorkPieces.length : 'none'}`
    });
  }

  const foundWorkIntervals = (founds: WorkInterval[]): void => {
    otherWorkIntervals = founds;
    MessageStore.set({
      type: '',
      message: `found work intervals: ${otherWorkIntervals ? otherWorkIntervals.length : 'none'}`
    });
  }

  const selectWorkMilestone = (next: WorkMilestone): void => {
    MessageStore.set({
      type: '',
      message: `selected workMilestone: ${next.id}`
    });
    if (project) {
      next.project = project.id;
      WorkMilestoneService.update(next).then((response: any) => {
        const updated = response.data;
        WorkMilestoneStore.set({
          type: crud.UPDATE,
          payload: updated
        })
      });
    }
  }

  const selectWorkPiece = (next: WorkPiece): void => {
    MessageStore.set({
      type: '',
      message: `selected workPiece: ${next.id}`
    });
    if (project) {
      next.project = project.id;
      WorkPieceService.update(next).then((response: any) => {
        const updated = response.data;
        WorkPieceStore.set({
          type: crud.UPDATE,
          payload: updated
        })
      });
    }
  }

  const selectWorkInterval = (next: WorkInterval): void => {
    MessageStore.set({
      type: '',
      message: `selected workInterval: ${next.id}`
    });
    if (project) {
      next.project = project.id;
      WorkIntervalService.update(next).then((response: any) => {
        const updated = response.data;
        WorkIntervalStore.set({
          type: crud.UPDATE,
          payload: updated
        })
      });
    }
  }
  let showClientSelector = false;
  $: showClientSelector
  const toggleClientSelector = (): void => {
    showClientSelector = !showClientSelector;
    if (showClientSelector) {
      showAgreementSelector = false;
    }
  }

  let showAgreementSelector = false;
  $: showAgreementSelector
  const toggleAgreementSelector = (): void => {
    showAgreementSelector = !showAgreementSelector;
    if (showAgreementSelector) {
      showClientSelector = false;
    }
  }

  let assignableClients: Client[];
  $: assignableClients

  const foundClients = (next: Client[]): void => {
    assignableClients = next;
  }

  let assignableAgreements: Agreement[];
  $: assignableAgreements

  const foundAgreements = (next: Agreement[]): void => {
    assignableAgreements = next;
  }

  const setProjectAgreement = (next: Agreement): void => {
    showAgreementSelector = false;
    if (project) {
      project.agreement = next.id;
      ProjectService.update(project).then((response: any) =>{
        const updated = response.data;
        project = updated;
        ProjectStore.set({
          type: crud.UPDATE,
          payload: updated
        });
      });
    }
  }

  const setProjectClient = (next: Client): void => {
    showClientSelector = false;
    client = next;
    if (project) {
      project.client = next.id;
      ProjectService.update(project).then((response: any) =>{
        const updated = response.data;
        project = updated;
        ProjectStore.set({
          type: crud.UPDATE,
          payload: updated
        });
      });
    }
  }

  let showNewWorkMilestone = false;
  const toggleNewWorkMilestone = (): void => {
    showNewWorkMilestone = !showNewWorkMilestone;
  }

  let createdWorkMilestone = (next: WorkMilestone): void => {
    WorkMilestoneStore.set({
      type: crud.CREATE,
      payload: next
    });
    showNewWorkMilestone = false;
  }

  let showTimeRecorder = false;
  $: showTimeRecorder
  const toggleTimeRecorder = (): void => {
    showTimeRecorder = !showTimeRecorder;
  }
</script>
{#if project}
<div class="project-view">
  <div class="bg-mymid_white flex flex-row pl-2">
    <div class="mr-5">project: {project?.name} [{project?.id}]</div>
    <div  on:click={toggleClientSelector}
          class="mr-5 pl-2 pr-2 cursor-pointer hover:bg-myblue-500 hover:text-myhigh_white">
          client: {project?.client ? `[${project?.client}] ${client?.name}` : 'none'}
    </div>
    {#if showClientSelector}
    <div class="mr-5" style="position: relative;">
      <SearchClient foundClients={foundClients}></SearchClient>
      {#if assignableClients}
        <div class="bg-myhigh_white border border-2 border-myblue-500" style="position: absolute; top: 24px; left: -2px;">
          <ClientList clients={assignableClients} selectClient={setProjectClient}></ClientList>
        </div>
      {/if}
    </div>
    {/if}
    {#if client}
    <div on:click={toggleAgreementSelector} class="mr-5 pl-2 pr-2 cursor-pointer hover:bg-myblue-500 hover:text-myhigh_white">
      agreement: {project?.agreement ? project?.agreement : 'none'}
    </div>
    {/if}
    {#if showAgreementSelector && client}
      <div class="mr-5" style="position: relative;">
        <SearchAgreement client={client} foundAgreements={foundAgreements}></SearchAgreement>
        {#if assignableAgreements}
          <div class="bg-myhigh_white border border-2 border-myblue-500" style="position: absolute; top: 24px; left: -2px;">
            <AgreementList agreements={assignableAgreements} selectAgreement={setProjectAgreement}></AgreementList>
          </div>
        {/if}
      </div>
    {/if}
  </div>
  <div class="project-demogs text-left ml-2">
    <div>id</div><div>{project?.id}</div>
    <div>name</div><div>{project?.name}</div>
    <div>description</div><div>{project?.description}</div>
    <div>agreement_id</div><div>{project?.agreement}</div>
<!--    <div>client_id</div><div>{project?.client}</div>-->
    <div>created</div><div>{project?.created?.split("T")[0]}</div>
  </div>
  <div class="bg-mymid_white flex flex-row">
    <div>work intervals</div>
    <div on:click={toggleTimeRecorder} class="text-center ml-4 pt-1 px-5 cursor-pointer hover:border-myroon-900 hover:text-white hover:bg-blue-800">
      <svg style="margin: auto;" xmlns="http://www.w3.org/2000/svg" width="1em" height="1em" viewBox="0 0 14 14" {...$$props}>
        <g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9.5 8.5a1.5 1.5 0 1 0 0-3a1.5 1.5 0 0 0 0 3m-5 0a1.5 1.5 0 1 0 0-3a1.5 1.5 0 0 0 0 3m0 0h5" />
          <path d="M4.145 12.84a6.5 6.5 0 1 0-2.556-2.238m2.556 2.239L.5 13.5l1.089-2.897m2.556 2.238l.005-.001m-2.561-2.237l.001-.003" />
        </g>
      </svg>
    </div>
  </div>
  <div class="work-intervals">
    {#if showTimeRecorder && client}
      <TimeRecorder client={client} project={project}></TimeRecorder>
      <div></div>
    {/if}
    <div class="flex flex-col m-2 work-intervals-assigned">
      <div class="text-mywood-900" style="height: 72px; padding-top: 23px;">assigned to project</div>
      <ProjectWorkIntervals project={project}></ProjectWorkIntervals>
    </div>
    <div class="flex flex-col m-2 work-intervals-other">
      <div class="text-mywood-900">search other work intervals</div>
      <SearchWorkInterval foundWorkIntervals={foundWorkIntervals}></SearchWorkInterval>
      {#if otherWorkIntervals && otherWorkIntervals.length > 0}
        <div class="text-left pl-2 w-full text-mywood-900">select to assign to project:</div>
        <WorkIntervalList selectWorkInterval={selectWorkInterval}
                          workIntervals={otherWorkIntervals}>
        </WorkIntervalList>
      {/if}
    </div>
  </div>
  <div class="bg-mymid_white">work pieces</div>
  <div class="work-pieces">
    <div class="flex flex-col m-2 work-pieces-assigned">
      <div class="text-mywood-900" style="height: 72px; padding-top: 23px;">assigned to project</div>
      <ProjectWorkPieces project={project}></ProjectWorkPieces>
    </div>
    <div class="flex flex-col m-2 work-pieces-other">
      <div class="text-mywood-900">search other work pieces</div>
      <SearchWorkPiece foundWorkPieces={foundWorkPieces}></SearchWorkPiece>
      {#if otherWorkPieces && otherWorkPieces.length > 0}
        <div class="text-left pl-2 w-full text-mywood-900">select to assign to project:</div>
        <WorkPieceList selectWorkPiece={selectWorkPiece}
                          workPieces={otherWorkPieces}>
        </WorkPieceList>
      {/if}
    </div>
  </div>
  <div class="bg-mymid_white flex flex-row"
  >
    <div class="ml-2">work milestones</div>
    <div
      style="position: relative"
    >
      {#if client && project}
        <div  on:click={toggleNewWorkMilestone}
              class="ml-2 cursor-pointer menu-item"
        >
          <div>new</div>
        </div>
      {/if}
      {#if showNewWorkMilestone}
        <div class="border border-2 border-myblue-500 bg-myhigh_white"
             style="text-align: left; position: absolute; top: 28px; left: 12px; width: 700px; z-index: 1000;"
        >
          <NewWorkMilestone client={client} project={project} createdWorkMilestone={createdWorkMilestone}></NewWorkMilestone>
        </div>
      {/if}
    </div>
  </div>
  <div class="work-milestones">
    <div class="flex flex-col m-2 work-milestones-assigned">
      <div class="text-mywood-900" style="height: 72px; padding-top: 23px;">assigned to project</div>
      <ProjectWorkMilestones project={project}></ProjectWorkMilestones>
    </div>
    <div class="flex flex-col m-2 work-milestones-other">
      <div class="text-mywood-900">search other work milestones</div>
      <SearchWorkMilestone foundWorkMilestones={foundWorkMilestones}></SearchWorkMilestone>
      {#if otherWorkMilestones && otherWorkMilestones.length > 0}
        <div class="text-left pl-2 w-full text-mywood-900">select to assign to project:</div>
        <WorkMilestoneList selectWorkMilestone={selectWorkMilestone}
                       workMilestones={otherWorkMilestones}>
        </WorkMilestoneList>
      {/if}
    </div>
  </div>
</div>
{/if}
