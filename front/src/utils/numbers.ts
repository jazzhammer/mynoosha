export function padLeft(value: number, length: number): string {
  const cat = `${'0'.repeat(length)}${value}`
  return cat.substring(cat.length - length);
}