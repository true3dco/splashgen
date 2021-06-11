const fs = require("fs");
const path = require("path");
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
  const node = ts.createSourceFile(
    nodeFileLocation,
    fs.readFileSync(nodeFileLocation, "utf-8"),
    ts.ScriptTarget.Latest
  );

  walkTheTree(node, (child) => {
    if (!isAnImportStatement(child)) {
      return;
    }
    const modPath = getTheModulePath(child);
    if (!modPath.startsWith(".")) {
      return;
    }

    const pathFromSource = convertThePathSoInsteadOfComingFrom(
      modPath,
      nodeFileLocation,
      sourceFileLocation
    );
    const alreadyProcessed = importPaths.has(pathFromSource);
    if (alreadyProcessed) {
      return;
    }
    // NOTE: We handle normalizing all of these paths
    importPaths.add(pathFromSource);
    const resolvedFile = resolvePathToJsTsFile(
      pathFromSource,
      sourceFileLocation
    );
    if (resolvedFile) {
      gatherImportPaths(resolvedFile, sourceFileLocation, importPaths);
    }
  });
}

function walkTheTree(node, fn) {
  fn(node);
  ts.forEachChild(node, (child) => walkTheTree(child, fn));
}

function isAnImportStatement(node) {
  return node.kind === ts.SyntaxKind.ImportDeclaration;
}

function getTheModulePath(importDecl) {
  return importDecl.moduleSpecifier.text;
}

function convertThePathSoInsteadOfComingFrom(importPath, origFile, targetFile) {
  // NOTE: This is a very simple way to resolve relative imports.
  const origDir = path.dirname(origFile);
  const absModulePath = path.resolve(origDir, importPath);

  const targetDir = path.dirname(targetFile);
  // Must use POSIX path normalization to make sure imports are accounted for.
  let relModulePathFromTarget = path.posix.normalize(
    path.relative(targetDir, absModulePath)
  );
  if (!relModulePathFromTarget.startsWith(".")) {
    relModulePathFromTarget = `./${relModulePathFromTarget}`;
  }
  return relModulePathFromTarget;
}

function resolvePathToJsTsFile(pathFromSource, sourceFileLocation) {
  const _JS_TS_EXTS = [".js", ".jsx", ".tsx", ".ts"];
  // TODO: Maybe use TS's actual module resolution API in the future? This seems to work for now
  const ext = path.extname(pathFromSource);
  const hasNoExt = ext === "";
  const isJsTsModule = _JS_TS_EXTS.includes(ext) || hasNoExt;
  if (!isJsTsModule) {
    return null;
  }

  // TODO: Needs module resolution dirs?
  let absPath = path.resolve(path.dirname(sourceFileLocation), pathFromSource);
  if (hasNoExt) {
    let correctExt = "";
    for (let jsTsExt of _JS_TS_EXTS) {
      if (fs.existsSync(absPath + jsTsExt)) {
        correctExt = jsTsExt;
        break;
      }
    }
    if (!correctExt) {
      throw new Error(
        `Could not find extension for module path ${absPath} (resolving import ${pathFromSource} from ${sourceFileLocation})`
      );
    }
    absPath += correctExt;
  }

  return absPath;
}
