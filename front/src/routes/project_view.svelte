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
    WorkIntervalStore,
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
            client = response.data;
          });
        }
      }
    }
  });
  onDestroy(unsubProject);

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
</script>
{#if project}
<div class="project-view">
  <div class="bg-mymid_white flex flex-row pl-2">
    <div class="mr-5">project: {project?.name} [{project?.id}]</div>
    <div on:click={toggleClientSelector} class="mr-5 pl-2 pr-2 cursor-pointer hover:bg-myblue-500 hover:text-myhigh_white">
      client: {project?.client ? `[${project?.client}] ${project?.name}` : 'none'}
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
  <div class="bg-mymid_white">work intervals</div>
  <div class="work-intervals">
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
</div>
{/if}
