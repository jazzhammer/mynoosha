<style>
  .project-work-pieces {

  }
</style>
<script lang="ts">
  import type {Project} from "../models/project";
  // import TimeRecorder from './time_recorder.svelte';
  import WorkPieceList from './work_piece_list.svelte';
  import WorkPieceService from "../services/work_piece.service";
  import type {WorkPiece} from "../models/work_piece";
  import {type WorkPieceCrud, WorkPieceStore} from "../stores";
  import {onDestroy} from "svelte";

  export let project: Project;
  $: project

  let workPieces: WorkPiece[];
  $: workPieces

  const getWorkPieces = (): void => {
    if (project) {
      WorkPieceService.find({project: project.id}).then((response: any) => {
        workPieces = response.data;

      });
    }
  }
  getWorkPieces();
  const unsubWorkPiece = WorkPieceStore.subscribe((wicrud: WorkPieceCrud) => {
    if (!Array.isArray(wicrud)) {
      getWorkPieces();
    }
  })
  onDestroy(unsubWorkPiece);
  const selectWorkPiece = (next: WorkPiece): void => {
    console.log(`project work pieces: selectedWorkPiece: ${next.id}`);
  }
</script>
<div class="project-work-pieces">
  <WorkPieceList workPieces={workPieces} selectWorkPiece={selectWorkPiece}></WorkPieceList>
</div>