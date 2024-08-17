<script lang="ts">

  import {format} from "date-fns";
  import {DatePicker} from "@svelte-plugins/datepicker";


  let dateFormat = 'yyyy-MM-dd';
  const formatDate = (dateString: Date) => {
    return dateString && format(new Date(dateString), dateFormat) || '';
  };
  export let initialYmd = new Date();
  initialYmd.setDate(1);
  let ymd = initialYmd;
  $: ymd
  let isOpen = false;
  const toggleDatePicker = () => (isOpen = !isOpen);

  let formattedYmd = formatDate(initialYmd);
  function setYmd(event: any): void {
    ymd = new Date(event.startDate)
    formattedYmd = formatDate(ymd);
    selectYmd(formattedYmd)
  }

  export let selectYmd = (next: string) => {
    console.log(`selected ymd: ${formattedYmd}`);
  }

</script>
<div>
  <DatePicker onDayClick={setYmd} isOpen={isOpen} startDate={initialYmd} enableFutureDates={true}>
    <input type="text"
           placeholder="from"
           value={formattedYmd}
           on:click={toggleDatePicker}
           style="width: 100px; font-size: 9pt; height: 18px; text-align: center;"
    />
  </DatePicker>
</div>
