import sharp from 'sharp';
import fs from 'fs/promises';
import path from 'path';

const sourceDir = './static';
const quality = 80;

const files = await fs.readdir(sourceDir);

for (const file of files) {
    const ext = path.extname(file).toLowerCase();
    if (!['.jpg', '.jpeg', '.png'].includes(ext)) continue;

    const inputPath = path.join(sourceDir, file);
    const outputPath = inputPath.replace(/\.\w+$/, '.webp');

    await sharp(inputPath)
        .webp({ quality })
        .toFile(outputPath);

    console.log(`✅ ${file} → ${path.basename(outputPath)}`);
}
