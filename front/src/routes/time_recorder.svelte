<style>
  .time-recorder {
    display: flex;
    flex-direction: column;
  }
  .work-interval-list-header-row {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 5fr;
    font-size: 9pt;
  }
  .work-interval-list-header-row > * {
    text-align: center;
    border-bottom: 1px solid;
  }
  .work-interval-list-row {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 5fr;
    font-size: 9pt;
  }
  .work-interval-list-row > * {
    text-align: center;
  }
</style>
<script lang="ts">

  import type {Client} from "../models/client";
  import type {WorkInterval} from "../models/work_interval";
  import WorkIntervalService from "../services/work_interval.service";
  import { DateTime } from "luxon";
  import {onDestroy} from "svelte";
  import {padLeft} from "../utils/numbers.js";

  export let client: Client;
  export let workIntervalList: WorkInterval[];

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

  let debouncedCreateWorkTimeInterval: any;
  function createWorkInterval(keyEvent: any): void {
    // debugger;
    if (debouncedCreateWorkTimeInterval) {
      clearTimeout(debouncedCreateWorkTimeInterval);
    }
    if (!keyEvent || (keyEvent.code==='Enter' || keyEvent.code === 'Space')) {
      debouncedCreateWorkTimeInterval = setTimeout(
        () => {
          const dt = DateTime.utc().toISO();
          WorkIntervalService.create({
            start: dt,
            client: client.id
          }).then((response: any) => {
            if (response.data) {
              const created = response.data;

              const isoStart = DateTime.fromISO(created.start)
              const isoStartLocal = isoStart.toLocal();
              created.localHHMMStart = `${isoStartLocal.hour > 9 ? isoStartLocal.hour : '0' + isoStartLocal.hour}:${isoStartLocal.minute > 9 ? isoStartLocal.minute : '0' + isoStartLocal.minute}`;

              if (created.stop) {
                const isoStop = DateTime.fromISO(created.stop)
                const isoStopLocal = isoStop.toLocal();
                created.localHHMMStop = `${isoStopLocal.hour > 9 ? isoStopLocal.hour : '0' + isoStopLocal.hour}:${isoStopLocal.minute > 9 ? isoStopLocal.minute : '0' + isoStopLocal.minute}`;
                const HH = Math.floor((created.stop_utcms - created.start_utcms) / 3600);
                const MM = Math.floor((created.stop_utcms - created.start_utcms) - HH * 3600);
                created.hhmm = `${HH < 10 ? '0' + HH : HH}:${MM < 10 ? '0' + MM : MM}`;
              }

              let nextWorkIntervalList = []
              workIntervalList = workIntervalList ? workIntervalList: [];
              nextWorkIntervalList = [...workIntervalList, created];
              workIntervalList = nextWorkIntervalList;
              console.log(`created workInterval ${JSON.stringify(created)}`);
            }
          });
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
        debugger;
        const dt = DateTime.utc().toISO();
        WorkIntervalService.update({
          id: workInterval.id,
          start: workInterval.start,
          stop: dt,
        }).then((response: any) => {
          if (response.data) {
            const updated = response.data;

            const isoStart = DateTime.fromISO(updated.start)
            const isoStartLocal = isoStart.toLocal();
            updated.localHHMMStart = `${isoStartLocal.hour > 9 ? isoStartLocal.hour : '0' + isoStartLocal.hour}:${isoStartLocal.minute > 9 ? isoStartLocal.minute : '0' + isoStartLocal.minute}`;

            if (updated.stop) {
              const isoStop = DateTime.fromISO(updated.stop)
              const isoStopLocal = isoStop.toLocal();
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


</script>
<div class="border-2 border-myroon-100 rounded text-mywood-900 m-2 time-recorder" style="min-width: 400px; min-height: 200px; max-width: 450px; max-height: 250px;">
  <div class="h-2/12 text-center text-myhigh_white bg-myroon-100">{client.name}</div>
  <div class="work-interval-list-header-row">
    <div class="">start</div>
    <div>stop</div>
    <div>hh:mm</div>
    <div>description</div>
  </div>
  {#if workIntervalList}
  {#each workIntervalList as workInterval}
  <div class="work-interval-list-row">
    <div class="bg-myhigh_white">{workInterval.localHHMMStart}</div>
    <div class="bg-myhigh_white">{workInterval.localHHMMStop ? workInterval.localHHMMStop : tickedHourMinute }</div>
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
    <div class="bg-myhigh_white">{workInterval.description ? workInterval.description : ''}</div>
  </div>
  {/each}
  {/if}

    <div on:click={() => createWorkInterval(null)}
         on:keyup={() => {}}
         tabindex="0"
         role="button"
         class="bg-myblue-100 w-full text-xl cursor-pointer hover:border text-myhigh_white">+</div>
</div>