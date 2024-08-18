<style>
  .project-work-intervals {

  }
</style>
<script lang="ts">
  import type {Project} from "../models/project";
  import TimeRecorder from './time_recorder.svelte';

  export let project: Project;
  $: project

</script>
<div class="project-work-intervals">
  <TimeRecorder></TimeRecorder>
</div>