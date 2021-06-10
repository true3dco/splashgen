const ts = require("typescript");

main();

function main() {
  const sourceFile = process.argv[2];
  const importPaths = new Set();
  gatherImportPaths(sourceFile, sourceFile, importPaths);
  for (const importPath of importPaths) {
    console.log(importPath);
  }
}

function gatherImportPaths(nodeFileLocation, sourceFileLocation, importPaths) {
  const node = createTheNodeAndShit(nodeFileLocation);
  walkTheTree(node, (child) => {
    if (!isAnImportStatement(child)) {
      return;
    }
    const path = getTheModulePath(child);
    if (!path.startsWith(".")) {
      return;
    }

    const pathFromSource = convertThePathSoInsteadOfComingFrom(
      nodeFileLocation,
      sourceFileLocation
    );
    const alreadyProcessed = importPaths.has(pathFromSource);
    if (alreadyProcessed) {
      return;
    }
    // NOTE: We handle normalizing all of these paths
    importPaths.add(pathFromSource);
    const resolvedFile = resolvePathToFile(pathFromSource, sourceFileLocation);
    gatherImportPaths(resolvedFile, sourceFileLocation, importPaths);
  });
}
