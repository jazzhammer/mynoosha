<style>
  .edit-time-grid {
    display: grid;
    grid-template-columns: 2fr 4fr 2fr 2fr 4fr 2fr;
    width: 100%;
  }
  .edit-time-grid > * {
    text-align: center;
  }

  .tbm {
    height: 16px;
    width: 16px;
    font-weight: bold;
    font-size:14pt;
    margin: 0;
    margin-top: 3px;
    border-radius: 2px;
    background-color: #ea9f07;
    line-height: 10pt;
    cursor: pointer;
    border: 1px solid black;


  }
  .tbm:hover {
    transform: rotate(45deg);
  }

  .tbp {
    height: 16px;
    width: 16px;
    font-weight: bold;
    font-size:14pt;
    margin: 0;
    margin-top: 3px;
    border-radius: 2px;
    background-color: #30b20d;
    line-height: 10pt;
    cursor: pointer;
  }
  .tbp:hover {
    transform: rotate(45deg);
  }

  .tc {
    border: 1px solid black;
  }
  .bc {

  }
  .bc > * {
    margin: auto;
    margin-top: 3px;
  }
</style>
<script lang="ts">
  import type {WorkInterval} from "../models/work_interval";
  import WorkIntervalService from "../services/work_interval.service";
  import type {WorkIntervalCrud} from "../stores";
  import {crud, WorkIntervalStore} from "../stores";
  import {onDestroy} from "svelte";

  let workInterval: WorkInterval | null = null;
  $: workInterval
  const unsubWorkIntervalStore = WorkIntervalStore.subscribe((wicrud: WorkIntervalCrud) => {
    if (wicrud && wicrud.type === crud.READ) {
      if (!Array.isArray(wicrud)) {
        workInterval = wicrud.payload as WorkInterval;
      }
    }
  });
  onDestroy(unsubWorkIntervalStore);

</script>
<div class="edit-time-grid">
  <div class="bc"><div class="tbm">-</div></div>
  <div class="tc">start</div>
  <div class="bc"><div class="tbp">+</div></div>

  <div class="bc"><div class="tbm">-</div></div>
  <div class="tc">start</div>
  <div class="bc"><div class="tbp">+</div></div>

  <div class="bc"><div class="tbm">-</div></div>
  <div class="tc">start</div>
  <div class="bc"><div class="tbp">+</div></div>

  <div class="bc"><div class="tbm">-</div></div>
  <div class="tc">start</div>
  <div class="bc"><div class="tbp">+</div></div>

</div>