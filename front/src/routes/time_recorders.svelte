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
  import {
    RecordableClientsStore,
  } from "../stores";
  import {onDestroy} from "svelte";

  let clients: Client[] = []
  const unsubscribe = RecordableClientsStore.subscribe((founds: Client[]) => {
    clients = founds;
  });
  onDestroy(unsubscribe);

  // let workIntervalListsByClient: {[key: number]: WorkInterval[]} = {};
  // $: workIntervalListsByClient
  // const unsubWorkIntervalLists = WorkIntervalListsByClient.subscribe((lists: {[key: number]: WorkInterval[]}) => {
  //   workIntervalListsByClient = lists;
  // });
  // onDestroy(unsubWorkIntervalLists)


</script>
<div class="bg-mymid_white w-full h-lvh recorder-flow text-mywood-900">
  <TimeRecorder></TimeRecorder>
</div>