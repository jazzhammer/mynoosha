<style>
  .time-recorder {
    display: flex;
    flex-direction: column;
  }
  .work-interval-list-header-row {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 5fr 1fr 1fr;
    font-size: 9pt;
  }
  .work-interval-list-header-row > * {
    text-align: center;
    border-bottom: 1px solid;
  }
  .work-interval-list-row {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 5fr 1fr 1fr;
    font-size: 9pt;
  }
  .work-interval-list-row > * {
    text-align: center;
  }
  .editor-controls {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }
</style>
<script lang="ts">
  import WorkIntervalDescription from './work_interval_description.svelte';
  import type {Client} from "../models/client";
  import type {WorkInterval} from "../models/work_interval";
  import WorkIntervalService, {type WorkIntervalDto} from "../services/work_interval.service";
  import {DateTime} from "luxon";
  import {onDestroy} from "svelte";
  import {padLeft} from "../utils/numbers.js";
  import markdownify from "../utils/markdown.js";
  import {
    type ClientCrud,
    ClientStore,
    crud,
    type WorkIntervalCrud,
    WorkIntervalListsByClient,
    WorkIntervalStore
  } from "../stores";
  import ProjectService from "../services/project.service";
  import type {Project} from "../models/project";
  import WorkIntervalProject from './work_interval_project.svelte';


  let workIntervalList: WorkInterval[];
  $: workIntervalList

  let workIntervalListsByClient: {[key: number]: WorkInterval[]} = {};
  $: workIntervalListsByClient

  export let client: Client;
  $: client

  export let project: Project;
  $: project

  let editableWorkInterval: WorkInterval | null = null
  $: editableWorkInterval


  // ------------------------------------------------------------
  let firstTimeNow = DateTime.now();
  let newWorkIntervalHH = firstTimeNow.hour;
  let newWorkIntervalMM = firstTimeNow.minute;
  // ------------------------------------------------------------
  // hour- & minute-updater for currently unfinalized WorkInterval
  let tickedHourMinute = '';
  let tickInterval = setInterval(
    () => {
      const now = DateTime.now();
      const hh = padLeft(now.hour, 2)
      const mm = padLeft(now.minute, 2)
      tickedHourMinute = `${hh}:${mm}`;
    }, 1000
  );
  onDestroy(() => {
    clearInterval(tickInterval);
  });



  // ------------------------------------------------------------
  // listen for store events related to Clients:
  const unsubClient = ClientStore.subscribe((ccrud: ClientCrud) => {
    if (ccrud && ccrud.type === crud.READ) {
      if (!Array.isArray(ccrud.payload)) {
        client = ccrud.payload;
        workIntervalList = workIntervalListsByClient[client?.id as unknown as number];
      }
    }
  });
  onDestroy(unsubClient)

  // ------------------------------------------------------------
  // listen for store events related to WorkIntervals:
  // WorkIntervalListsByClient and
  // WorkInterval


  const unsubWorkIntervalLists = WorkIntervalListsByClient.subscribe((lists: {[key: number]: WorkInterval[]}) => {
    // console.log(`WorkIntervalListsByClient event>...`);
    workIntervalListsByClient = lists;
    workIntervalList = workIntervalListsByClient[client?.id as unknown as number];
    // console.log(`workIntervalList now length: ${workIntervalList ? workIntervalList.length : 'none'}`);
  });
  onDestroy(unsubWorkIntervalLists)

  const unsubWorkInterval = WorkIntervalStore.subscribe((wicrud: WorkIntervalCrud) => {
    if (wicrud && wicrud.type === crud.DELETE) {
      const nextWorkInterval = wicrud.payload as WorkInterval;
      if (nextWorkInterval) {
        if (workIntervalList) {
          const index = workIntervalList.findIndex((maybe: WorkInterval) => {
            maybe.id === nextWorkInterval.id;
          });
          if (index > 0) {
            const nextWorkIntervalList = structuredClone(workIntervalList);
            nextWorkIntervalList.splice(index, 1);
            workIntervalList = nextWorkIntervalList;
          }
        }
      }
    } else
    if (wicrud && wicrud.type === crud.UPDATE) {
      // debugger;
      const nextWorkInterval = wicrud.payload as WorkInterval;
      if (workIntervalList) {
        const index = workIntervalList.findIndex((maybe: WorkInterval) => {
          maybe.id === nextWorkInterval.id;
        });
        if (index > 0) {
          const nextWorkIntervalList = structuredClone(workIntervalList);
          nextWorkIntervalList[index] = nextWorkInterval;
          workIntervalList = nextWorkIntervalList;
        }
      } else {
        console.log(`false alarm: no workInterval`)
      }
    }
  });
  onDestroy(unsubWorkInterval)

  function createWorkIntervalForDTISO(dtIso: string): void {
    // console.log(`createWorkIntervalForDTISO(${dtIso})`)
    // debugger;
    const widto: WorkIntervalDto = {
      start: dtIso,
      client: client.id
    }
    if (project) {
      widto['project'] = project.id;
    }
    WorkIntervalService.create(widto).then((response: any) => {
      if (response.data) {
        const created = response.data;

        const isoStart = DateTime.fromISO(created.start, {zone: 'utc'})
        const isoStartLocal = isoStart.toLocal();
        created.localHHMMStart = `${padLeft(isoStartLocal.hour, 2)}:${padLeft(isoStartLocal.minute, 2)}`;

        if (created.stop) {
          const isoStop = DateTime.fromISO(created.stop, {zone: 'utc'})
          const isoStopLocal = isoStop.toLocal();
          created.localHHMMStop = `${padLeft(isoStopLocal.hour, 2)}:${padLeft(isoStopLocal.minute, 2)}`;
          const diff = (created.stop_utcms - created.start_utcms);
          const HH = Math.floor(diff / 3600);
          const MM = Math.floor((diff % 3600) / 60);
          created.hhmm = `${padLeft(HH, 2)}:${padLeft(MM, 2)}`;
        }

        WorkIntervalStore.set({
          type: crud.CREATE,
          payload: created
        });
        // let nextWorkIntervalList = []
        // workIntervalList = workIntervalList ? workIntervalList: [];
        // nextWorkIntervalList = [...workIntervalList, created];
        // workIntervalList = nextWorkIntervalList;
      }
    });
  }

  let debouncedCreateWorkTimeInterval: any;
  function createWorkInterval(keyEvent: any): void {
    if (debouncedCreateWorkTimeInterval) {
      clearTimeout(debouncedCreateWorkTimeInterval);
    }
    if (!keyEvent || (keyEvent.code==='Enter' || keyEvent.code === 'Space')) {
      debouncedCreateWorkTimeInterval = setTimeout(
        () => {
          const dtISO = DateTime.utc().toISO();
          createWorkIntervalForDTISO(dtISO);
        },
        500
      );
    }
  }

  let debounceFinalizeWorkInterval: any;
  function finalizeWorkInterval(workInterval: WorkInterval, keyEvent: any): void {
    if (debounceFinalizeWorkInterval) {
      clearTimeout(debounceFinalizeWorkInterval);
    }
    if (!keyEvent || (keyEvent.code === 'Enter' || keyEvent.code === 'Space')) {
      debounceFinalizeWorkInterval = setTimeout(() => {
        const dtISO = DateTime.utc().toISO();
        WorkIntervalService.update({
          id: workInterval.id,
          start: workInterval.start,
          stop: dtISO,
          description: workInterval.description
        }).then((response: any) => {
          if (response.data) {
            const updated = response.data;

            const isoStart = DateTime.fromISO(updated.start, {zone: 'utc'})
            const isoStartLocal = isoStart.toLocal();
            updated.localHHMMStart = `${padLeft(isoStartLocal.hour, 2)}:${padLeft(isoStartLocal.minute, 2)}`;

            if (updated.stop) {
              console.log(`updated stop: ${updated.stop}`);
              const isoStop = DateTime.fromISO(updated.stop, {zone: 'utc'})
              const isoStopLocal = isoStop.toLocal();
              console.log(`isoStopLocal.hour: ${isoStopLocal.hour}`);
              updated.localHHMMStop = `${padLeft(isoStopLocal.hour,2)}:${padLeft(isoStopLocal.minute, 2)}`;
              const diff = (updated.stop_utcms - updated.start_utcms);
              const HH = Math.floor(diff / 3600);
              const MM = Math.floor((diff % 3600) / 60);
              updated.hhmm = `${padLeft(HH, 2)}:${padLeft(MM, 2)}`;
            }

            let nextWorkIntervalList = []
            const indexToRemove = workIntervalList.findIndex((one: WorkInterval) => {
              return one.id === workInterval.id;
            });
            if (indexToRemove > 0) {
              workIntervalList.splice(indexToRemove, 1);
            }
            workIntervalList = workIntervalList ? workIntervalList: [];
            nextWorkIntervalList = [...workIntervalList, updated];
            workIntervalList = nextWorkIntervalList;
            // console.log(`created workInterval ${JSON.stringify(updated)}`);
          }
        });

      }, 500);
    }
  }

  function openDescription(workInterval: WorkInterval): void {
    editableWorkInterval = workInterval;
    WorkIntervalStore.set({
      type: crud.READ,
      payload: editableWorkInterval
    })
    // find attached project
    ProjectService.find({workInterval: workInterval.id}).then((response: any) => {
      const found = response.data;
      project = found;
    });
  }

  function keyupHHMM(e: any): void {
    if (e.key == 'Enter') {
      const utcNow = DateTime.utc();
      const utcNewWorkInterval = DateTime.fromObject({
        year: utcNow.year,
        month: utcNow.month,
        day: utcNow.day,
        hour: parseInt(''+newWorkIntervalHH),
        minute: parseInt('' + newWorkIntervalMM)
      }).toUTC()
      // debugger;
      createWorkIntervalForDTISO(utcNewWorkInterval.toISO() as string);
    }
  }

  function deleteEditableWorkInterval(): void {
    if (editableWorkInterval) {
      WorkIntervalService.delete(editableWorkInterval).then(() => {
        const deleted = structuredClone(editableWorkInterval)
        editableWorkInterval = null;
        WorkIntervalStore.set({
          type: crud.DELETE,
          payload: deleted as WorkInterval
        });
      });
    }
  }

  let workIntervalProject = false;
  $: workIntervalProject
  const selectWorkIntervalProject = (): void => {
    workIntervalProject = true;
  }

  const updatedWorkInterval = (updated: WorkInterval): void => {
    WorkIntervalStore.set({
      type: crud.UPDATE,
      payload: updated
    });
  }
</script>
{#if client}
  <div class="border-2 border-myroon-100 rounded text-mywood-900 m-2 time-recorder"
       style="min-width: 400px; min-height: 200px; width: 650px; max-height: 250px;">
    <div class="h-4/12 text-center text-myhigh_white bg-myroon-100">{client.name} intervals={!workIntervalList ? '(0)' : workIntervalList?.length}</div>
    <div class="work-interval-list-header-row">
      <div class="">start</div>
      <div>stop</div>
      <div>hh:mm</div>
      <div>description</div>
      <div>invoice</div>
      <div>project</div>
    </div>
    {#if workIntervalList}
      {#each workIntervalList as workInterval, index}
        {#if index > workIntervalList.length - 4}
          <div class="work-interval-list-row">
            <div class="bg-myhigh_white">{workInterval.localHHMMStart}</div>
            <div class="bg-myhigh_white">{workInterval.localHHMMStop ? workInterval.localHHMMStop : `<${tickedHourMinute}>`}</div>
            {#if workInterval.localHHMMStop }
              <div class="bg-myhigh_white">{workInterval.hhmm ? workInterval.hhmm : ''}</div>
            {:else }
              <div class="bg-myhigh_white" style="padding-top: 2px;">
                <div on:click={() => finalizeWorkInterval(workInterval, null)}
                     on:keyup={() => {}}
                     tabindex="0"
                     role="button"
                     class="rounded bg-blue-800 cursor-pointer hover:border-gray-300" style="height:12px; width: 12px; border-radius: 2px; margin: auto;">
                </div>
              </div>
            {/if}
            <div class="bg-myhigh_white hover:bg-myblue-50"
                 on:click={() => openDescription(workInterval)}
                 on:keyup={() => {}}
                 tabindex="0"
                 role="button"
            >{@html markdownify(workInterval.description)}
            </div>
            <div>{workInterval.invoice_item}</div>
            <div on:click={ selectWorkIntervalProject } class="hover:bg-myblue-50 cursor-pointer">{workInterval.project ? workInterval.project : 'none'}</div>
          </div>
        {/if}
      {/each}
    {/if}
    <div class="bg-myblue-100 w-full text-xl cursor-pointer hover:border text-myhigh_white flex flex-row align-middle items-center"
         style="position: relative">
      <div on:click={() => createWorkInterval(null)}
           on:keyup={() => {}}
           tabindex="0"
           role="button"
           style="position:absolute; top: -5px; left: 10px; "
      >
        +
      </div>
      <div class="text-sm ml-10 border-l-mywood-900 flex flex-row">
        <div>or using:</div>
        <div><input type="text" placeholder="hh"
                    class="ml-4 pl-1 text-center"
                    style="width: 48px; height: 14px; font-size: 9pt; color: black"
                    bind:value={newWorkIntervalHH}
                    on:focus={(e) => (e.target?.select())}
                    on:keyup={keyupHHMM}
        />
        </div>
        <div><input type="text" placeholder="mm"
                    class="ml-4 pl-1 text-center"
                    style="width: 48px; height: 14px; font-size: 9pt; color: black"
                    bind:value={newWorkIntervalMM}
                    on:focus={(e) => (e.target?.select())}
                    on:keyup={keyupHHMM}
        />
        </div>
      </div>
    </div>
    <div class="flex flex-col w-full h-full">
      <div class="flex flex-row editor-controls">
        <WorkIntervalDescription></WorkIntervalDescription>
<!--        <WorkIntervalTimeEditor></WorkIntervalTimeEditor>-->
      </div>
      {#if editableWorkInterval}
        {#if workIntervalProject}
        <div>
          <WorkIntervalProject workInterval={editableWorkInterval}
                               updatedWorkinterval={updatedWorkInterval}
          ></WorkIntervalProject>
        </div>
        {/if}
        <div  on:click={deleteEditableWorkInterval}
              on:keyup={() => {}}
              tabindex="0"
              role="button"
              class="m-3 bg-myroon-100 text-myhigh_white p-1 rounded cursor-pointer hover:border"
              style="height: 27px; width: 200px; margin-left: auto; margin-right: auto;"
        >delete this interval
        </div>
      {/if}
    </div>
  </div>
{/if}