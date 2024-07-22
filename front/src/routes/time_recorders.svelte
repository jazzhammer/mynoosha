<style>
  .recorder-flow {
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
  }
</style>
<script lang="ts">
  import TimeRecorder from './time_recorder.svelte';
  import type {Client} from "../models/client";
  import {RecordableClientsStore, WorkIntervalListsByClient} from "../stores";
  import {onDestroy} from "svelte";
  import type {WorkInterval} from "../models/work_interval";

  let clients: Client[] = []
  const unsubscribe = RecordableClientsStore.subscribe((founds: Client[]) => {
    clients = founds;
    // console.log(`new set of recordables: ${JSON.stringify(clients)}`);
  });
  onDestroy(unsubscribe);

  let workIntervalListsByClient: {[key: number]: WorkInterval[]} = {};

  const unsubWorkIntervalLists = WorkIntervalListsByClient.subscribe((lists: {[key: number]: WorkInterval[]}) => {
    workIntervalListsByClient = lists;
  });

</script>
<div class="bg-mymid_white w-full h-lvh recorder-flow text-mywood-900">
  {#each clients as client}
    <TimeRecorder
      client={client}
      workIntervalList={workIntervalListsByClient[client.id]}
    ></TimeRecorder>
  {/each}
</div>