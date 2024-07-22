export interface WorkInterval {
  start: string;
  stop?: string;
  start_utcms?: number;
  stop_utcms?: number;
  description?: string;
  client?: number;
  minutes?: number;
  hours?: number;
  localHHMMStart?: string;
  localHHMMStop?: string;
  hhmm?: string;
}