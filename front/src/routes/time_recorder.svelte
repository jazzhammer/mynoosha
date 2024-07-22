<style>
  .time-recorder {
    display: flex;
    flex-direction: column;
  }
  .work-interval-list-header-row {
    display: grid;
    grid-template-columns: 1fr 1fr 2fr 4fr;
    font-size: 9pt;
  }
  .work-interval-list-header-row > * {
    text-align: center;
    border-bottom: 1px solid;
  }
  .work-interval-list-row {
    display: grid;
    grid-template-columns: 1fr 1fr 2fr 4fr;
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

  export let client: Client;
  export let workIntervalList: WorkInterval[];

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
</script>
<div class="border-2 border-myroon-100 rounded text-mywood-900 m-2 time-recorder" style="min-width: 300px; min-height: 200px; max-width: 350px; max-height: 250px;">
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
    <div class="bg-myhigh_white">{workInterval.localHHMMStop ? workInterval.localHHMMStop : '' }</div>
    <div class="bg-myhigh_white">{workInterval.hhmm ? workInterval.hhmm : ''}</div>
    <div class="bg-myhigh_white">{workInterval.description ? workInterval.description : ''}</div>
  </div>
  {/each}
  {/if}

    <div on:click={() => createWorkInterval(null)}
         on:keyup={createWorkInterval}
         tabindex="0"
         role="button"
         class="bg-myblue-100 w-full text-xl cursor-pointer hover:border text-myhigh_white">+</div>
</div>