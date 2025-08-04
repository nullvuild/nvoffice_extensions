// 파일명에 POSTFIX를 붙여 이름을 바꿔주는 모듈
// args: [file1, file2, ..., postfix]
const fs = require('fs');
const path = require('path');

async function run() {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.log('ERROR: 파일과 POSTFIX를 인자로 전달하세요.');
    process.exit(1);
  }
  const postfix = args[args.length - 1];
  const files = args.slice(0, -1);
  let result = '';
  for (const file of files) {
    try {
      const dir = path.dirname(file);
      const ext = path.extname(file);
      const base = path.basename(file, ext);
      const newName = base + postfix + ext;
      const newPath = path.join(dir, newName);
      fs.copyFileSync(file, newPath);
      result += `${file} → ${newName}\n`;
    } catch (e) {
      result += `ERROR: ${file}: ${e.message}\n`;
    }
  }
  console.log(result.trim());
}

run();
