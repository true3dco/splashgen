const fs = require("fs");
const path = require("path");
const favicons = require("favicons");

main().catch((err) => {
  console.error(err.message);
  process.exit(1);
});

async function main() {
  const source = process.argv[2];
  if (!source) {
    throw new Error("Source required");
  }

  const outputDir = process.argv[3];
  if (!outputDir) {
    throw new Error("Output Directory required");
  }

  const { images } = await favicons(source);
  const faviconIco = images.find(({ name }) => name === "favicon.ico");
  if (!faviconIco) {
    throw new Error("Could not find favicon?");
  }
  fs.writeFileSync(path.join(outputDir, faviconIco.name), faviconIco.contents);
}
