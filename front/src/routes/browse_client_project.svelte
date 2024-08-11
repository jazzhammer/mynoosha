<style>
  .client-form-fields {
    display: grid;
    grid-template-columns: 1fr;
    width: 180px;
  }

  .client-form-fields > * {
    margin-bottom: 2px;
  }

  .field-label {
    text-align: left;
    width: 110px;
  }

  .search-bar {
    display: grid;
    grid-template-columns: 4fr 4fr 4fr 4fr 1fr 1fr;
    width: 100%;
  }

  .search-bar > * {
    margin: 0;
  }

</style>
<script lang="ts">

  import {type ClientCrud, ClientStore, crud, ProjectStore} from "../stores";


  import { DatePicker } from "@svelte-plugins/datepicker";
  import { format } from 'date-fns';
  import { type Client } from "../models/client";
  import { onDestroy}  from "svelte";
  import ProjectService from "../services/project.service";
  import { type Project } from "../models/project";
  import ProjectList from './project_list.svelte';

  let dateFormat = 'yyyy-MM-dd';

  let initialYmdFrom = new Date();
  initialYmdFrom.setDate(1);
  let initialYmdThrough = new Date();
  let ymdFrom = initialYmdFrom;
  let ymdThrough = initialYmdThrough;
  $: ymdFrom
  $: ymdThrough

  let projects: Project[] = [];
  $: projects

  function previousMonth() : void {
    ymdFrom.setMonth(ymdFrom.getMonth() - 1)
    ymdThrough.setMonth(ymdThrough.getMonth() - 1)
    formattedYmdIssueFrom = formatDate(ymdFrom);
    formattedYmdIssueThrough = formatDate(ymdThrough);
    retrieveProjects();
  }

  function nextMonth(): void {
    ymdFrom.setMonth(ymdFrom.getMonth() + 1)
    ymdThrough.setMonth(ymdThrough.getMonth() + 1)
    formattedYmdIssueFrom = formatDate(ymdFrom);
    formattedYmdIssueThrough = formatDate(ymdThrough);
    retrieveProjects();
  }



  let isOpenFrom = false;
  let isOpenThrough = false;

  const toggleDatePickerFrom = () => (isOpenFrom = !isOpenFrom);
  const toggleDatePickerThrough = () => (isOpenThrough = !isOpenThrough);

  const formatDate = (dateString: Date) => {
    return dateString && format(new Date(dateString), dateFormat) || '';
  };

  let formattedYmdIssueFrom = formatDate(initialYmdFrom);
  let formattedYmdIssueThrough = formatDate(initialYmdThrough);

  let client: Client;
  $: client
  const unsubClient = ClientStore.subscribe((ccrud: ClientCrud) => {
    if (!Array.isArray(ccrud.payload)) {
      client = ccrud.payload as Client
    }
  });
  onDestroy(unsubClient)

  $: formattedYmdIssueFrom
  $: formattedYmdIssueThrough

  function createProject(): void {
    ProjectService.create({
      client: client.id
    }).then((response: any) => {
      const created = response.data;
      ProjectStore.set({
        type: crud.CREATE,
        payload: created
      });
    })
  }


  function setYmdFrom(event: any): void {
    ymdFrom = new Date(event.startDate)
    formattedYmdIssueFrom = formatDate(ymdFrom);
    retrieveProjects();
  }

  function setYmdThrough(event: any): void {
    ymdThrough = new Date(event.startDate)
    formattedYmdIssueThrough = formatDate(ymdThrough);
    retrieveProjects();
  }


  let retrieveProjectTimeout: any = null;

  function retrieveProjects(): void {
    if (retrieveProjectTimeout) {
      clearTimeout(retrieveProjectTimeout);
    }
    retrieveProjectTimeout = setTimeout(
      () => {
        if (ymdFrom && ymdThrough && ymdFrom.getTime() < ymdThrough.getTime()) {
          const ymdFromBod = new Date(ymdFrom);
          ymdFromBod.setHours(0);
          ymdFromBod.setMinutes(0);
          const ymdThroughEod = new Date(ymdThrough);
          ymdThroughEod.setDate(ymdThrough.getDate() + 1);
          ymdThroughEod.setHours(0);
          ymdThroughEod.setMinutes(0);
          ProjectService.find({
            ymdIssueFrom: ymdFromBod.toISOString(),
            ymdIssueThrough: ymdThroughEod.toISOString(),
            client: client.id
          }).then((response: any) => {
            const founds = response.data;
            projects = founds;
          });
        } else {
          // console.log(`invalid project search interval:`);
          // console.log(`from:    ${ymdFrom ? ymdFrom.getTime() : 'none'}`)
          // console.log(`through: ${ymdThrough ? ymdThrough.getTime() : 'none'}`)
        }
      },
      500
    );
  }

  function selectProject(selected: Project): void {
    ProjectStore.set({
      type: crud.READ,
      payload: selected
    })
  }
</script>
<div class="new-project flex flex-col border-myroon-100 border p-3 mr-6 ml-3 rounded w-full text-myhigh_white"
     style="min-width: 226px; max-width: 375px; font-size: 10pt;" data-testid="browse_project"
>
  <div class="bg-mywood-900 rounded mb-5 w-full" data-testid="browse_project_header" id="browse_project_header">browse projects</div>
  <div class="search-bar text-mywood-900 flex flex-row" data-testid="browse_project_form">
    <div class="" data-testid="browse_project_name">from</div>
    <div>
      <DatePicker onDayClick={setYmdFrom} isOpen={isOpenFrom} startDate={initialYmdFrom} enableFutureDates={true}>
        <input type="text"
               placeholder="from"
               value={formattedYmdIssueFrom}
               on:click={toggleDatePickerFrom}
               style="width: 100px; font-size: 9pt; height: 18px; text-align: center;"
        />
      </DatePicker>
    </div>
    <div class="" data-testid="browse_project_name">through</div>
    <div>
      <DatePicker onDayClick={setYmdThrough} isOpen={isOpenThrough} startDate={initialYmdThrough} enableFutureDates={true}>
        <input type="text"
               placeholder="through"
               value={formattedYmdIssueThrough}
               on:click={toggleDatePickerThrough}
               style="width: 100px; font-size: 9pt; height: 18px; text-align: center;"
        />
      </DatePicker>
    </div>
    <div on:click={previousMonth}
          class="pl-2 pr-2 text-center bg-mywood-100 rounded cursor-pointer"
         style="height: 18px; margin-top: 3px; font-size: 8pt; padding-top: 0px; font-weight: bold; position: relative; margin-left: 4px; margin-right: 2px;"
    ><div style="position: absolute; left: 4px; top: -3px; margin: 0;">&lt;</div></div>
    <div on:click={nextMonth}
         class="pl-2 pr-2 text-center bg-mywood-100 rounded cursor-pointer"
         style="height: 18px; margin-top: 3px; font-size: 8pt; padding-top: 0px; font-weight: bold; position: relative; margin-left: 2px; margin-right: 2px;"
    ><div class="" style="position: absolute; left: 4px; top: -3px; margin: 0;">&gt;</div></div>
  </div>
  <div class="project-list-container">
    <ProjectList projects={projects} selectProject={selectProject}></ProjectList>
  </div>
</div>
