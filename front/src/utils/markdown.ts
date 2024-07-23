function markdownify(source: string | undefined): string {
  if (!source) {
    source = '';
  }
  const lines = source.split('\n');
  const mdLines: string[] = [];
  lines.forEach((line) => {
    line = line.trim();
    let mdLine = line;
    if (mdLine.startsWith('# ')) {
      line = line.substring(2);
      mdLine = `<h1>${line}</h1>\n`;
    } else
    if (mdLine.startsWith('## ')) {
      line = line.substring(3);
      mdLine = `<h2>${line}</h2>\n`;
    } else
    if (mdLine.startsWith('### ')) {
      line = line.substring(4);
      mdLine = `<h3>${line}</h3>\n`;
    } else
    if (mdLine.startsWith('- ')) {
      line = mdLine.substring(2);
      line = line.trim();
      if (line.startsWith('**') && line.endsWith('**')) {
        line = line.substring(2, line.length - 2);
        line = `<b>${line}</b>\n`;
      }
      else if (line.startsWith('*') && line.endsWith('*')) {
        line = line.substring(1, line.length - 1);
        line = `<i>${line}</i>\n`;
      }
      mdLine = `<li>${line}</li>\n`;
    } else
    if (mdLine.startsWith('**') && mdLine.endsWith('**')) {
      line = mdLine.substring(2, line.length - 2);
      mdLine = `<b>${line}</b>\n`;
    } else
    if (mdLine.startsWith('*') && mdLine.endsWith('*')) {
      line = mdLine.substring(1, line.length - 1);
      mdLine = `<i>${line}</i>\n`;
    }
    mdLines.push(mdLine);
  });
  let md = `<div style="text-align: left">`;
  mdLines.forEach((mdLine) => {
    md = `${md}${mdLine}`;
  });
  md = `${md}<div>`
  return md;
}
export default markdownify;